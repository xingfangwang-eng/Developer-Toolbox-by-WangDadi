#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Colab Soul Factory - 不成功，毋宁死
暴力重写逻辑，确保每个文件都注入灵魂
"""

import os
import re
import time
import requests
import subprocess
import concurrent.futures
from tqdm import tqdm

# 配置
GITHUB_REPO = "your-github-username/your-repo-name"  # 替换为你的仓库
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# 检查环境变量
if not GITHUB_TOKEN:
    print("错误：请设置 GITHUB_TOKEN 环境变量")
    exit(1)
OLLAMA_API_ENDPOINT = "http://127.0.0.1:11434/api/generate"
OLLAMA_TAGS_ENDPOINT = "http://127.0.0.1:11434/api/tags"
MODEL = "llama3"  # 显式指定模型
MAX_WORKERS = 4  # 并发线程数

# 占位符和禁止词汇
PLACEHOLDER_PATTERNS = [
    r'Describe feature',
    r'Step 1',
    r'Practice 1',
    r'Beschreiben',
    r'Beschreiben Funktion',
    r'Schritt 1',
    r'説明する',
    r'ステップ 1',
    r'Describir',
    r'Describir función',
    r'Paso 1'
]

FORBIDDEN_WORDS = [
    'Describe', 'feature', 'Beschreiben', 'Funktion', 'Schritt',
    '説明する', 'ステップ', 'Describir', 'función', 'Paso'
]

# 全局变量
processed_count = 0
lock = concurrent.futures.ThreadPoolExecutor(max_workers=1)

# API 验证
def verify_api():
    """验证 Ollama API 是否就绪"""
    print("验证 Ollama API 连接...")
    try:
        response = requests.get(OLLAMA_TAGS_ENDPOINT, timeout=10)
        if response.status_code == 200:
            print("Ollama API 连接成功！")
            return True
        else:
            print(f"Ollama 服务返回状态码: {response.status_code}")
            print(f"错误响应: {response.text}")
            print("Ollama 服务未就绪，请先运行点火单元格")
            exit(1)
    except Exception as e:
        print(f"无法连接 Ollama 服务: {e}")
        print("Ollama 服务未就绪，请先运行点火单元格")
        exit(1)

# 等待 Ollama 服务就绪
def wait_for_ollama():
    """等待 Ollama 服务就绪"""
    print("等待 Ollama 服务启动...")
    attempt = 0
    while True:
        attempt += 1
        try:
            response = requests.get(OLLAMA_TAGS_ENDPOINT, timeout=10)
            if response.status_code == 200:
                print("Ollama 服务已就绪！")
                return True
            else:
                print(f"Ollama 服务状态码: {response.status_code} (尝试 {attempt})，正在等待 5 秒...")
                print(f"错误响应: {response.text}")
                time.sleep(5)
        except Exception as e:
            print(f"无法连接 Ollama 服务 (尝试 {attempt}): {e}，正在等待 5 秒...")
            time.sleep(5)

# 语言检测
def detect_file_language(file_path):
    """根据文件路径检测语言"""
    if '/de/' in file_path:
        return "de"
    elif '/es/' in file_path:
        return "es"
    elif '/ja/' in file_path:
        return "ja"
    return "en"  # 默认英语

# 提取项目信息
def extract_project_info(file_path):
    """从文件路径提取项目信息"""
    # 提取项目名
    parts = file_path.split(os.sep)
    project_name = ""
    for part in parts:
        if part == "manual":
            break
        if part and not part.startswith('.'):
            project_name = part
    
    # 生成关键词
    keywords = [project_name]
    if "postgres" in project_name.lower():
        keywords.extend(["database", "SQL", "PostgreSQL"])
    elif "notion" in project_name.lower():
        keywords.extend(["productivity", "collaboration", "database"])
    elif "cron" in project_name.lower():
        keywords.extend(["scheduling", "automation", "tasks"])
    else:
        keywords.extend(["tool", "automation", "productivity"])
    
    return project_name, keywords

# 生成系统提示
def generate_system_prompt(lang):
    """根据语言生成系统提示"""
    if lang == "de":
        return "Du bist ein führender deutscher IT-Architekt. Schreibe ausschließlich auf Deutsch. Alle technischen Begriffe müssen in deutscher Sprache formuliert werden."
    elif lang == "ja":
        return "あなたは日本の経験豊富なソフトウェアエンジニアです。完全に日本語で書いてください。すべての技術用語は日本語で表現してください。"
    elif lang == "es":
        return "Eres un experto técnico latinoamericano. Escribe exclusivamente en español. Todos los términos técnicos deben estar formulados en español."
    else:  # en
        return "You are a senior Silicon Valley DevOps engineer. Write exclusively in English. All technical terms must be formulated in English."

# 检查内容是否包含占位符
def contains_placeholders(content):
    """检查内容是否包含占位符"""
    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            return True
    return False

# 生成内容
def generate_content(content, project_name, keywords, lang):
    """调用 Ollama 生成内容（暴力模式）"""
    # 生成系统提示
    system_prompt = generate_system_prompt(lang)
    
    # 生成用户提示
    user_prompt = f"""直接重写 Markdown。要求：根据项目名 {project_name} 和关键词 {', '.join(keywords)}，生成地道、硬核的 {lang} 技术说明。字数 > 500。严禁输出任何废话和占位符。

{content}

IMPORTANT: Output ONLY the Markdown content. Do NOT include any introductory text. No conversational filler. Just the code.
"""
    
    # 构建请求
    payload = {
        "model": MODEL,
        "prompt": user_prompt,
        "system": system_prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "max_tokens": 2000
        }
    }
    
    # 创建会话
    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=10))
    
    max_retries = 10
    for attempt in range(max_retries):
        try:
            response = session.post(OLLAMA_API_ENDPOINT, json=payload, timeout=60)  # 设置 60 秒超时
            if response.status_code == 404:
                print(f"404 错误: {response.text}")
                time.sleep(3)
                continue
            response.raise_for_status()
            result = response.json()
            generated_content = result.get("response", "")
            
            # 严苛的响应校验
            if not generated_content.strip():
                time.sleep(3)
                continue
            
            if len(generated_content) < 200:
                time.sleep(3)
                continue
            
            # 检查禁止词汇
            contains_forbidden = False
            for word in FORBIDDEN_WORDS:
                if word.lower() in generated_content.lower():
                    contains_forbidden = True
                    break
            if contains_forbidden:
                time.sleep(3)
                continue
            
            # 检查占位符
            if contains_placeholders(generated_content):
                time.sleep(3)
                continue
            
            # 验证通过
            return generated_content
            
        except requests.exceptions.Timeout:
            print(f"请求超时 (尝试 {attempt+1}/{max_retries})，正在等待 3 秒...")
            time.sleep(3)
        except requests.exceptions.ConnectionError:
            print(f"连接错误 (尝试 {attempt+1}/{max_retries})，正在等待 3 秒...")
            time.sleep(3)
        except requests.exceptions.HTTPError as e:
            if hasattr(e, 'response'):
                error_text = e.response.text if hasattr(e.response, 'text') else 'No response text'
                if e.response.status_code == 502:
                    print(f"502 错误 (尝试 {attempt+1}/{max_retries}): {error_text}，正在等待 3 秒...")
                    time.sleep(3)
                else:
                    print(f"HTTP 错误 (尝试 {attempt+1}/{max_retries}): {e}")
                    print(f"错误响应: {error_text}")
                    time.sleep(3)
            else:
                print(f"HTTP 错误 (尝试 {attempt+1}/{max_retries}): {e}")
                time.sleep(3)
        except Exception as e:
            print(f"生成内容失败 (尝试 {attempt+1}/{max_retries}): {e}")
            time.sleep(3)
    
    # 重试次数用完，返回空
    return ""

# 重写并验证
def rewrite_and_verify(file_path, total_files):
    """重写文件并验证"""
    global processed_count
    
    # 识别语言
    lang = detect_file_language(file_path)
    
    # 提取项目信息
    project_name, keywords = extract_project_info(file_path)
    
    # 读取文件内容
    try:
        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f"[Error] 读取文件失败 {file_path}: {e}")
        return False
    
    # 生成内容
    generated_content = generate_content(content, project_name, keywords, lang)
    
    # 检查生成结果
    if not generated_content:
        print(f"[Error] 无法生成有效的内容: {file_path}")
        return False
    
    # 添加底部链接
    footer = f"\n---\n\n👉 `https://www.wangdadi.xyz/?utm_source=github_colab`\n"
    final_content = generated_content + footer
    
    # 写入文件
    try:
        with open(file_path, 'w', encoding='utf-8-sig') as f:
            f.write(final_content)
    except Exception as e:
        print(f"[Error] 写入文件失败 {file_path}: {e}")
        return False
    
    # 写入后的"回头看"验证
    try:
        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
            written_content = f.read()
        
        # 检查是否还有占位符
        if contains_placeholders(written_content):
            print(f"[Error] 写入后的文件仍然包含占位符: {file_path}")
            return False
        
        # 检查内容长度
        if len(written_content) < 500:
            print(f"[Error] 写入后的文件内容长度不足 500 字符: {file_path}")
            return False
    except Exception as e:
        print(f"[Error] 验证文件失败 {file_path}: {e}")
        return False
    
    # 更新计数
    with lock:
        processed_count += 1
        current_count = processed_count
    
    # 极简日志
    print(f"[Progress] {current_count}/{total_files} | Project: {project_name} | Lang: {lang.upper()}")
    
    return True

# 克隆仓库
def clone_repository():
    """克隆 GitHub 仓库"""
    repo_url = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git"
    repo_name = GITHUB_REPO.split('/')[-1]
    
    if os.path.exists(repo_name):
        print(f"仓库 {repo_name} 已存在，执行 git pull 更新...")
        subprocess.run(["git", "pull"], cwd=repo_name, check=True)
    else:
        print(f"克隆仓库 {GITHUB_REPO}...")
        subprocess.run(["git", "clone", repo_url], check=True)
    
    return repo_name

# 收集需要重写的文件
def collect_zombie_files(repo_path):
    """收集包含占位符的文件（全盘地毯式搜索）"""
    zombie_files = []
    scanned_folders = set()
    
    print(f"开始在 {repo_path} 中扫描...")
    
    for root, dirs, files in os.walk(repo_path):
        # 跳过隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        # 调试输出：打印正在查看的文件夹
        if root not in scanned_folders:
            print(f"[扫描] 正在查看文件夹: {root}")
            scanned_folders.add(root)
        
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                
                # 读取文件内容
                try:
                    with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
                        content = f.read()
                    
                    # 检查是否包含占位符
                    if contains_placeholders(content):
                        print(f"[发现] 僵尸文件: {file_path}")
                        zombie_files.append(file_path)
                except Exception as e:
                    print(f"[Error] 读取文件失败 {file_path}: {e}")
    
    print(f"扫描完成，共发现 {len(zombie_files)} 个僵尸文件")
    return zombie_files

# 执行 Git 提交
def git_commit_push(repo_path, count):
    """执行 Git 提交和推送（强制模式）"""
    try:
        # 暴力添加所有更改
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
        
        # 检查是否有更改
        result = subprocess.run(
            ["git", "status", "--porcelain"], 
            cwd=repo_path, 
            capture_output=True, 
            text=True
        )
        
        if result.stdout.strip():
            # 提交
            commit_message = f"Colab Soul Factory: Resurrected {count} files"
            subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_path, check=True)
            # 强制推送
            subprocess.run(["git", "push", "-f"], cwd=repo_path, check=True)
            print(f"[Git] 已强制提交并推送 {count} 个文件的更改")
    except Exception as e:
        print(f"[Error] Git 操作失败: {e}")

# 主函数
def main():
    print("Colab Soul Factory 启动 - 不成功，毋宁死模式")
    
    # 验证 API 连接
    verify_api()
    
    # 等待 Ollama 服务就绪
    wait_for_ollama()
    
    # 克隆仓库
    repo_name = clone_repository()
    repo_path = os.path.join(os.getcwd(), repo_name)
    
    # 收集僵尸文件
    print("收集需要重写的文件...")
    zombie_files = collect_zombie_files(repo_path)
    total_files = len(zombie_files)
    print(f"共发现 {total_files} 个僵尸页面")
    
    if not zombie_files:
        print("没有发现需要重写的文件，任务完成！")
        return
    
    # 开始处理
    print("开始暴力重写...")
    global processed_count
    processed_count = 0
    success_count = 0
    
    # 使用线程池并发处理
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # 提交所有任务
        future_to_file = {executor.submit(rewrite_and_verify, file_path, total_files): file_path for file_path in zombie_files}
        
        # 处理结果
        for future in tqdm(concurrent.futures.as_completed(future_to_file), total=total_files, desc="处理进度"):
            file_path = future_to_file[future]
            try:
                if future.result():
                    success_count += 1
                    
                    # 每成功处理 10 个文件，执行一次 Git 操作
                    if success_count % 10 == 0:
                        git_commit_push(repo_path, success_count)
            except Exception as e:
                print(f"[Error] 处理文件失败 {file_path}: {e}")
    
    # 最后一次提交
    if success_count > 0 and success_count % 10 != 0:
        git_commit_push(repo_path, success_count)
    
    print("\n处理完成！")
    print(f"成功重写: {success_count}")
    print(f"总处理: {total_files}")

if __name__ == "__main__":
    main()
