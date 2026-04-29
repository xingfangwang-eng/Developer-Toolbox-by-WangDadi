#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FocusInbox URL 修复脚本
- 替换错误的 focusinbox.wangdadi.xyz → focusinbox-eight.wangdadi.xyz
- 检查 projects.json 配置
- 检测死链
"""

import os
import re
import json

ROOT_DIR = r"E:\Developer-Toolbox-by-WangDadi"

def fix_focusinbox_urls():
    """修复 FocusInbox URL"""
    print("=" * 70)
    print("1. 修复 FocusInbox URL")
    print("=" * 70)

    old_domain = "focusinbox.wangdadi.xyz"
    new_domain = "focusinbox-eight.wangdadi.xyz"

    fixed_count = 0
    for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
        if '.git' in dirpath:
            continue
        for filename in filenames:
            if filename.endswith('.md'):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8-sig', errors='replace') as f:
                        content = f.read()

                    if old_domain in content:
                        new_content = content.replace(old_domain, new_domain)
                        with open(filepath, 'w', encoding='utf-8-sig') as f:
                            f.write(new_content)
                        fixed_count += 1
                        print(f"✅ 修复: {filepath.replace(ROOT_DIR + os.sep, '')}")
                except Exception as e:
                    print(f"❌ 错误: {filepath} - {e}")

    print(f"\n📊 共修复 {fixed_count} 个文件")
    return fixed_count

def check_projects_json():
    """检查并修复 projects.json"""
    print("\n" + "=" * 70)
    print("2. 检查 projects.json")
    print("=" * 70)

    json_path = os.path.join(ROOT_DIR, "projects.json")
    if not os.path.exists(json_path):
        print("⚠️ projects.json 不存在，跳过")
        return

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            projects = json.load(f)

        fixed = False
        for project in projects:
            if 'url' in project and 'focusinbox.wangdadi.xyz' in project['url']:
                old_url = project['url']
                project['url'] = project['url'].replace('focusinbox.wangdadi.xyz', 'focusinbox-eight.wangdadi.xyz')
                print(f"✅ projects.json 修复: {project.get('name', 'unknown')}")
                print(f"   {old_url} → {project['url']}")
                fixed = True

        if fixed:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(projects, f, ensure_ascii=False, indent=2)
            print("✅ projects.json 已更新")
        else:
            print("⚠️ projects.json 无需修复")

    except Exception as e:
        print(f"❌ projects.json 处理失败: {e}")

def check_broken_links():
    """检测死链（括号没关好的）"""
    print("\n" + "=" * 70)
    print("3. 检测死链")
    print("=" * 70)

    broken_links = []
    bracket_pattern = re.compile(r'\[([^\]]+)\]\(([^)]*)$')  # 开了括号没关的

    for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
        if '.git' in dirpath:
            continue
        for filename in filenames:
            if filename.endswith('.md'):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8-sig', errors='replace') as f:
                        content = f.read()

                    matches = bracket_pattern.findall(content)
                    for text, url in matches:
                        if url.strip():
                            broken_links.append((filepath, text, url))
                except:
                    pass

    if broken_links:
        print(f"⚠️ 发现 {len(broken_links)} 个疑似死链:")
        for path, text, url in broken_links[:20]:
            print(f"  ❌ [{text}]({url}...")
            print(f"     文件: {path}")
        if len(broken_links) > 20:
            print(f"  ... 还有 {len(broken_links) - 20} 个")
    else:
        print("✅ 未发现明显死链")

def check_utm_params():
    """二次检查 UTM 参数"""
    print("\n" + "=" * 70)
    print("4. 检查 UTM 参数保留情况")
    print("=" * 70)

    files_with_utm = 0
    files_without_utm = 0

    for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
        if '.git' in dirpath:
            continue
        for filename in filenames:
            if filename.endswith('.md'):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8-sig', errors='replace') as f:
                        content = f.read()

                    if 'wangdadi' in content.lower():
                        if 'utm_source' in content:
                            files_with_utm += 1
                        else:
                            files_without_utm += 1
                except:
                    pass

    print(f"📊 含 UTM 参数: {files_with_utm} 个文件")
    print(f"⚠️ 不含 UTM 参数: {files_without_utm} 个文件")

def main():
    print("FocusInbox URL 修复脚本")
    print("=" * 70)

    fix_focusinbox_urls()
    check_projects_json()
    check_broken_links()
    check_utm_params()

    print("\n" + "=" * 70)
    print("所有修复完成！")
    print("=" * 70)

if __name__ == "__main__":
    main()