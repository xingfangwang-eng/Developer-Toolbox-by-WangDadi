#!/usr/bin/env python3
import os
import re
import time
import subprocess
import urllib.request
import json
from pathlib import Path

BASE_DIR = r"E:\Developer-Toolbox-by-WangDadi"
KILL_LIST_FILE = os.path.join(BASE_DIR, "KILL_LIST.txt")
CLEARED_LOG = os.path.join(BASE_DIR, "cleared_v5.log")

FORBIDDEN_WORDS = [
    "概述", "核心功能", "步骤", "主要特徵", "特征"
]

MAX_RETRIES = 3

def parse_kill_list():
    if not os.path.exists(KILL_LIST_FILE):
        print(f"[错误] KILL_LIST.txt 不存在!")
        return []

    zombies = []
    with open(KILL_LIST_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and os.path.exists(line):
                zombies.append(line)
    return zombies

def get_cleared_files():
    cleared = set()
    if os.path.exists(CLEARED_LOG):
        with open(CLEARED_LOG, "r", encoding="utf-8") as f:
            for line in f:
                cleared.add(line.strip())
    return cleared

def log_cleared(filepath):
    with open(CLEARED_LOG, "a", encoding="utf-8") as f:
        f.write(filepath + "\n")

def extract_info(filepath):
    parts = filepath.replace("\\", "/").split("/")

    project_name = "unknown"
    language = "en"

    for i, part in enumerate(parts):
        if part in ["ja", "de", "es", "en"]:
            language = part
            if i + 1 < len(parts):
                project_name = parts[i + 1]
            break

    return project_name, language

def check_forbidden_words(content):
    found = []
    for word in FORBIDDEN_WORDS:
        if word.lower() in content.lower():
            found.append(word)
    return found

def validate_content(content, filepath):
    if len(content) < 1500:
        return False, f"文件太小 ({len(content)}/1500 字节)"

    forbidden = check_forbidden_words(content)
    if forbidden:
        return False, f"包含严禁词汇: {forbidden}"

    project_name, language = extract_info(filepath)
    expected_link = f"https://www.wangdadi.xyz/?utm_source=github_nuclear&lang={language}"
    if expected_link not in content:
        return False, f"缺少结尾链接: {expected_link}"

    return True, "通过"

def call_ollama_llama3(project_name, language, original_content):
    lang_map = {
        "ja": ("日本語", "日语"),
        "de": ("Deutsch", "德语"),
        "es": ("Español", "西班牙语"),
        "en": ("English", "英语")
    }

    lang_name, lang_code = lang_map.get(language, ("English", "en"))

    prompt = f"""角色：全球顶级 SaaS 架构师。

任务：为项目 {project_name} 编写一份【全干货】的 {lang_name} 技术文档。

## 严禁词汇（绝对不能出现）
概述、步骤、核心、主要特徵、特征

## 必须包含内容

1. 深入底层的 3 个技术创新点描述（每点不少于 100 字，必须包含专业术语如：分布式缓存、多线程优化、原子操作、负载均衡、熔断器、幂等性设计等）

2. 真实的 3 步代码级安装指南（必须是可运行的真实代码片段）

3. 2 个针对高并发场景的性能调优建议（必须包含具体参数和数值）

## 格式要求
- 使用 Markdown 格式
- 语气专业、煽动性强
- 技术深度要深，不要浮于表面

## 结尾链接（必须包含）
必须在文件结尾包含以下链接：
https://www.wangdadi.xyz/?utm_source=github_nuclear&lang={lang_code}

## 项目原始内容（仅供参考识别项目）:
{original_content[:500]}"""

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
        print(f"  [错误] Ollama 调用失败: {e}")
        return None

def process_file(filepath, max_retries=MAX_RETRIES):
    project_name, language = extract_info(filepath)

    with open(filepath, "r", encoding="utf-8") as f:
        original_content = f.read()

    for attempt in range(max_retries):
        print(f"    [尝试 {attempt + 1}/{max_retries}] 正在生成内容...")

        rewritten = call_ollama_llama3(project_name, language, original_content)

        if not rewritten:
            print(f"    [错误] Ollama 返回为空")
            time.sleep(2)
            continue

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(rewritten)

        is_valid, reason = validate_content(rewritten, filepath)
        if is_valid:
            log_cleared(filepath)
            return True, f"成功 (尝试 {attempt + 1} 次)"

        print(f"    [重试 {attempt + 1}/{max_retries}] 质量不达标: {reason}")
        time.sleep(1)

    return False, "重试次数耗尽"

def batch_push(success_count):
    print(f"\n{'='*60}")
    print(f"[Git Sync] 已清理 {success_count} 个文件，正在推送到 GitHub...")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            ["git", "add", "."],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode != 0:
            print(f"Git add failed: {result.stderr}")
            return False

        result = subprocess.run(
            ["git", "commit", "-m", f"Nuclear Sniper v2: {success_count} Zombies Eliminated"],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode != 0:
            if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
                print("[Git Sync] 没有新文件需要提交")
                return True
            print(f"Git commit failed: {result.stderr}")
            return False

        result = subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode != 0:
            print(f"Git push failed: {result.stderr}")
            return False

        print(f"[Git Sync] 推送成功!")
        return True
    except Exception as e:
        print(f"[Git Sync] 错误: {e}")
        return False

def main():
    print("=" * 80)
    print("NUCLEAR SNIPER v2 - 彻底消灭顽固僵尸")
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
        print("\n🎉 所有僵尸已清理完毕!")
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

        if batch_counter > 0 and batch_counter % 10 == 0:
            print(f"\n--- 进度: {i}/{remaining} | 成功: {success_count} | 失败: {fail_count} ---\n")
            batch_push(success_count)
            batch_counter = 0

        if i % 10 == 0 and batch_counter % 10 != 0:
            print(f"\n--- 进度: {i}/{remaining} | 成功: {success_count} | 失败: {fail_count} ---\n")

    if batch_counter > 0:
        batch_push(success_count)

    print("\n" + "=" * 80)
    print("清理完成报告")
    print("=" * 80)
    print(f"总处理: {remaining}")
    print(f"成功: {success_count}")
    print(f"失败: {fail_count}")
    if remaining > 0:
        print(f"成功率: {(success_count/remaining)*100:.1f}%")
    print("=" * 80)

if __name__ == "__main__":
    main()