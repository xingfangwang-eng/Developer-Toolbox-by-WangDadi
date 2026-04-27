#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Colab Zombie Killer - 0 成本大拯救
在 Google Colab 环境中批量处理包含占位符的 Markdown 文件
"""

import os
import re
import time
import requests
import subprocess
from tqdm import tqdm

# 配置
GITHUB_REPO = "your-github-username/your-repo-name"  # 替换为你的仓库
GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"  # 在 Colab 中设置环境变量
OLLAMA_API_ENDPOINT = "http://localhost:11434/api/generate"
MODEL = "qwen2:1.5b"  # Colab 中安装的模型

# 占位符模式
PLACEHOLDER_PATTERNS = [
    r'Describe feature',
    r'Step 1',
    r'Practice 1',
    r'Beschreiben Funktion',
    r'Schritt 1',
    r'説明する',
    r'ステップ 1',
    r'Describir función',
    r'Paso 1'
]

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
        return "Du bist ein führender deutscher IT-Architekt. Schreibe ausschließlich auf Deutsch."
    elif lang == "ja":
        return "あなたは日本の経験豊富なソフトウェアエンジニアです。完全に日本語で書いてください。"
    elif lang == "es":
        return "Eres un experto técnico latinoamericano. Escribe exclusivamente en español."
    else:  # en
        return "You are a senior Silicon Valley DevOps engineer. Write exclusively in English."

# 生成内容
def generate_content(content, project_name, keywords, lang):
    """调用 Ollama 生成内容（无限重试）"""
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
    
    attempt = 0
    while True:
        attempt += 1
        try:
            response = session.post(OLLAMA_API_ENDPOINT, json=payload, timeout=180)
            response.raise_for_status()
            result = response.json()
            generated_content = result.get("response", "")
            
            # 检查是否为空
            if generated_content.strip():
                return generated_content
            else:
                print(f"生成内容为空 (尝试 {attempt})，正在等待 5 秒...")
                time.sleep(5)
        except requests.exceptions.ConnectionError:
            print(f"连接错误 (尝试 {attempt})，正在等待 5 秒...")
            time.sleep(5)
        except requests.exceptions.HTTPError as e:
            if hasattr(e, 'response') and e.response.status_code == 502:
                print(f"502 错误 (尝试 {attempt})，正在等待 5 秒...")
                time.sleep(5)
            else:
                print(f"HTTP 错误 (尝试 {attempt}): {e}")
                time.sleep(5)
        except Exception as e:
            print(f"生成内容失败 (尝试 {attempt}): {e}")
            time.sleep(5)

# 质量检查
def check_quality(content, lang):
    """检查内容质量（严格模式）"""
    # 检查长度
    if len(content) < 500:
        return False, f"内容长度不足 500 字符，当前长度: {len(content)}"
    
    # 检查占位符词汇
    forbidden_words = [
        'Describe', 'feature', 'Beschreiben', 'Funktion', 'Schritt',
        '説明する', 'ステップ', 'Describir', 'función', 'Paso'
    ]
    
    for word in forbidden_words:
        if word.lower() in content.lower():
            return False, f"内容包含禁止词汇: {word}"
    
    # 检查原始占位符模式
    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            return False, "内容仍包含占位符"
    
    return True, "质量检查通过"

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

# 收集僵尸文件
def collect_zombie_files(repo_path):
    """收集包含占位符的文件"""
    zombie_files = []
    
    for root, dirs, files in os.walk(repo_path):
        # 跳过隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                
                # 读取文件内容
                try:
                    with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
                        content = f.read()
                    
                    # 检查是否包含占位符
                    for pattern in PLACEHOLDER_PATTERNS:
                        if re.search(pattern, content, re.IGNORECASE):
                            zombie_files.append(file_path)
                            break
                except Exception as e:
                    print(f"读取文件失败 {file_path}: {e}")
    
    return zombie_files

# 处理单个文件
def process_file(file_path):
    """处理单个文件（强制模式）"""
    # 识别语言
    lang = detect_file_language(file_path)
    
    # 读取文件内容
    try:
        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f"读取文件失败 {file_path}: {e}")
        return False
    
    # 提取项目信息
    project_name, keywords = extract_project_info(file_path)
    
    # 无限尝试直到成功
    attempt = 0
    while True:
        attempt += 1
        print(f"处理文件 {file_path} (尝试 {attempt})...")
        
        # 生成内容
        generated_content = generate_content(content, project_name, keywords, lang)
        
        # 实时预览前 50 个字
        preview = generated_content[:50] + "..." if len(generated_content) > 50 else generated_content
        print(f"生成预览: {preview}")
        
        # 质量检查
        is_valid, reason = check_quality(generated_content, lang)
        if is_valid:
            # 添加底部链接
            footer = f"\n---\n\n👉 `https://www.wangdadi.xyz/?utm_source=github_colab`\n"
            final_content = generated_content + footer
            
            # 写入文件
            try:
                with open(file_path, 'w', encoding='utf-8-sig') as f:
                    f.write(final_content)
                print(f"文件处理成功: {file_path}")
                return True
            except Exception as e:
                print(f"写入文件失败 {file_path}: {e}")
                time.sleep(5)
                continue
        else:
            print(f"质量检查失败 (尝试 {attempt}): {reason}")
            time.sleep(5)
            continue

# 执行 Git 提交
def git_commit_push(repo_path, processed_count):
    """执行 Git 提交和推送（暴力模式）"""
    try:
        # 暴力添加所有更改
        print("执行 git add . 强制添加所有更改...")
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
            commit_message = f"Colab Zombie Killer: Processed {processed_count} files"
            print(f"执行 git commit -m '{commit_message}'...")
            subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_path, check=True)
            # 推送
            print("执行 git push...")
            subprocess.run(["git", "push"], cwd=repo_path, check=True)
            print(f"已提交并推送 {processed_count} 个文件的更改")
        else:
            print("没有更改需要提交")
    except Exception as e:
        print(f"Git 操作失败: {e}")

# 主函数
def main():
    print("Colab Zombie Killer 启动...")
    
    # 克隆仓库
    repo_name = clone_repository()
    repo_path = os.path.join(os.getcwd(), repo_name)
    
    # 收集僵尸文件
    print("收集僵尸文件...")
    zombie_files = collect_zombie_files(repo_path)
    print(f"共发现 {len(zombie_files)} 个僵尸页面")
    
    # 开始处理
    print("开始处理...")
    success_count = 0
    failure_count = 0
    processed_since_last_commit = 0
    
    for file_path in tqdm(zombie_files, desc="处理进度"):
        if process_file(file_path):
            success_count += 1
            processed_since_last_commit += 1
        else:
            failure_count += 1
        
        # 每处理 100 个文件提交一次
        if processed_since_last_commit >= 100:
            git_commit_push(repo_path, processed_since_last_commit)
            processed_since_last_commit = 0
        
        # 避免过度请求
        time.sleep(1)
    
    # 最后一次提交
    if processed_since_last_commit > 0:
        git_commit_push(repo_path, processed_since_last_commit)
    
    print("\n处理完成！")
    print(f"成功: {success_count}")
    print(f"失败: {failure_count}")
    print(f"总处理: {success_count + failure_count}")

if __name__ == "__main__":
    main()
