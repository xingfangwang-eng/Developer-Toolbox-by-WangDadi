import os
import json
import time
import random
import concurrent.futures
from tqdm import tqdm
import requests

# 全局变量
API_KEY = "sk-acea097d87da45508303b0662a398434"
API_ENDPOINT = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"
THREAD_COUNT = 2  # 严格限制在 2 个并发
PROGRESS_LOG = "rewrite_progress.log"
PROJECTS_JSON = "projects.json"

# 创建 requests session 以复用 TCP 连接
session = requests.Session()
session.headers.update({
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
})

# 读取已处理文件列表
processed_files = set()
if os.path.exists(PROGRESS_LOG):
    with open(PROGRESS_LOG, 'r', encoding='utf-8-sig') as f:
        for line in f:
            processed_files.add(line.strip())

# 加载项目信息
def load_projects():
    if os.path.exists(PROJECTS_JSON):
        try:
            with open(PROJECTS_JSON, 'r', encoding='utf-8-sig') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载项目信息失败: {e}")
    return {}

# 检查文件是否包含乱码字符
def contains_garbled_chars(content):
    garbled_chars = ['å', 'æ', 'ì']
    for char in garbled_chars:
        if char in content:
            return True
    return False

# 提取项目信息和语言
def extract_info(file_path):
    # 从文件路径中提取信息
    parts = file_path.split(os.sep)
    # 寻找 manual 目录
    manual_index = -1
    for i, part in enumerate(parts):
        if part == 'manual':
            manual_index = i
            break
    
    if manual_index != -1 and manual_index + 2 < len(parts):
        project_name = parts[manual_index + 1]
        lang = parts[manual_index + 2].split('.')[0]  # 如 ja.md -> ja
        return project_name, lang
    return "", "en"

# 检查文件是否需要重写（包含占位符）
def needs_rewrite(content):
    placeholders = ["Describe feature", "Step 1", "説明する"]
    for placeholder in placeholders:
        if placeholder in content:
            return True
    return False

# 调用 DeepSeek API 重写内容
def rewrite_content(content, project_name, keywords, lang):
    # 强制类型转换，确保所有变量都是字符串
    project_name = str(project_name or "")
    keywords = str(keywords or "")
    lang = str(lang or "en")
    content = str(content or "")
    
    # 模拟“慢速工作的专家” - 随机呼吸
    time.sleep(random.uniform(1.5, 3.5))
    
    prompt = '你不再是翻译官，你是这个项目的首席架构师。\n项目名：' + project_name + '，关键词：' + keywords + '，目标语言：' + lang + '。\n请彻底重写这段 Markdown，要求如下：\n1. 严禁翻译原本的 "Describe feature" 或 "説明する" 等词汇。\n2. 根据项目名和关键词，发挥想象力编写 3 个真实的、硬核的技术功能。例如：如果是 champions-sp-calc，你应该写它如何精准计算英雄技能点分配、支持多版本数据对比等。\n3. 必须包含具体的参数名、技术指标（如：ミリ秒単位の計算、PostgreSQLとの連携）。\n4. 语言必须是 100% 地道的 ' + lang + '。\n5. 彻底删除 Related Resources 里所有包含 example.com 的假链接。\n6. 替换为：👉 `https://www.wangdadi.xyz/?utm_source=github`。\n7. 必须生成 3 个详细的操作步骤，内容要显得极度专业。\n8. 生成 2 个针对该工具的行业最佳实践建议。\n9. 直接输出正文，不要包含任何"好的，这是重写后的内容"之类的废话。\n\n原文：\n' + content
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2000,
        "temperature": 0.7
    }
    
    try:
        # 使用 session 发送请求，复用 TCP 连接
        response = session.post(API_ENDPOINT, json=payload, timeout=180)
        
        # 检查是否是 429 错误（Rate Limit）
        if response.status_code == 429:
            print("API Error 429: Rate Limit Exceeded. Sleeping for 30 seconds...")
            time.sleep(30)  # 指数退避 - 强制休眠 30 秒以上
            return None
        
        response.raise_for_status()
        result = response.json()
        # 空响应防御
        content = result.get("choices", [{}])[0].get("message", {}).get("content", None)
        if not content:
            print("Empty Response from API")
            return None
        return content
    except requests.exceptions.Timeout:
        print("API Request Timeout")
        return None
    except Exception as e:
        print(f"API Error: {str(e)}")
        return None

# 处理单个文件
def process_file(file_path, projects):
    # 读取文件内容，使用 utf-8-sig 编码
    try:
        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f"读取文件失败 {file_path}: {e}")
        # 记录错误
        with open('error.log', 'a', encoding='utf-8-sig') as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - 读取失败 - {file_path} - {str(e)}\n")
        return False
    
    # 检查是否需要重写（包含占位符）
    if not needs_rewrite(content):
        # 记录为已处理
        with open(PROGRESS_LOG, 'a', encoding='utf-8-sig') as f:
            f.write(file_path + '\n')
        return True
    
    # 最多尝试 3 次
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # 提取项目信息
            project_name, lang = extract_info(file_path)
            
            # 获取项目关键词
            keywords = ""
            if project_name and project_name in projects:
                keywords = projects[project_name].get("keywords", "")
            
            # 调用 API 重写
            rewritten_content = rewrite_content(content, project_name, keywords, lang)
            
            if rewritten_content and len(rewritten_content) > 150:
                # 检查是否仍包含占位符
                if not needs_rewrite(rewritten_content):
                    # 写入新内容，使用 utf-8-sig 编码
                    with open(file_path, 'w', encoding='utf-8-sig') as f:
                        f.write(rewritten_content)
                    
                    # 实时记录已处理
                    with open(PROGRESS_LOG, 'a', encoding='utf-8-sig') as f:
                        f.write(file_path + '\n')
                    
                    return True
                else:
                    print("Rewritten content still contains placeholders")
            else:
                print("Rewritten content is too short or empty")
                time.sleep(2)  # 等待 2 秒后重试
        except Exception as e:
            print(f"处理失败 {file_path}: {e}")
            time.sleep(2)  # 等待 2 秒后重试
    
    # 所有尝试都失败，记录到错误日志
    with open('error.log', 'a', encoding='utf-8-sig') as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - 处理失败 - {file_path}\n")
    
    return False

# 主函数
def main():
    # 加载项目信息
    projects = load_projects()
    
    # 收集 manual/ 下的所有 .md 文件
    md_files = []
    base_dir = os.path.dirname(os.path.abspath(__file__))
    manual_dir = os.path.join(base_dir, 'manual')
    
    if os.path.exists(manual_dir):
        for root, dirs, files in os.walk(manual_dir):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    md_files.append(file_path)
    
    total_files = len(md_files)
    print(f"共发现 {total_files} 个 .md 文件")
    
    # 过滤已处理的文件
    pending_files = [f for f in md_files if f not in processed_files]
    pending_count = len(pending_files)
    print(f"待处理文件数: {pending_count}")
    
    # 多线程处理
    processed_count = 0
    success_count = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
        # 创建任务
        future_to_file = {executor.submit(process_file, file, projects): file for file in pending_files}
        
        # 处理结果
        for future in tqdm(concurrent.futures.as_completed(future_to_file), total=pending_count, desc="处理进度"):
            file = future_to_file[future]
            try:
                success = future.result()
                processed_count += 1
                if success:
                    success_count += 1
            except Exception as e:
                print(f"处理文件时发生异常 {file}: {e}")
    
    print(f"\n处理完成！")
    print(f"总文件数: {total_files}")
    print(f"已处理文件数: {processed_count}")
    print(f"成功重写文件数: {success_count}")
    print(f"失败文件数: {processed_count - success_count}")

if __name__ == "__main__":
    main()