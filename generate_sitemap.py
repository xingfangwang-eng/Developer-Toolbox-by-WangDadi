import os
import json
import time

# 全局变量
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_FILE = os.path.join(ROOT_DIR, 'projects.json')
SITEMAP_FILE = os.path.join(ROOT_DIR, 'sitemap.xml')
BASE_DOMAIN = 'wangdadi.xyz'

# 读取项目文件
def load_projects():
    if os.path.exists(PROJECTS_FILE):
        try:
            with open(PROJECTS_FILE, 'r', encoding='utf-8-sig') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载项目文件失败: {e}")
            return []
    else:
        print(f"项目文件不存在: {PROJECTS_FILE}")
        return []

# 生成 sitemap.xml
def generate_sitemap(projects):
    # 生成 XML 头部
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'''
    
    # 添加每个项目的 URL
    for project in projects:
        project_name = project.get('name', '').lower().replace(' ', '-')
        if project_name:
            subdomain_url = f"https://{project_name}.{BASE_DOMAIN}"
            lastmod = time.strftime('%Y-%m-%d')
            
            xml_content += f'''
    <url>
        <loc>{subdomain_url}</loc>
        <lastmod>{lastmod}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
'''
    
    # 关闭 urlset 标签
    xml_content += '''</urlset>
'''
    
    return xml_content

# 保存 sitemap.xml
def save_sitemap(xml_content):
    try:
        with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        return True
    except Exception as e:
        print(f"保存 sitemap.xml 失败: {e}")
        return False

# 主函数
def main():
    print("开始生成 sitemap.xml...")
    
    # 加载项目
    projects = load_projects()
    total_projects = len(projects)
    print(f"已加载 {total_projects} 个项目")
    
    # 生成 sitemap
    xml_content = generate_sitemap(projects)
    
    # 保存 sitemap
    if save_sitemap(xml_content):
        print(f"sitemap.xml 生成成功！")
        print(f"文件位置: {SITEMAP_FILE}")
        print(f"包含 {total_projects} 个子域名")
    else:
        print("sitemap.xml 生成失败！")

if __name__ == "__main__":
    main()