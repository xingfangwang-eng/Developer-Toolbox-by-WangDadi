import os
import re
import json

# 读取 projects.json 文件
with open('projects.json', 'r', encoding='utf-8') as f:
    projects = json.load(f)

# 创建项目名称到关键词的映射
project_keywords = {}
for project in projects:
    project_name = project['name'].lower().replace(' ', '-')
    project_keywords[project_name] = project['keywords']

# 生成本地化导语

def generate_intro(project_name, lang, keywords):
    # 清理项目名称
    clean_project_name = project_name.replace('-', ' ').title()
    
    # 提取核心功能描述
    if keywords:
        # 使用第一个关键词作为功能描述
        core_function = keywords[0]
    else:
        core_function = "your tasks"
    
    if lang == 'de':
        return f"Willkommen beim {clean_project_name}-Leitfaden. Dieses Tool wurde entwickelt, um {core_function} effizient und einfach zu gestalten."
    elif lang == 'es':
        return f"Bienvenido a la guía de {clean_project_name}. Esta herramienta está diseñada para optimizar {core_function} de manera profesional."
    elif lang == 'ja':
        return f"{clean_project_name} ガイドへようこそ。このツールは、{core_function} を効率化するために開発されました。"
    else:
        return f"Welcome to the {clean_project_name} guide. This tool was developed to efficiently and easily handle {core_function}."

# 处理单个文件
def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 确定语言
        normalized_path = file_path.replace('\\', '/')
        if '/de/' in normalized_path:
            lang = 'de'
        elif '/es/' in normalized_path:
            lang = 'es'
        elif '/ja/' in normalized_path:
            lang = 'ja'
        else:
            lang = 'en'
        
        # 提取项目名称
        parts = file_path.split(os.sep)
        project_name = None
        for i, part in enumerate(parts):
            if part == 'manual':
                if i > 0:
                    project_name = parts[i-1].lower().replace(' ', '-')
                break
        
        if not project_name:
            return False
        
        # 获取关键词
        keywords = project_keywords.get(project_name, [])
        
        # 查找并替换 SEO 声明
        seo_pattern = r'This is SEO optimized content for.*?(?=\n\n|$)'
        if re.search(seo_pattern, content):
            intro = generate_intro(project_name, lang, keywords)
            content = re.sub(seo_pattern, intro, content)
            
            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        else:
            return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

# 主函数
def main():
    success_count = 0
    error_count = 0
    
    # 遍历所有项目目录
    for project in projects:
        project_name = project['name'].lower().replace(' ', '-')
        project_path = os.path.join(os.getcwd(), project_name)
        
        if os.path.exists(project_path):
            # 检查 manual 目录
            manual_path = os.path.join(project_path, 'manual')
            if os.path.exists(manual_path):
                # 检查 de、es、ja 文件夹
                for lang in ['de', 'es', 'ja']:
                    lang_path = os.path.join(manual_path, lang)
                    if os.path.exists(lang_path):
                        # 遍历所有 MD 文件
                        for root, dirs, files in os.walk(lang_path):
                            for file in files:
                                if file.endswith('.md'):
                                    file_path = os.path.join(root, file)
                                    if process_file(file_path):
                                        success_count += 1
                                    else:
                                        error_count += 1
    
    print(f"Processing complete!")
    print(f"Success: {success_count}")
    print(f"Error: {error_count}")

if __name__ == "__main__":
    main()
