#!/usr/bin/env python3
import os
import re
import glob

BASE_DIR = r"E:\Developer-Toolbox-by-WangDadi"
KILL_LIST_FILE = r"E:\Developer-Toolbox-by-WangDadi\KILL_LIST.txt"

POLLUTED_KEYWORDS = [
    "概述", "核心功能", "步骤", "Describe feature", "Step 1",
    "核心", "功能点", "自定义", "异常", "故障", "问题",
    "解决方案", "配置", "设置", "安装步骤", "简介", "主要功能",
    "使用方法", "技术架构", "应用场景", "优势特点", "快速开始",
    "环境要求", "安装教程", "常见问题", "更新日志", "版本说明"
]

def has_polluted_keywords(content):
    for keyword in POLLUTED_KEYWORDS:
        if keyword in content:
            return True, keyword
    return False, None

def has_chinese_chars(content):
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
    return len(chinese_pattern.findall(content)) > 0

def has_colab_hook(content):
    return "colab.research.google.com" in content and "utm_source=github_local" in content

def audit_file(filepath):
    results = {
        'filepath': filepath,
        'is_zombie': False,
        'reasons': []
    }
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 内容厚度检查
        char_count = len(content)
        if char_count <= 400:
            results['is_zombie'] = True
            results['reasons'].append(f"内容过薄 ({char_count} 字)")
        
        # 关键词污染检查
        has_polluted, keyword = has_polluted_keywords(content)
        if has_polluted:
            results['is_zombie'] = True
            results['reasons'].append(f"关键词污染: {keyword}")
        
        # 电钩子检查
        if not has_colab_hook(content):
            results['is_zombie'] = True
            results['reasons'].append("缺少电钩子 (colab.research.google.com + utm_source=github_local)")
        
        # 日语版专项检查
        if "/ja/" in filepath:
            if has_chinese_chars(content):
                results['is_zombie'] = True
                results['reasons'].append("日语版包含简体中文")
        
    except Exception as e:
        results['is_zombie'] = True
        results['reasons'].append(f"读取错误: {str(e)}")
    
    return results

def main():
    print("=" * 80)
    print("AUDIT V3 - 终极判决系统")
    print("=" * 80)
    print("正在扫描所有项目文件...")
    
    all_files = []
    for pattern in [
        os.path.join(BASE_DIR, "*/manual/*/*.md"),
        os.path.join(BASE_DIR, "*/manual/*.md"),
    ]:
        all_files.extend(glob.glob(pattern))
    
    all_files = list(set(all_files))
    total_files = len(all_files)
    print(f"扫描完成，共发现 {total_files} 个文件")
    print("-" * 80)
    
    zombie_list = []
    soul_count = 0
    
    for i, filepath in enumerate(all_files, 1):
        if i % 100 == 0:
            print(f"\r审计进度: {i}/{total_files} ({(i/total_files)*100:.1f}%)", end="")
        
        result = audit_file(filepath)
        if result['is_zombie']:
            zombie_list.append(result)
        else:
            soul_count += 1
    
    print(f"\r审计进度: {total_files}/{total_files} (100%)")
    print("-" * 80)
    
    zombie_count = len(zombie_list)
    soul_rate = (soul_count / total_files) * 100
    
    print("\n" + "=" * 80)
    print("审计结果报告")
    print("=" * 80)
    print(f"总文件数: {total_files}")
    print(f"灵魂页数: {soul_count}")
    print(f"僵尸页数: {zombie_count}")
    print(f"注魂率: {soul_rate:.2f}%")
    print("=" * 80)
    
    if zombie_count > 0:
        print(f"\n发现 {zombie_count} 个僵尸文件，正在写入 KILL_LIST.txt...")
        with open(KILL_LIST_FILE, "w", encoding="utf-8") as f:
            for zombie in zombie_list:
                f.write(f"{zombie['filepath']}\n")
                f.write(f"  原因: {', '.join(zombie['reasons'])}\n")
                f.write("-" * 100 + "\n")
        
        print("\n僵尸文件详情:")
        print("-" * 80)
        for i, zombie in enumerate(zombie_list[:10], 1):
            print(f"\n[{i}] {zombie['filepath']}")
            for reason in zombie['reasons']:
                print(f"      ✗ {reason}")
        
        if zombie_count > 10:
            print(f"\n... 还有 {zombie_count - 10} 个僵尸文件未显示")
    
    if soul_rate == 100.0:
        print("\n🎉 恭喜！所有文件通过审计，注魂率 100%！")
    else:
        print(f"\n⚠️ 警告：发现 {zombie_count} 个僵尸文件！")
        print("立即行动，消灭僵尸！")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()