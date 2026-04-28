#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Colab Injector - 云端手术室入口全量挂载脚本
统一注入 Google Colab 在线演示入口和资源链接
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
        'title': 'Verwandte Ressourcen',
        'quick_start': 'Schnellstart',
        'demo_text': 'Online-Demo in Google Colab ausführen',
        'demo_link': '🏥 Online-Demo in Google Colab ausführen',
        'preview_note': 'KI-gestützte Echtzeit-Vorschau der Tool-Effekte'
    },
    'ja': {
        'title': '関連リソース',
        'quick_start': 'クイックスタート',
        'demo_text': 'Google Colab でオンラインデモを実行する',
        'demo_link': '🏥 Google Colab でオンラインデモを実行する',
        'preview_note': 'AI によるツール効果のリアルタイムプレビュー'
    },
    'es': {
        'title': 'Recursos relacionados',
        'quick_start': 'Inicio rápido',
        'demo_text': 'Ejecutar demostración en línea en Google Colab',
        'demo_link': '🏥 Ejecutar demostración en línea en Google Colab',
        'preview_note': 'Vista previa en tiempo real de los efectos de la herramienta con IA'
    },
    'en': {
        'title': 'Related Resources',
        'quick_start': 'Quick Start',
        'demo_text': 'Run Online Demo in Google Colab',
        'demo_link': '🏥 Run Online Demo in Google Colab',
        'preview_note': 'Real-time AI preview of tool effects'
    }
}

def detect_language(file_path):
    """根据路径检测语言"""
    path_lower = file_path.lower()
    # 同时支持正斜杠和反斜杠路径
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
    """处理单个文件（强制缝合版）"""
    try:
        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
            content = f.read()
        
        # 【去重检查】如果已包含 Colab 链接，跳过
        if 'colab.research.google.com' in content:
            return False, "已包含 Colab 链接，跳过"
        
        lang = detect_language(file_path)
        config = LANG_CONFIG[lang]
        link_section = generate_link_section(file_path)
        new_content = content
        
        # 策略 1: 模糊匹配资源相关标题（二级或三级）
        resource_keywords = ['Resources', 'Ressourcen', 'Recursos', 'リソース']
        resource_pattern = '|'.join(resource_keywords)
        # 匹配 ## 或 ### 后面跟包含资源关键词的标题
        resource_regex = re.compile(rf'(#{2,3}\s+[^\n]*?({resource_pattern})[^\n]*)\n', re.IGNORECASE)
        resource_match = resource_regex.search(content)
        
        if resource_match:
            # 在资源标题后插入链接组，替换原有内容直到下一个标题
            title_text = resource_match.group(1)
            new_content = re.sub(
                rf'({re.escape(title_text)})\n[\s\S]*?(?=\n#{2,3}\s|$)',
                rf'\1\n\n{link_section}',
                content
            )
        else:
            # 策略 2: 暴力兜底 - 寻找 Navigation 标题
            nav_regex = re.compile(r'(\n##\s*Navigation\n)', re.IGNORECASE)
            nav_match = nav_regex.search(content)
            
            if nav_match:
                # 在 Navigation 上方插入链接组
                new_content = nav_regex.sub(rf'\n{link_section}\1', content)
            else:
                # 策略 3: 二次审计 - 追加到文件末尾
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
        # 跳过 .git 目录
        if '.git' in dirpath:
            continue
        for filename in filenames:
            if filename.endswith('.md'):
                md_files.append(os.path.join(dirpath, filename))
    return md_files

def main():
    print("=" * 60)
    print("Colab Injector - 云端手术室入口挂载")
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
            print(f"✅ [{success_count}] {os.path.basename(file_path)}")
        elif "已包含 Colab 链接" in msg or "未找到" in msg or "未变化" in msg:
            skipped_count += 1
        else:
            failed_count += 1
            print(f"❌ [{failed_count}] {os.path.basename(file_path)} - {msg}")
        
        if success_count % 50 == 0 and success_count > 0:
            print(f"\n📊 进度: 成功 {success_count} | 跳过 {skipped_count} | 失败 {failed_count}")
    
    print("\n" + "=" * 60)
    print("任务完成！")
    print(f"✅ 成功注入: {success_count} 个文件")
    print(f"⏭️ 跳过: {skipped_count} 个文件")
    print(f"❌ 失败: {failed_count} 个文件")
    print("=" * 60)
    
    # 展示一个德语文件的示例
    print("\n📋 德语版示例 (focusinbox):")
    de_example = os.path.join(ROOT_DIR, 'focusinbox', 'manual', 'de', 'FOC_001.md')
    if os.path.exists(de_example):
        with open(de_example, 'r', encoding='utf-8-sig', errors='replace') as f:
            content = f.read()
            # 找到 Verwandte Ressourcen 部分
            start = content.find('## Verwandte Ressourcen')
            if start != -1:
                # 取后面 1000 字符
                end = min(start + 1000, len(content))
                print(content[start:end])
    else:
        print("⚠️ focusinbox 德语文件未找到")

if __name__ == "__main__":
    main()