#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
审计脚本 - 检测僵尸页面
地毯式搜索所有 .md 文件，统计僵尸页面数量
"""

import os
import re
from collections import defaultdict

# 占位符关键词
ZOMBIE_KEYWORDS = [
    'Describe feature', 'Step 1', 'Practice 1',
    'Beschreiben', 'Schritt', 'Paso', '機能',
    '説明する', 'ステップ', 'Describir', 'función'
]

# 语言目录
LANG_DIRS = ['de', 'es', 'ja']

def is_zombie(content):
    """检测内容是否包含占位符"""
    content_lower = content.lower()
    for keyword in ZOMBIE_KEYWORDS:
        if keyword.lower() in content_lower:
            return True
    return False

def detect_language(file_path):
    """检测文件语言"""
    for lang in LANG_DIRS:
        if f'/{lang}/' in file_path.replace('\\', '/'):
            return lang.upper()
    return 'EN'

def audit_repository(root_path):
    """审计仓库"""
    stats = {
        'total': 0,
        'zombie': 0,
        'soul': 0,
        'by_lang': defaultdict(lambda: {'total': 0, 'zombie': 0, 'soul': 0})
    }
    zombie_files = []
    
    print(f"开始审计: {root_path}")
    print("=" * 60)
    
    for root, dirs, files in os.walk(root_path):
        # 跳过隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                stats['total'] += 1
                
                # 检测语言
                lang = detect_language(file_path)
                stats['by_lang'][lang]['total'] += 1
                
                try:
                    with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
                        content = f.read()
                    
                    if is_zombie(content):
                        stats['zombie'] += 1
                        stats['by_lang'][lang]['zombie'] += 1
                        zombie_files.append(file_path)
                    else:
                        stats['soul'] += 1
                        stats['by_lang'][lang]['soul'] += 1
                except Exception as e:
                    print(f"[Error] 读取失败: {file_path} - {e}")
    
    return stats, zombie_files

def print_report(stats, zombie_files):
    """打印审计报告"""
    print("\n" + "=" * 60)
    print("审计报告")
    print("=" * 60)
    
    print(f"\n📊 总体统计:")
    print(f"   总文件数: {stats['total']}")
    print(f"   🧟 僵尸页面: {stats['zombie']}")
    print(f"   ✅ 灵魂页面: {stats['soul']}")
    
    if stats['total'] > 0:
        soul_rate = (stats['soul'] / stats['total']) * 100
        print(f"   灵魂率: {soul_rate:.2f}%")
    
    print(f"\n📈 按语言统计:")
    for lang in sorted(stats['by_lang'].keys()):
        lang_stats = stats['by_lang'][lang]
        print(f"   {lang}: 总计 {lang_stats['total']} | 僵尸 {lang_stats['zombie']} | 灵魂 {lang_stats['soul']}")
    
    if zombie_files:
        print(f"\n🧟 前 10 个僵尸文件:")
        for i, file_path in enumerate(zombie_files[:10], 1):
            rel_path = os.path.relpath(file_path)
            print(f"   {i}. {rel_path}")
        
        if len(zombie_files) > 10:
            print(f"   ... 还有 {len(zombie_files) - 10} 个僵尸文件")
    
    print("\n" + "=" * 60)

def main():
    # 获取当前目录
    root_path = os.getcwd()
    
    # 执行审计
    stats, zombie_files = audit_repository(root_path)
    
    # 打印报告
    print_report(stats, zombie_files)
    
    # 保存僵尸文件列表
    if zombie_files:
        with open('zombie_files.txt', 'w', encoding='utf-8') as f:
            for file_path in zombie_files:
                f.write(f"{file_path}\n")
        print(f"\n✅ 僵尸文件列表已保存到: zombie_files.txt")

if __name__ == "__main__":
    main()
