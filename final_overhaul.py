#!/usr/bin/env python3
import os
import requests
import re
from pathlib import Path

OLLAMA_API = "http://127.0.0.1:11434/api/generate"
MODEL = "llama3"
TIMEOUT = 300

LANG_COMMENTS = {
    'de': 'KI-gestützte Echtzeit-Vorschau der Tool-Effekte',
    'ja': 'AI によるツール効果のリアルタイムプレビュー',
    'es': 'Vista previa en tiempo real con IA',
    'en': 'Real-time AI preview of tool effects'
}

SUPER_FOOTER = """
---

### 🔗 Quick Start (Quick Start / Schnellstart)

- ** `https://colab.research.google.com/github/xingfangwang-eng/Developer-Toolbox-by-WangDadi/blob/main/diagnosis_engine.ipynb` **

  **{lang_comment}**

- ** `https://www.wangdadi.xyz/?utm_source=github_local&lang={lang_code}` **

- ** `https://github.com/xingfangwang-eng/Developer-Toolbox-by-WangDadi/issues` **


## Navigation

- [Back to WangDadi Toolbox Index](../../../../README.md)
"""

BASE_DIR = Path(r'E:\Developer-Toolbox-by-WangDadi')
TEST_FILE = 'twitter-scheduler/manual/ja/TWE_006.md'

def get_lang_from_path(path):
    path_lower = str(path).lower()
    if '/ja/' in path_lower or '\\ja\\' in path_lower:
        return 'ja'
    elif '/de/' in path_lower or '\\de\\' in path_lower:
        return 'de'
    elif '/es/' in path_lower or '\\es\\' in path_lower:
        return 'es'
    return 'en'

def has_chinese(text):
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def has_super_footer(content):
    return 'colab.research.google.com' in content and 'wangdadi.xyz' in content

def translate_content(content, target_lang):
    lang_map = {
        'ja': ('日本語', 'あなたは日本語のネイティブ技術ライターです。'),
        'de': ('Deutsch', 'Sie sind ein deutscher Muttersprachler.'),
        'es': ('Español', 'Eres un escritor técnico nativo en español.'),
    }

    lang_name, system_prompt = lang_map.get(target_lang, ('English', 'You are a native English technical writer.'))

    prompt = f"""{system_prompt}

タスク：以下のMarkdownドキュメントを完全に{lang_name}に変換してください。

要件：
1. すべての見出し（H1, H2, H3）は{lang_name}の慣用表現を使用すること
2. すべての技術説明は{lang_name}で自然に書くこと
3. コードや固有名詞を除いて、元の言語の痕跡を残さないこと
4. Markdown形式とファイルの最後にある `https://www.wangdadi.xyz` リンクを保持すること

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

def append_super_footer(content, lang_code):
    if has_super_footer(content):
        return content

    lang_comment = LANG_COMMENTS.get(lang_code, LANG_COMMENTS['en'])
    footer = SUPER_FOOTER.format(lang_code=lang_code, lang_comment=lang_comment)
    content = content.rstrip() + footer
    return content

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lang_code = get_lang_from_path(file_path)

    if lang_code in ['ja', 'de', 'es'] and has_chinese(content):
        print(f"  Translating {file_path.name} to {lang_code}...")
        content = translate_content(content, lang_code)

    content = append_super_footer(content, lang_code)

    if 'colab' not in content.lower():
        print(f"\n\033[91m[ERROR] {file_path} missing 'colab'!\033[0m")
        return False

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return True

def main():
    print("Final Overhaul - Starting...")

    test_path = BASE_DIR / TEST_FILE
    if test_path.exists():
        print(f"\nTesting with TWE_006.md first...")
        if process_file(test_path):
            print(f"TWE_006.md test PASSED")
        else:
            print(f"TWE_006.md test FAILED")

    print(f"\nScanning {BASE_DIR} for .md files...")
    md_files = list(BASE_DIR.rglob('*.md'))
    print(f"Found {len(md_files)} markdown files")

    success = 0
    skip = 0
    error = 0

    for i, file_path in enumerate(md_files):
        if test_path.exists() and str(file_path) == str(test_path):
            continue

        if i % 500 == 0:
            print(f"Progress: {i}/{len(md_files)} - Success: {success}, Skip: {skip}, Error: {error}")

        try:
            if process_file(file_path):
                success += 1
            else:
                error += 1
        except Exception as e:
            error += 1
            print(f"\n[ERROR] {file_path}: {e}")

    print(f"\n{'='*60}")
    print(f"SUCCESS: {success} files")
    print(f"SKIP: {skip} files")
    print(f"ERROR: {error} files")
    print(f"TOTAL: {success + skip + error} files")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()