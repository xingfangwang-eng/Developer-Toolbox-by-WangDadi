#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Colab Soul Factory - Gemini API 暴力重写版
使用 Gemini 1.5 Flash 实现稳定的内容生成
"""

import os
import re
import time
import subprocess
import concurrent.futures
from tqdm import tqdm
import google.generativeai as genai

# 配置
GITHUB_REPO = "xingfangwang-eng/Developer-Toolbox-by-WangDadi"
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# 检查环境变量
if not GITHUB_TOKEN:
    print("错误：请设置 GITHUB_TOKEN 环境变量")
    exit(1)

if not GEMINI_API_KEY:
    print("错误：请设置 GEMINI_API_KEY 环境变量")
    exit(1)

# Gemini API 配置
MODEL_NAME = "gemini-1.5-flash"
MAX_WORKERS = 1  # 单线程运行，严格控制请求数

# 初始化 Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    MODEL_NAME,
    system_instruction={"role": "system", "parts": ["You are a helpful assistant."]}
)

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
rate_limit_count = 0

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
    parts = file_path.split(os.sep)
    project_name = ""
    for part in parts:
        if part == "manual":
            break
        if part and not part.startswith('.'):
            project_name = part

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
    """调用 Gemini API 生成内容（严格限速）"""
    global rate_limit_count

    system_prompt = generate_system_prompt(lang)

    user_prompt = f"""直接重写 Markdown。要求：根据项目名 {project_name} 和关键词 {', '.join(keywords)}，生成地道、硬核的 {lang} 技术说明。字数 > 500。严禁输出任何废话和占位符。

{content}

IMPORTANT: Output ONLY the Markdown content. Do NOT include any introductory text. No conversational filler. Just the code.
"""

    max_retries = 10
    for attempt in range(max_retries):
        try:
            # 严格限速：每次请求前等待 4.5 秒，确保每分钟 ≤ 14 次请求
            time.sleep(4.5)

            # 构建完整的提示（包含语言指令）
            full_prompt = f"{system_prompt}\n\n{user_prompt}"

            response = model.generate_content(
                contents=[{"role": "user", "parts": [full_prompt]}],
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 2000
                },
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                ]
            )

            generated_content = response.text

            # 严苛的响应校验
            if not generated_content.strip():
                time.sleep(1)
                continue

            if len(generated_content) < 200:
                time.sleep(1)
                continue

            # 检查禁止词汇
            contains_forbidden = False
            for word in FORBIDDEN_WORDS:
                if word.lower() in generated_content.lower():
                    contains_forbidden = True
                    break
            if contains_forbidden:
                time.sleep(1)
                continue

            # 检查占位符
            if contains_placeholders(generated_content):
                time.sleep(1)
                continue

            # 验证通过，重置限流计数
            rate_limit_count = 0
            return generated_content

        except Exception as e:
            error_str = str(e).lower()
            if '429' in error_str or 'rate' in error_str or 'quota' in error_str:
                rate_limit_count += 1
                wait_time = 60 * rate_limit_count
                print(f"[Warning] 触发限流，进入深度休眠以恢复配额... (等待 {wait_time} 秒)")
                time.sleep(wait_time)
            else:
                print(f"生成内容失败 (尝试 {attempt+1}/{max_retries}): {e}")
                time.sleep(3)

    # 重试次数用完，重置计数
    rate_limit_count = 0
    return ""

# 重写并验证
def rewrite_and_verify(file_path, total_files):
    """重写文件并验证"""
    global processed_count

    lang = detect_file_language(file_path)
    project_name, keywords = extract_project_info(file_path)

    try:
        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f"[Error] 读取文件失败 {file_path}: {e}")
        return False

    generated_content = generate_content(content, project_name, keywords, lang)

    if not generated_content:
        print(f"[Error] 无法生成有效的内容: {file_path}")
        return False

    footer = f"\n---\n\n👉 `https://www.wangdadi.xyz/?utm_source=github_gemini`\n"
    final_content = generated_content + footer

    try:
        with open(file_path, 'w', encoding='utf-8-sig') as f:
            f.write(final_content)
    except Exception as e:
        print(f"[Error] 写入文件失败 {file_path}: {e}")
        return False

    # 写入后验证
    try:
        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
            written_content = f.read()

        if contains_placeholders(written_content):
            print(f"[Error] 写入后的文件仍然包含占位符: {file_path}")
            return False

        if len(written_content) < 500:
            print(f"[Error] 写入后的文件内容长度不足 500 字符: {file_path}")
            return False
    except Exception as e:
        print(f"[Error] 验证文件失败 {file_path}: {e}")
        return False

    with lock:
        processed_count += 1
        current_count = processed_count

    print(f"[Progress] {current_count}/{total_files} | Project: {project_name} | Lang: {lang.upper()}")

    return True

# 克隆仓库
def clone_repository():
    """克隆 GitHub 仓库"""
    repo_url = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git"
    repo_name = GITHUB_REPO.split('/')[-1]

    if os.path.exists('.git'):
        print(f"检测到当前目录已是 Git 仓库，跳过克隆")
        return os.getcwd()

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
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        if root not in scanned_folders:
            print(f"[扫描] 正在查看文件夹: {root}")
            scanned_folders.add(root)

        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
                        content = f.read()

                    if contains_placeholders(content):
                        print(f"[发现] 僵尸文件: {file_path}")
                        zombie_files.append(file_path)
                    else:
                        print(f"[跳过] 已完成文件: {file_path}")
                except Exception as e:
                    print(f"[Error] 读取文件失败 {file_path}: {e}")

    print(f"扫描完成，共发现 {len(zombie_files)} 个僵尸文件")
    return zombie_files

# 执行 Git 提交
def git_commit_push(repo_path, count):
    """执行 Git 提交和推送（强制模式）"""
    try:
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)

        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )

        if result.stdout.strip():
            commit_message = f"Colab Soul Factory: Resurrected {count} files"
            subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_path, check=True)
            subprocess.run(["git", "push", "-f"], cwd=repo_path, check=True)
            print(f"[Git] 已强制提交并推送 {count} 个文件的更改")
    except Exception as e:
        print(f"[Error] Git 操作失败: {e}")

# 主函数
def main():
    print("Colab Soul Factory 启动 - Gemini API 限速版")
    print(f"模型: {MODEL_NAME} | 限速: 14 RPM | 单线程")

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

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_file = {executor.submit(rewrite_and_verify, file_path, total_files): file_path for file_path in zombie_files}

        for future in tqdm(concurrent.futures.as_completed(future_to_file), total=total_files, desc="处理进度"):
            file_path = future_to_file[future]
            try:
                if future.result():
                    success_count += 1

                    if success_count % 10 == 0:
                        git_commit_push(repo_path, success_count)
            except Exception as e:
                print(f"[Error] 处理文件失败 {file_path}: {e}")

    if success_count > 0 and success_count % 10 != 0:
        git_commit_push(repo_path, success_count)

    print("\n处理完成！")
    print(f"成功重写: {success_count}")
    print(f"总处理: {total_files}")

if __name__ == "__main__":
    main()
