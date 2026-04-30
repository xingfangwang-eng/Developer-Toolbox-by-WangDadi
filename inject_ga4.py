#!/usr/bin/env python3
import os
import re
from pathlib import Path

GA4_CODE = """
<script async src="https://www.googletagmanager.com/gtag/js?id=G-WC4677QJMF"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-WC4677QJMF', {
    'custom_map': {
      'dimension1': 'project_name'
    },
    'project_name': '{project_name}'
  });
</script>
"""

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

def inject_ga4():
    md_files = list(BASE_DIR.rglob('*.md'))
    print(f"📊 Found {len(md_files)} markdown files")

    injected = 0
    skipped = 0
    errors = 0

    for i, file_path in enumerate(md_files):
        if i % 500 == 0:
            print(f"Progress: {i}/{len(md_files)} - Injected: {injected}, Skipped: {skipped}, Errors: {errors}")

        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()

            if has_ga4_code(content):
                skipped += 1
                continue

            project_name = get_project_name(file_path)
            ga4_code = GA4_CODE.format(project_name=project_name)

            new_content = content.rstrip() + '\n\n' + ga4_code

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            injected += 1

        except Exception as e:
            errors += 1
            if errors < 10:
                print(f"❌ Error processing {file_path}: {e}")

    print(f"\n{'='*60}")
    print(f"✅ Injected: {injected} files")
    print(f"⏭️ Skipped: {skipped} files")
    print(f"❌ Errors: {errors} files")
    print(f"📊 Total: {injected + skipped + errors} files")
    print(f"{'='*60}")

if __name__ == '__main__':
    inject_ga4()