#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sitemap Generator - 生成 Google Sitemap 格式的站点地图
自动处理超过 5000 条目的情况
"""

import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

ROOT_DIR = r"E:\Developer-Toolbox-by-WangDadi"
OUTPUT_DIR = ROOT_DIR
GITHUB_REPO = "xingfangwang-eng/Developer-Toolbox-by-WangDadi"

# 选择使用 GitHub Pages 链接还是 Raw 链接
# 对于 SEO 来说，GitHub Pages 链接更合适
BASE_URL = f"https://{GITHUB_REPO.replace('/', '.github.io/')}"
# BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main"

def find_markdown_files(root_dir):
    """查找所有 Markdown 文件"""
    md_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if '.git' in dirpath:
            continue
        for filename in filenames:
            if filename.endswith('.md'):
                # 获取相对路径
                rel_path = os.path.relpath(os.path.join(dirpath, filename), root_dir)
                md_files.append(rel_path)
    return md_files

def generate_sitemap_entries(file_list):
    """生成 sitemap 条目"""
    urlset = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    
    for rel_path in file_list:
        # 将 Windows 路径转换为 URL 路径
        url_path = rel_path.replace('\\', '/')
        # GitHub Pages 链接
        loc = f"{BASE_URL}/{url_path}"
        
        url = ET.SubElement(urlset, 'url')
        loc_elem = ET.SubElement(url, 'loc')
        loc_elem.text = loc
        
        # 添加优先级（可选）
        priority = ET.SubElement(url, 'priority')
        priority.text = '0.7'
    
    return urlset

def prettify_xml(element):
    """美化 XML 输出"""
    rough_string = ET.tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding='UTF-8')

def generate_sitemaps(file_list, max_entries=5000):
    """生成多个 sitemap 文件"""
    total_files = len(file_list)
    num_sitemaps = (total_files // max_entries) + 1 if total_files % max_entries != 0 else total_files // max_entries
    
    sitemap_files = []
    
    for i in range(num_sitemaps):
        start = i * max_entries
        end = min((i + 1) * max_entries, total_files)
        chunk = file_list[start:end]
        
        filename = f"sitemap_{i + 1}.xml" if i > 0 else "sitemap.xml"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        urlset = generate_sitemap_entries(chunk)
        xml_content = prettify_xml(urlset)
        
        with open(filepath, 'wb') as f:
            f.write(xml_content)
        
        sitemap_files.append(filename)
        print(f"✅ 生成: {filename} ({len(chunk)} 条目)")
    
    return sitemap_files

def generate_sitemap_index(sitemap_files):
    """生成 sitemap 索引文件"""
    sitemapindex = ET.Element('sitemapindex', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    
    for sitemap_file in sitemap_files:
        sitemap = ET.SubElement(sitemapindex, 'sitemap')
        loc = ET.SubElement(sitemap, 'loc')
        loc.text = f"{BASE_URL}/{sitemap_file}"
    
    xml_content = prettify_xml(sitemapindex)
    filepath = os.path.join(OUTPUT_DIR, 'sitemap_index.xml')
    
    with open(filepath, 'wb') as f:
        f.write(xml_content)
    
    print(f"✅ 生成: sitemap_index.xml")

def main():
    print("=" * 60)
    print("Sitemap Generator")
    print("=" * 60)
    
    # 1. 查找所有 Markdown 文件
    print("🔍 扫描所有 Markdown 文件...")
    md_files = find_markdown_files(ROOT_DIR)
    print(f"📊 发现 {len(md_files)} 个 Markdown 文件")
    
    # 2. 生成 sitemap 文件
    print("\n📝 生成 Sitemap 文件...")
    sitemap_files = generate_sitemaps(md_files)
    
    # 3. 生成索引文件
    print("\n📋 生成 Sitemap 索引...")
    generate_sitemap_index(sitemap_files)
    
    print("\n" + "=" * 60)
    print(f"✅ Sitemap 生成完成！")
    print(f"📁 生成 {len(sitemap_files)} 个 sitemap 文件")
    print(f"📄 总条目数: {len(md_files)}")
    print("=" * 60)

if __name__ == "__main__":
    main()