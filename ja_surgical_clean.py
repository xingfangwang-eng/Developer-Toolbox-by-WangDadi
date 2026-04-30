#!/usr/bin/env python3
import os
import requests
import re
import subprocess
from pathlib import Path

OLLAMA_API = "http://127.0.0.1:11434/api/generate"
MODEL = "llama3"
TIMEOUT = 300
PUSH_INTERVAL = 30

CONTAMINATION_WORDS = ['概述', '核心功能', '快速开始', '步骤', '专家建议', '性能优化']

BASE_DIR = Path(r'E:\Developer-Toolbox-by-WangDadi')

def is_contaminated(content):
    for word in CONTAMINATION_WORDS:
        if word in content:
            return True
    return False

def rewrite_to_pure_japanese(content):
    prompt = f"""任務：以下のマニュアルから「中国語の漢字」を完全に排除し、プロフェッショナルな「純粋な日本語」でリライトしてください。

変換ルール：
- 概述 -> 概要 / イントロダクション
- 核心功能 -> 主な機能 / コア機能
- 快速开始 -> クイックスタート
- 步骤 -> ステップ / 手順
- 专家建议 -> エキスパートのアドバイス / 推奨事項

要求：技術的に正確で、日本企業が採用するような高品質なドキュメントに仕上げること。Markdown形式と底部のURLは維持すること。

ドキュメント：
{content}"""

    try:
        response = requests.post(OLLAMA_API, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "num_predict": 1024
        }, timeout=TIMEOUT)

        if response.status_code == 200:
            return response.json().get('response', content)
    except Exception as e:
        print(f"Translation error: {e}")
    return content

def git_push():
    try:
        subprocess.run(['git', 'add', '-A'], cwd=BASE_DIR, check=True)
        subprocess.run(['git', 'commit', '-m', f'🌏 JA surgical clean: batch push'], cwd=BASE_DIR, check=True)
        subprocess.run(['git', 'push'], cwd=BASE_DIR, check=True)
        print(f"   🚀 Pushed to GitHub!")
        return True
    except Exception as e:
        print(f"   ❌ Git push failed: {e}")
        return False

def main():
    print("🚀 JA Surgical Clean - Starting...")

    log_file = BASE_DIR / 'ja_cleaned_files.log'
    ja_files = list(BASE_DIR.rglob('*/ja/*.md'))

    print(f"📊 Found {len(ja_files)} Japanese markdown files")

    contaminated = []
    clean = []

    for file_path in ja_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if is_contaminated(content):
            contaminated.append(file_path)
        else:
            clean.append(file_path)

    print(f"🔍 Audit Result:")
    print(f"   Contaminated: {len(contaminated)} files")
    print(f"   Clean: {len(clean)} files")

    success = 0
    error = 0

    with open(log_file, 'w', encoding='utf-8') as log:
        log.write("JA Surgical Clean Log\n")
        log.write("=" * 60 + "\n\n")

        for i, file_path in enumerate(contaminated):
            print(f"[{i+1}/{len(contaminated)}] Processing: {file_path.name}...")

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                new_content = rewrite_to_pure_japanese(content)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                log.write(f"SUCCESS: {file_path}\n")
                success += 1
                print(f"   ✅ Done: {file_path.name}")

                if success % PUSH_INTERVAL == 0:
                    print(f"\n   📦 Reached {success} files, pushing to GitHub...")
                    git_push()

            except Exception as e:
                log.write(f"ERROR: {file_path} - {e}\n")
                error += 1
                print(f"   ❌ Error: {e}")

        if success % PUSH_INTERVAL != 0 and success > 0:
            print(f"\n   📦 Final push ({success} files)...")
            git_push()

        log.write(f"\n{'='*60}\n")
        log.write(f"Total Contaminated: {len(contaminated)}\n")
        log.write(f"Success: {success}\n")
        log.write(f"Error: {error}\n")

    print(f"\n{'='*60}")
    print(f"✅ SUCCESS: {success} files cleaned")
    print(f"❌ ERROR: {error} files")
    print(f"📝 Log: {log_file}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()