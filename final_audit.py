#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终全量审计脚本
检查点 A: 是否包含占位符
检查点 B: 是否包含 Colab 链接
"""

import os
import re

ROOT_DIR = r"E:\Developer-Toolbox-by-WangDadi"

# 检查点 A: 占位符关键词
ZOMBIE_KEYWORDS = [
    'Describe feature',
    '説明する',
    '機能説明する',
    '功能点一',
    '功能点二',
    'feature 1',
    'feature 2',
    '功能1',
    '功能2'
]

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

def audit_file(file_path):
    """审计单个文件"""
    issues = []

    try:
        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
            content = f.read()

        # 检查点 A: 占位符检测
        for keyword in ZOMBIE_KEYWORDS:
            if keyword in content:
                issues.append(f"占位符: '{keyword}'")

        # 检查点 B: Colab 链接检测
        if 'colab.research.google.com' not in content:
            issues.append("缺少 Colab 链接")

    except Exception as e:
        issues.append(f"读取失败: {e}")

    return issues

def main():
    print("=" * 70)
    print("最终全量审计 - 双检查点验证")
    print("=" * 70)

    md_files = find_markdown_files(ROOT_DIR)
    print(f"扫描文件总数: {len(md_files)}")
    print("=" * 70)

    zombie_files = []  # 检查点 A: 占位符文件
    no_colab_files = []  # 检查点 B: 无 Colab 链接文件
    clean_files = []  # 双达标文件

    for i, file_path in enumerate(md_files):
        issues = audit_file(file_path)

        if any("占位符" in issue for issue in issues):
            zombie_files.append(file_path)
        if any("缺少 Colab" in issue for issue in issues):
            no_colab_files.append(file_path)
        if not issues:
            clean_files.append(file_path)

        if (i + 1) % 1000 == 0:
            print(f"已审计: {i + 1}/{len(md_files)} | 占位符: {len(zombie_files)} | 无Colab: {len(no_colab_files)}")

    print("\n" + "=" * 70)
    print("审计报告")
    print("=" * 70)
    print(f"📊 总文件数: {len(md_files)}")
    print(f"✅ 双达标: {len(clean_files)}")
    print(f"☠️ 含占位符: {len(zombie_files)}")
    print(f"🔗 缺 Colab: {len(no_colab_files)}")

    if zombie_files:
        print("\n" + "=" * 70)
        print(f"☠️ 检查点 A 失败 - 仍有 {len(zombie_files)} 个文件包含占位符:")
        print("=" * 70)
        for f in zombie_files[:50]:
            print(f"  ☠️ {f}")
        if len(zombie_files) > 50:
            print(f"  ... 还有 {len(zombie_files) - 50} 个")

    if no_colab_files:
        print("\n" + "=" * 70)
        print(f"🔗 检查点 B 失败 - 仍有 {len(no_colab_files)} 个文件缺少 Colab 链接:")
        print("=" * 70)
        for f in no_colab_files[:50]:
            print(f"  🔗 {f}")
        if len(no_colab_files) > 50:
            print(f"  ... 还有 {len(no_colab_files) - 50} 个")

    if not zombie_files and not no_colab_files:
        print("\n🎉 所有文件双达标！审计通过！")

    print("=" * 70)

if __name__ == "__main__":
    main()