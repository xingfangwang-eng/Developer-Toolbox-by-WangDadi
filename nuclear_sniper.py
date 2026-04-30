#!/usr/bin/env python3
import os
import re
import time
import subprocess
import urllib.request
import json
from pathlib import Path

KILL_LIST = r"E:\Developer-Toolbox-by-WangDadi\KILL_LIST.txt"
CLEARED_LOG = r"E:\Developer-Toolbox-by-WangDadi\cleared_v4.log"
BASE_DIR = r"E:\Developer-Toolbox-by-WangDadi"

def parse_kill_list():
    filepaths = []
    try:
        with open(KILL_LIST, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith("原因") and not line.startswith("-"):
                    if os.path.exists(line):
                        filepaths.append(line)
    except Exception as e:
        print(f"读取 KILL_LIST.txt 失败: {e}")
    return filepaths

def get_cleared_files():
    cleared = set()
    if os.path.exists(CLEARED_LOG):
        try:
            with open(CLEARED_LOG, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        cleared.add(line.strip())
        except Exception as e:
            print(f"读取 cleared_v4.log 失败: {e}")
    return cleared

def log_cleared(filepath):
    try:
        with open(CLEARED_LOG, "a", encoding="utf-8") as f:
            f.write(f"{filepath}\n")
    except Exception as e:
        print(f"记录日志失败: {e}")

def extract_info(filepath):
    parts = Path(filepath).parts
    project_name = "unknown"
    language = "en"
    
    for i, part in enumerate(parts):
        if part == "manual" and i > 0:
            project_name = parts[i-1]
            if i + 1 < len(parts) and parts[i+1] in ["ja", "de", "es"]:
                language = parts[i+1]
            break
    
    return project_name, language

def has_chinese_chars(content):
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
    return len(chinese_pattern.findall(content)) > 0

def validate_content(content, language):
    char_count = len(content)
    if char_count < 500:
        return False, f"字数不足 ({char_count}/500)"
    
    if "colab.research.google.com" not in content:
        return False, "缺少 Colab 链接"
    
    if "utm_source=github_local" not in content:
        return False, "缺少 utm 参数"
    
    return True, "通过"

def call_ollama_llama3(project_name, language, original_content):
    prompts = {
        "ja": f"""你是一个全球顶级的 SaaS 架构师和资深技术撰稿人。
任务：彻底重写该マニュアル（手册）。
要求：
1. 这是 {project_name} 项目的日语版手册。
2. 严禁使用任何'概述'、'步骤'、'Describe'等机械化占位词。
3. 你必须【虚构】出三个非常硬核、非常具体的技术模块描述。
4. 正文字数必须超过 600 字，语气要具有极强的专业煽动性。
5. 结尾必须保留 Colab 链接，格式必须是: https://colab.research.google.com/github/.../...ipynb?utm_source=github_local
6. 使用完全自然的日语技术术语。
7. 保持原有的 Emoji 链接格式。

原始内容：
{original_content}""",
        
        "de": f"""你是一个全球顶级的 SaaS 架构师和资深技术撰稿人。
任务：彻底重写该 Handbuch（手册）。
要求：
1. 这是 {project_name} 项目的德语版手册。
2. 严禁使用任何'概述'、'步骤'、'Describe'等机械化占位词。
3. 你必须【虚构】出三个非常硬核、非常具体的技术模块描述。
4. 正文字数必须超过 600 字，语气要具有极强的专业煽动性。
5. 结尾必须保留 Colab 链接，格式必须是: https://colab.research.google.com/github/.../...ipynb?utm_source=github_local
6. 使用完全自然的德语技术术语。
7. 保持原有的 Emoji 链接格式。

原始内容：
{original_content}""",
        
        "es": f"""你是一个全球顶级的 SaaS 架构师和资深技术撰稿人。
任务：彻底重写该 manual（手册）。
要求：
1. 这是 {project_name} 项目的西班牙语版手册。
2. 严禁使用任何'概述'、'步骤'、'Describe'等机械化占位词。
3. 你必须【虚构】出三个非常硬核、非常具体的技术模块描述。
4. 正文字数必须超过 600 字，语气要具有极强的专业煽动性。
5. 结尾必须保留 Colab 链接，格式必须是: https://colab.research.google.com/github/.../...ipynb?utm_source=github_local
6. 使用完全自然的西班牙语技术术语。
7. 保持原有的 Emoji 链接格式。

原始内容：
{original_content}""",
        
        "en": f"""你是一个全球顶级的 SaaS 架构师和资深技术撰稿人。
任务：彻底重写该 manual（手册）。
要求：
1. 这是 {project_name} 项目的英文版手册。
2. 严禁使用任何'概述'、'步骤'、'Describe'等机械化占位词。
3. 你必须【虚构】出三个非常硬核、非常具体的技术模块描述。
4. 正文字数必须超过 600 字，语气要具有极强的专业煽动性。
5. 结尾必须保留 Colab 链接，格式必须是: https://colab.research.google.com/github/.../...ipynb?utm_source=github_local
6. 保持原有的 Emoji 链接格式。

原始内容：
{original_content}"""
    }
    
    prompt = prompts.get(language, prompts["en"])
    
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=180) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get("response", "")
    except Exception as e:
        print(f"Ollama 调用失败: {e}")
        return None

def process_file(filepath, max_retries=5):
    project_name, language = extract_info(filepath)
    
    for attempt in range(max_retries):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                original_content = f.read()
            
            rewritten = call_ollama_llama3(project_name, language, original_content)
            
            if not rewritten:
                print(f"  [重试 {attempt+1}/{max_retries}] Ollama 响应为空")
                time.sleep(2)
                continue
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(rewritten)
            
            is_valid, reason = validate_content(rewritten, language)
            if is_valid:
                log_cleared(filepath)
                return True, f"成功 (尝试 {attempt+1} 次)"
            else:
                print(f"  [重试 {attempt+1}/{max_retries}] 质量不达标: {reason}")
                time.sleep(2)
        
        except Exception as e:
            print(f"  [重试 {attempt+1}/{max_retries}] 处理错误: {e}")
            time.sleep(2)
    
    return False, "重试次数耗尽"

def git_add_commit_push(processed_count):
    print(f"\n{'='*60}")
    print(f"[Git Sync] 已清理 {processed_count} 个文件，正在推送到 GitHub...")
    print(f"{'='*60}")

    commands = [
        ["git", "add", "."],
        ["git", "commit", "-m", f"Nuclear Sniper: {processed_count} Zombies Eliminated"],
        ["git", "push", "origin", "main"]
    ]

    for attempt in range(3):
        try:
            for cmd in commands:
                result = subprocess.run(
                    cmd,
                    cwd=BASE_DIR,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if result.returncode != 0:
                    print(f"Git command failed: {' '.join(cmd)}")
                    print(f"Error: {result.stderr}")
                    if attempt < 2:
                        print(f"重试中... ({attempt + 1}/3)")
                        time.sleep(2)
                        break
                    else:
                        return False
            print(f"[Git Sync] 推送成功!")
            return True
        except subprocess.TimeoutExpired:
            print("Git timeout, retrying...")
        except Exception as e:
            print(f"Git error: {e}")
            if attempt >= 2:
                return False
        time.sleep(1)

    return False

def main():
    print("=" * 80)
    print("NUCLEAR SNIPER - 精准清理系统")
    print("=" * 80)
    
    all_zombies = parse_kill_list()
    cleared = get_cleared_files()
    to_process = [f for f in all_zombies if f not in cleared]
    
    total = len(all_zombies)
    remaining = len(to_process)
    print(f"总僵尸数: {total}")
    print(f"已清理: {total - remaining}")
    print(f"待清理: {remaining}")
    print("-" * 80)
    
    if remaining == 0:
        print("\n🎉 所有僵尸已清理完毕！")
        return
    
    success_count = 0
    fail_count = 0
    batch_counter = 0
    
    for i, filepath in enumerate(to_process, 1):
        project_name, language = extract_info(filepath)
        print(f"[{i}/{remaining}] 正在狙击: {os.path.basename(filepath)} ({language}/{project_name})")
        
        success, message = process_file(filepath)
        
        if success:
            success_count += 1
            batch_counter += 1
            print(f"  ✅ {message}")
        else:
            fail_count += 1
            print(f"  ❌ {message}")
        
        if batch_counter > 0 and batch_counter % 30 == 0:
            print(f"\n--- 进度: {i}/{remaining} | 成功: {success_count} | 失败: {fail_count} ---\n")
            git_add_commit_push(success_count)
            batch_counter = 0
        
        if i % 10 == 0 and batch_counter % 30 != 0:
            print(f"\n--- 进度: {i}/{remaining} | 成功: {success_count} | 失败: {fail_count} ---\n")
    
    if batch_counter > 0:
        git_add_commit_push(success_count)
    
    print("\n" + "=" * 80)
    print("清理完成报告")
    print("=" * 80)
    print(f"总处理: {remaining}")
    print(f"成功: {success_count}")
    print(f"失败: {fail_count}")
    print(f"成功率: {(success_count/remaining)*100:.1f}%")
    print("=" * 80)

if __name__ == "__main__":
    main()