#!/usr/bin/env python3
import os
import re
from pathlib import Path

LANG_COMMENTS = {
    'de': 'KI-gestützte Echtzeit-Vorschau der Tool-Effekte',
    'ja': 'AI によるツール効果のリアルタイムプレビュー',
    'es': 'Vista previa en tiempo real con IA',
    'en': 'Real-time AI preview of tool effects'
}

FOOTER_TEMPLATE = """
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
TEST_FILE = 'twitter-scheduler/manual/en/TWE_027.md'

def get_lang_from_path(path):
    path_lower = str(path).lower()
    if '/ja/' in path_lower or '\\ja\\' in path_lower:
        return 'ja'
    elif '/de/' in path_lower or '\\de\\' in path_lower:
        return 'de'
    elif '/es/' in path_lower or '\\es\\' in path_lower:
        return 'es'
    return 'en'

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    original_size = len(''.join(lines))
    new_lines = []
    found_wangdadi = False
    truncate_idx = -1

    for i, line in enumerate(lines):
        if 'wangdadi.xyz' in line.lower():
            found_wangdadi = True
            idx = i - 1
            while idx >= 0 and '---' in lines[idx].strip():
                idx -= 1
            truncate_idx = idx + 1
            break

    if not found_wangdadi:
        for i, line in enumerate(lines):
            if line.strip().startswith('## Navigation') or line.strip().startswith('## navigation'):
                truncate_idx = i
                break

    if truncate_idx >= 0:
        new_lines = lines[:truncate_idx]
    else:
        new_lines = lines

    lang_code = get_lang_from_path(file_path)
    lang_comment = LANG_COMMENTS.get(lang_code, LANG_COMMENTS['en'])

    footer = FOOTER_TEMPLATE.format(lang_code=lang_code, lang_comment=lang_comment)
    new_content = ''.join(new_lines) + footer

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    if 'colab' not in new_content.lower():
        print(f"\n\033[91m❌ ERROR: {file_path} missing 'colab' string!\033[0m")
        return False

    return True

def main():
    print("🚀 Nuclear Footer Overwriter - Starting...")

    test_path = BASE_DIR / TEST_FILE
    if test_path.exists():
        print(f"\n🔧 Testing with TWE_027.md first...")
        success = process_file(test_path)
        if success:
            print(f"✅ TWE_027.md test PASSED - proceeding with full run")
        else:
            print(f"❌ TWE_027.md test FAILED - aborting!")
            return

    print(f"\n📁 Scanning {BASE_DIR} for .md files...")
    md_files = list(BASE_DIR.rglob('*.md'))
    print(f"📊 Found {len(md_files)} markdown files")

    success_count = 0
    skip_count = 0
    error_count = 0

    for i, file_path in enumerate(md_files):
        if test_path.exists() and str(file_path) == str(test_path):
            continue

        if i % 500 == 0:
            print(f"Progress: {i}/{len(md_files)} - Success: {success_count}, Skip: {skip_count}, Error: {error_count}")

        try:
            if process_file(file_path):
                success_count += 1
            else:
                error_count += 1
        except Exception as e:
            error_count += 1
            print(f"\n❌ Error processing {file_path}: {e}")

    print(f"\n{'='*60}")
    print(f"✅ SUCCESS: {success_count} files")
    print(f"⏭️ SKIP: {skip_count} files")
    print(f"❌ ERROR: {error_count} files")
    print(f"📊 TOTAL: {success_count + skip_count + error_count} files")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()