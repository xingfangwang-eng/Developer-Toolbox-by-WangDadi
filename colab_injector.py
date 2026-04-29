#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Colab Injector - 云端手术室入口全量挂载脚本
无视标题、强制缝合版 - 确保所有文件都包含 Colab 链接
"""

import os
import re

ROOT_DIR = r"E:\Developer-Toolbox-by-WangDadi"

# 链接配置
COLAB_URL = "https://colab.research.google.com/github/xingfangwang-eng/Developer-Toolbox-by-WangDadi/blob/main/diagnosis_engine.ipynb"
WANGDADI_URL = "https://www.wangdadi.xyz/?utm_source=github_local"
ISSUES_URL = "https://github.com/xingfangwang-eng/Developer-Toolbox-by-WangDadi/issues"

# 语种配置
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
    """根据路径检测语言"""
    path_lower = file_path.lower()
    if '/de/' in path_lower or '\\de\\' in path_lower:
        return 'de'
    elif '/ja/' in path_lower or '\\ja\\' in path_lower:
        return 'ja'
    elif '/es/' in path_lower or '\\es\\' in path_lower:
        return 'es'
    return 'en'

def generate_link_section(file_path):
    """生成链接组内容"""
    lang = detect_language(file_path)
    config = LANG_CONFIG[lang]

    section = f"""### 🔗 {config['quick_start']} ({LANG_CONFIG['en']['quick_start']})

- **[{config['demo_link']}]({COLAB_URL})**  <-- *{config['preview_note']}*

- ** `{WANGDADI_URL}` **

- ** `{ISSUES_URL}` **

"""
    return section

def process_file(file_path):
    """处理单个文件（无视标题、强制缝合版）"""
    try:
        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
            content = f.read()

        # 【存在性检查】如果已包含 Colab 链接，跳过
        if 'colab.research.google.com' in content:
            return False, "已包含 Colab 链接，跳过"

        lang = detect_language(file_path)
        link_section = generate_link_section(file_path)

        # 【暴力插入】寻找 ## Navigation 或 ## 导航 等关键词
        nav_patterns = [
            r'(\n##\s*Navigation\n)',
            r'(\n##\s*导航\n)',
            r'(\n##\s*Navegación\n)',
            r'(\n##\s*Verwandte\s+Ressourcen\n)',
            r'(\n##\s*関連リソース\n)',
            r'(\n##\s*Recursos\s+Relacionados\n)',
            r'(\n##\s*Related\s+Resources\n)'
        ]

        nav_regex = re.compile('|'.join(nav_patterns), re.IGNORECASE)
        nav_match = nav_regex.search(content)

        if nav_match:
            # 在 Navigation 上方插入链接组
            new_content = nav_regex.sub(r'\n' + link_section + r'\1', content)
        else:
            # 【暴力兜底】直接追加到文件最末尾
            new_content = content.rstrip() + '\n\n' + link_section

        if content == new_content:
            return False, "内容未变化"

        with open(file_path, 'w', encoding='utf-8-sig') as f:
            f.write(new_content)

        return True, "成功注入链接"

    except Exception as e:
        return False, f"处理失败: {e}"

def find_markdown_files(root_dir):
    """查找所有 Markdown 文件"""
    md_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if '.git' in dirpath:
            continue
        for filename in filenames:
            if filename.endswith('.md'):
                md_files.append(os.path.join(dirpath, filename))
    return md_files

def main():
    print("=" * 60)
    print("Colab Injector - 无视标题、强制缝合版")
    print("=" * 60)
    print(f"扫描目录: {ROOT_DIR}")
    print("=" * 60)

    md_files = find_markdown_files(ROOT_DIR)
    print(f"发现 {len(md_files)} 个 Markdown 文件")

    success_count = 0
    failed_count = 0
    skipped_count = 0

    for file_path in md_files:
        success, msg = process_file(file_path)
        if success:
            success_count += 1
            if success_count <= 10:
                print(f"✅ [{success_count}] {os.path.basename(file_path)}")
        elif "已包含 Colab 链接" in msg:
            skipped_count += 1
        else:
            failed_count += 1
            print(f"❌ [{failed_count}] {os.path.basename(file_path)} - {msg}")

        if success_count > 10 and success_count % 100 == 0:
            print(f"📊 进度: 成功 {success_count} | 跳过 {skipped_count} | 失败 {failed_count}")

    print("\n" + "=" * 60)
    print("任务完成！")
    print(f"✅ 成功注入: {success_count} 个文件")
    print(f"⏭️ 跳过: {skipped_count} 个文件")
    print(f"❌ 失败: {failed_count} 个文件")
    print(f"📊 总计: {success_count + skipped_count + failed_count} 个文件")
    print("=" * 60)

if __name__ == "__main__":
    main()