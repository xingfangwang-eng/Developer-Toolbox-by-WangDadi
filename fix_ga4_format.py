#!/usr/bin/env python3
import os
import re
from pathlib import Path

# 使用单个花括号，因为不需要转义
GA4_CODE = '''
<script async src="https://www.googletagmanager.com/gtag/js?id=G-WC4677QJMF"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-WC4677QJMF', {
    'custom_map': {
      'dimension1': 'project_name'
    },
    'project_name': 'PROJECT_NAME_PLACEHOLDER'
  });
</script>
'''

BASE_DIR = Path(r'E:\Developer-Toolbox-by-WangDadi')

def get_project_name(file_path):
    parts = file_path.parts
    for i, part in enumerate(parts):
        if part == 'manual':
            if i > 0:
                return parts[i-1]
    return 'unknown'

def has_ga4_code(content):
    return 'G-WC4677QJMF' in content

def fix_ga4_format():
    md_files = list(BASE_DIR.rglob('*.md'))
    print(f"📊 Found {len(md_files)} markdown files")

    fixed = 0
    skipped = 0

    for i, file_path in enumerate(md_files):
        if i % 500 == 0:
            print(f"Progress: {i}/{len(md_files)} - Fixed: {fixed}, Skipped: {skipped}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if '{{' not in content:
                skipped += 1
                continue

            # 将双花括号替换为单花括号
            content = content.replace('{{', '{').replace('}}', '}')

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            fixed += 1

        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")

    print(f"\n{'='*60}")
    print(f"✅ Fixed: {fixed} files")
    print(f"⏭️ Skipped: {skipped} files")
    print(f"📊 Total: {fixed + skipped} files")
    print(f"{'='*60}")

if __name__ == '__main__':
    fix_ga4_format()