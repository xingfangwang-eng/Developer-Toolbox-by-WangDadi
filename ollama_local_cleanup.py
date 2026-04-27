import os
import json
import time
import requests
from tqdm import tqdm

# 全局变量
OLLAMA_API_ENDPOINT = "http://localhost:11434/api/generate"
MODEL = "qwen2:1.5b"
PROGRESS_LOG = "rewrite_progress.log"
PROJECTS_JSON = "projects.json"

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

# 检查文件是否需要重写（包含占位符）
def needs_rewrite(content):
    # 检查是否包含完整的原始占位符
    if "Describe feature" in content:
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

# 调用 Ollama API 生成内容
def generate_content(content, project_name, keywords, lang):
    # 强制类型转换，确保所有变量都是字符串
    project_name = str(project_name or "")
    keywords = str(keywords or "")
    lang = str(lang or "en")
    content = str(content or "")
    
    prompt = f"你是一个顶级技术作家。严禁输出 \"Describe\", \"Placeholder\", \"Step 1\" 等词汇。\n任务：根据项目名 {project_name} 和 关键词 {keywords}，【编撰】一段专业的、详细的、具有吸引力的功能介绍和使用指南。\n必须完全替换掉原本的占位符。直接输出 {lang} 语言的 Markdown。\n\n请确保内容包含：\n1. 3 个详细的技术功能介绍\n2. 具体的参数名和技术指标\n3. 3 个详细的操作步骤\n4. 2 个行业最佳实践建议\n5. 底部链接：👉 `https://www.wangdadi.xyz/?utm_source=github_local`\n\n原文：\n{content}"
    
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "max_tokens": 2000,
        "temperature": 0.7,
        "stream": False
    }
    
    while True:
        try:
            response = requests.post(OLLAMA_API_ENDPOINT, json=payload, timeout=300)
            response.raise_for_status()
            result = response.json()
            # 获取生成的内容
            generated_content = result.get("response", "")
            if not generated_content:
                print("Empty Response from Ollama")
                return None
            return generated_content
        except requests.exceptions.ConnectionError:
            print("正在等待 Ollama 服务恢复...")
            time.sleep(30)
        except requests.exceptions.Timeout:
            print("Ollama Request Timeout")
            return None
        except Exception as e:
            print(f"Ollama Error: {str(e)}")
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
    
    # 最多尝试 2 次
    max_retries = 2
    last_generated_content = None
    
    for attempt in range(max_retries):
        try:
            # 提取项目信息
            project_name, lang = extract_info(file_path)
            
            # 获取项目关键词
            keywords = ""
            if project_name and project_name in projects:
                keywords = projects[project_name].get("keywords", "")
            
            # 调用 Ollama API 生成内容
            generated_content = generate_content(content, project_name, keywords, lang)
            last_generated_content = generated_content
            
            if generated_content and len(generated_content) > 200:
                # 检查是否仍包含完整的原始占位符
                if not needs_rewrite(generated_content):
                    # 确保底部链接正确
                    if "https://www.wangdadi.xyz/?utm_source=github_local" not in generated_content:
                        # 如果链接不正确，添加到末尾
                        generated_content += "\n\n---\n\n## Related Resources\n- 👉 `https://www.wangdadi.xyz/?utm_source=github_local`"
                    
                    # 写入新内容，使用 utf-8-sig 编码
                    with open(file_path, 'w', encoding='utf-8-sig') as f:
                        f.write(generated_content)
                    
                    # 实时记录已处理
                    with open(PROGRESS_LOG, 'a', encoding='utf-8-sig') as f:
                        f.write(file_path + '\n')
                    
                    return True
                else:
                    print("Generated content still contains placeholders, retrying...")
            else:
                print("Generated content is too short or empty, retrying...")
                time.sleep(2)  # 等待 2 秒后重试
        except Exception as e:
            print(f"处理失败 {file_path}: {e}")
            time.sleep(2)  # 等待 2 秒后重试
    
    # 强制保存第 2 次的结果
    if last_generated_content and len(last_generated_content) > 200:
        print("[Force Save] 注入完成，人工后续微调")
        # 确保底部链接正确
        if "https://www.wangdadi.xyz/?utm_source=github_local" not in last_generated_content:
            # 如果链接不正确，添加到末尾
            last_generated_content += "\n\n---\n\n## Related Resources\n- 👉 `https://www.wangdadi.xyz/?utm_source=github_local`"
        
        # 写入新内容，使用 utf-8-sig 编码
        with open(file_path, 'w', encoding='utf-8-sig') as f:
            f.write(last_generated_content)
        
        # 实时记录已处理
        with open(PROGRESS_LOG, 'a', encoding='utf-8-sig') as f:
            f.write(file_path + '\n')
        
        return True
    
    # 所有尝试都失败，记录到错误日志
    with open('error.log', 'a', encoding='utf-8-sig') as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - 处理失败 - {file_path}\n")
    
    return False

# 主函数
def main():
    # 加载项目信息
    projects = load_projects()
    
    # 收集当前目录及其所有子文件夹下的 .md 文件
    md_files = []
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 递归扫描所有子文件夹，排除 .git 和 venv
    for root, dirs, files in os.walk(base_dir):
        # 排除不需要的文件夹
        dirs[:] = [d for d in dirs if d not in ['.git', 'venv']]
        
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
    
    # 单线程处理
    processed_count = 0
    success_count = 0
    
    for file_path in tqdm(pending_files, desc="处理进度"):
        try:
            success = process_file(file_path, projects)
            processed_count += 1
            if success:
                success_count += 1
        except Exception as e:
            print(f"处理文件时发生异常 {file_path}: {e}")
    
    print(f"\n处理完成！")
    print(f"总文件数: {total_files}")
    print(f"已处理文件数: {processed_count}")
    print(f"成功重写文件数: {success_count}")
    print(f"失败文件数: {processed_count - success_count}")

if __name__ == "__main__":
    main()