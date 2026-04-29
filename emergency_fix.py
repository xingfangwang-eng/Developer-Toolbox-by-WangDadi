#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
紧急修复脚本 - 处理审计发现的不达标文件
"""

import os
import re

ROOT_DIR = r"E:\Developer-Toolbox-by-WangDadi"

COLAB_URL = "https://colab.research.google.com/github/xingfangwang-eng/Developer-Toolbox-by-WangDadi/blob/main/diagnosis_engine.ipynb"
WANGDADI_URL = "https://www.wangdadi.xyz/?utm_source=github_local"
ISSUES_URL = "https://github.com/xingfangwang-eng/Developer-Toolbox-by-WangDadi/issues"

LANG_CONFIG = {
    'de': {
        'quick_start': 'Schnellstart',
        'demo_link': '🏥 Online-Demo in Google Colab ausführen',
        'preview_note': 'KI-gestützte Echtzeit-Vorschau der Tool-Effekte'
    },
    'ja': {
        'quick_start': 'クイックスタート',
        'demo_link': '🏥 Google Colab でオンラインデモを実行する',
        'preview_note': 'AI によるツール効果のリアルタイムプレビュー'
    },
    'es': {
        'quick_start': 'Inicio rápido',
        'demo_link': '🏥 Ejecutar demostración en línea en Google Colab',
        'preview_note': 'Vista previa en tiempo real de los efectos de la herramienta con IA'
    },
    'en': {
        'quick_start': 'Quick Start',
        'demo_link': '🏥 Run Online Demo in Google Colab',
        'preview_note': 'Real-time AI preview of tool effects'
    }
}

def detect_language(file_path):
    path_lower = file_path.lower()
    if '/de/' in path_lower or '\\de\\' in path_lower:
        return 'de'
    elif '/ja/' in path_lower or '\\ja\\' in path_lower:
        return 'ja'
    elif '/es/' in path_lower or '\\es\\' in path_lower:
        return 'es'
    return 'en'

def generate_link_section(file_path):
    lang = detect_language(file_path)
    config = LANG_CONFIG[lang]
    return f"""### 🔗 {config['quick_start']} ({LANG_CONFIG['en']['quick_start']})

- **[{config['demo_link']}]({COLAB_URL})**  <-- *{config['preview_note']}*

- ** `{WANGDADI_URL}` **

- ** `{ISSUES_URL}` **

"""

def fix_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
            content = f.read()

        modified = False

        # 修复占位符 - 强制删除包含占位符的行
        placeholder_patterns = [
            r'.*機能を説明します.*\n',
            r'.*Describe feature.*\n',
            r'.*説明する.*\n',
            r'.*Feature \d+.*\n',
            r'.*機能\d+.*\n',
        ]

        for pattern in placeholder_patterns:
            new_content = re.sub(pattern, '', content, flags=re.IGNORECASE)
            if new_content != content:
                content = new_content
                modified = True

        # 如果不包含 Colab 链接，强制插入
        if 'colab.research.google.com' not in content:
            link_section = generate_link_section(file_path)

            # 尝试在 Navigation 上方插入
            nav_match = re.search(r'(\n##\s*Navigation\n)', content, re.IGNORECASE)
            if nav_match:
                content = re.sub(r'(\n##\s*Navigation\n)', r'\n' + link_section + r'\1', content)
            else:
                # 直接追加到末尾
                content = content.rstrip() + '\n\n' + link_section
            modified = True

        if modified:
            with open(file_path, 'w', encoding='utf-8-sig') as f:
                f.write(content)
            return True

        return False

    except Exception as e:
        print(f"  错误: {e}")
        return False

# 手动指定需要修复的文件列表（基于审计结果）
FILES_TO_FIX = []

# AGE_xxx 日语文件
for i in range(1, 20):
    FILES_TO_FIX.append(f"agents-clean\\manual\\ja\\AGE_{i:03d}.md")

# SLO_xxx 日语文件
for i in range(1, 35):
    FILES_TO_FIX.append(f"slopkiller\\manual\\ja\\SLO_{i:03d}.md")

# SME_xxx 文件
for i in [1,2,5,6,9,10,12,13,16,18,19,20,21,22,23,25,26,29]:
    FILES_TO_FIX.append(f"smesurvivalai\\manual\\SME_{i:03d}.md")
for i in range(1, 20):
    FILES_TO_FIX.append(f"smesurvivalai\\manual\\de\\SME_{i:03d}.md")

def main():
    print("=" * 60)
    print("紧急修复脚本")
    print("=" * 60)

    fixed_count = 0
    for rel_path in FILES_TO_FIX:
        full_path = os.path.join(ROOT_DIR, rel_path)
        if os.path.exists(full_path):
            if fix_file(full_path):
                print(f"✅ 修复: {rel_path}")
                fixed_count += 1
            else:
                print(f"⏭️ 无需修复: {rel_path}")

    print(f"\n修复完成: {fixed_count} 个文件")

if __name__ == "__main__":
    main()