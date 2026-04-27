import os
import json

import shutil
import re

# 配置路径
SAAS_DIR = "E:\\kaifa\\saas"
MOTHERSHIP_DIR = "E:\\Developer-Toolbox-by-WangDadi"

# 读取 marketing_init.json 文件
def read_marketing_init(project_path):
    init_file = os.path.join(project_path, "marketing_init.json")
    if os.path.exists(init_file):
        with open(init_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

# 创建项目目录
def create_project_directory(project_name):
    project_dir = os.path.join(MOTHERSHIP_DIR, project_name)
    manual_dir = os.path.join(project_dir, "manual")
    
    # 创建项目目录
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)
    
    # 创建 manual 目录
    if not os.path.exists(manual_dir):
        os.makedirs(manual_dir)
    
    return project_dir, manual_dir

# 多语种词典
i18n_dict = {
    'en': {
        'overview': 'Overview',
        'detailed_content': 'Detailed Content',
        'what_is': 'What is',
        'core_features': 'Core Features',
        'how_to_use': 'How to Use',
        'step': 'Step',
        'feature': 'feature',
        'best_practices': 'Best Practices',
        'practice': 'Practice',
        'related_resources': 'Related Resources',
        'official_documentation': 'Official Documentation',
        'github_repository': 'GitHub Repository',
        'api_reference': 'API Reference',
        'navigation': 'Navigation',
        'back_to_mothership': 'Back to WangDadi Toolbox Index',
        'professional_tool': 'professional tool',
        'solve_problems': 'solve problems in related fields',
        'describe': 'Describe'
    },
    'de': {
        'overview': 'Übersicht',
        'detailed_content': 'Detaillierter Inhalt',
        'what_is': 'Was ist',
        'core_features': 'Kernfunktionen',
        'how_to_use': 'So verwenden Sie es',
        'step': 'Schritt',
        'feature': 'Funktion',
        'best_practices': 'Beste Praktiken',
        'practice': 'Praxis',
        'related_resources': 'Verwandte Ressourcen',
        'official_documentation': 'Offizielle Dokumentation',
        'github_repository': 'GitHub-Repository',
        'api_reference': 'API-Referenz',
        'navigation': 'Navigation',
        'back_to_mothership': 'Zurück zum WangDadi Toolbox Index',
        'professional_tool': 'professionelles Tool',
        'solve_problems': 'Probleme in verwandten Bereichen lösen',
        'describe': 'Beschreiben'
    },
    'es': {
        'overview': 'Resumen',
        'detailed_content': 'Contenido Detallado',
        'what_is': '¿Qué es',
        'core_features': 'Características Principales',
        'how_to_use': 'Cómo Usar',
        'step': 'Paso',
        'feature': 'característica',
        'best_practices': 'Mejores Prácticas',
        'practice': 'Práctica',
        'related_resources': 'Recursos Relacionados',
        'official_documentation': 'Documentación Oficial',
        'github_repository': 'Repositorio de GitHub',
        'api_reference': 'Referencia de API',
        'navigation': 'Navegación',
        'back_to_mothership': 'Volver al Índice de WangDadi Toolbox',
        'professional_tool': 'herramienta profesional',
        'solve_problems': 'resolver problemas en campos relacionados',
        'describe': 'Describir'
    },
    'ja': {
        'overview': '概要',
        'detailed_content': '詳細な内容',
        'what_is': 'とは',
        'core_features': 'コア機能',
        'how_to_use': '使い方',
        'step': 'ステップ',
        'feature': '機能',
        'best_practices': 'ベストプラクティス',
        'practice': 'プラクティス',
        'related_resources': '関連リソース',
        'official_documentation': '公式ドキュメント',
        'github_repository': 'GitHub リポジトリ',
        'api_reference': 'API リファレンス',
        'navigation': 'ナビゲーション',
        'back_to_mothership': 'WangDadi ツールボックス インデックスに戻る',
        'professional_tool': 'プロフェッショナルツール',
        'solve_problems': '関連分野の問題を解決する',
        'describe': '説明する'
    },
    'fr': {
        'overview': 'Aperçu',
        'detailed_content': 'Contenu Détailé',
        'what_is': 'Quest-ce que',
        'core_features': 'Fonctionnalités Principales',
        'how_to_use': 'Comment Utiliser',
        'step': 'Étape',
        'feature': 'fonctionnalité',
        'best_practices': 'Meilleures Pratiques',
        'practice': 'Pratique',
        'related_resources': 'Ressources Liées',
        'official_documentation': 'Documentation Officielle',
        'github_repository': 'Dépôt GitHub',
        'api_reference': 'Référence API',
        'navigation': 'Navigation',
        'back_to_mothership': 'Retour à lIndex WangDadi Toolbox',
        'professional_tool': 'outil professionnel',
        'solve_problems': 'résoudre les problèmes dans des domaines connexes',
        'describe': 'Décire'
    }
}

# 生成 SEO 友好的 .md 文件
def generate_seo_files(manual_dir, keywords, project_name):
    # 生成 20-50 个 SEO 友好的 .md 文件
    num_files = 30  # 取中间值
    
    # 生成英文版文件
    generate_language_files(manual_dir, keywords, project_name, 'en')
    
    return num_files

def generate_language_files(manual_dir, keywords, project_name, lang):
    # 获取对应语言的词典
    lang_dict = i18n_dict.get(lang, i18n_dict['en'])
    
    # 确定目标目录
    if lang == 'en':
        target_dir = manual_dir
    else:
        target_dir = os.path.join(manual_dir, lang)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
    
    # 生成文件
    for i in range(1, 31):  # 30个文件
        # 为每个文件生成一个唯一的标识符
        file_id = f"{project_name[:3].upper()}_{i:03d}"
        
        # 随机选择几个关键词
        selected_keywords = keywords[:min(3, len(keywords))]
        
        # 生成文件内容
        content = f"# {project_name} - {file_id}\n\n"
        content += f"## {lang_dict['overview']}\n\n"
        content += f"This is SEO optimized content for the {project_name} project, keywords: {', '.join(selected_keywords)}\n\n"
        content += f"## {lang_dict['detailed_content']}\n\n"
        content += f"### {lang_dict['what_is']} {project_name}?\n\n"
        content += f"{project_name} is a {lang_dict['professional_tool']} that helps {lang_dict['solve_problems']}.\n\n"
        content += f"### {lang_dict['core_features']}\n\n"
        content += f"- {lang_dict['describe']} {lang_dict.get('feature', 'feature')} 1\n"
        content += f"- {lang_dict['describe']} {lang_dict.get('feature', 'feature')} 2\n"
        content += f"- {lang_dict['describe']} {lang_dict.get('feature', 'feature')} 3\n\n"
        content += f"### {lang_dict['how_to_use']}\n\n"
        content += f"1. {lang_dict['step']} 1: {lang_dict['describe']} {lang_dict['step']} 1\n"
        content += f"2. {lang_dict['step']} 2: {lang_dict['describe']} {lang_dict['step']} 2\n"
        content += f"3. {lang_dict['step']} 3: {lang_dict['describe']} {lang_dict['step']} 3\n\n"
        content += f"### {lang_dict['best_practices']}\n\n"
        content += f"- {lang_dict['practice']} 1: {lang_dict['describe']} {lang_dict['practice']} 1\n"
        content += f"- {lang_dict['practice']} 2: {lang_dict['describe']} {lang_dict['practice']} 2\n\n"
        content += f"## {lang_dict['related_resources']}\n\n"
        content += f"- [{lang_dict['official_documentation']}](https://{project_name.lower()}.example.com/docs)\n"
        content += f"- [{lang_dict['github_repository']}](https://github.com/xingfangwang-eng/{project_name.lower()})\n"
        content += f"- [{lang_dict['api_reference']}](https://{project_name.lower()}.example.com/api)\n\n"
        content += f"## {lang_dict['navigation']}\n\n"
        
        # 计算相对路径到母舰首页
        if lang == 'en':
            home_link = "../.."
        else:
            home_link = "../../.."
        
        content += f"- [{lang_dict['back_to_mothership']}]({home_link}/README.md)\n"
        
        # 写入文件
        file_path = os.path.join(target_dir, f"{file_id}.md")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

# 更新 projects.json
def update_projects_json(project_info):
    projects_file = os.path.join(MOTHERSHIP_DIR, "projects.json")
    
    # 读取现有项目
    if os.path.exists(projects_file):
        with open(projects_file, 'r', encoding='utf-8') as f:
            projects = json.load(f)
    else:
        projects = []
    
    # 检查项目是否已存在
    project_name = project_info["name"]
    existing_projects = [p["name"] for p in projects]
    
    if project_name not in existing_projects:
        # 构建项目信息
        new_project = {
            "name": project_name,
            "keywords": project_info["keywords"],
            "manual_base_url": f"https://github.com/xingfangwang-eng/Developer-Toolbox-by-WangDadi/blob/main/{project_name.lower()}/manual/"
        }
        
        # 添加新项目
        projects.append(new_project)
        
        # 写回文件
        with open(projects_file, 'w', encoding='utf-8') as f:
            json.dump(projects, f, indent=2, ensure_ascii=False)
        
        return True
    return False

# 更新 README.md
def update_readme(project_info):
    readme_file = os.path.join(MOTHERSHIP_DIR, "README.md")
    
    if not os.path.exists(readme_file):
        # 如果 README 不存在，创建一个基本的
        content = "# 🛠️ WangDadi's Developer Toolbox\n\n"
        content += "## 🚀 项目简介\n\n"
        content += "基于 AI 和自动化驱动的开发者工具矩阵，致力于解决数据库、系统及 SaaS 开发中的核心痛点。\n\n"
        content += "## 📦 工具矩阵\n\n"
        content += "| 工具名称 | 描述 | 链接 |\n"
        content += "|---------|------|------|\n"
    else:
        # 读取现有 README
        with open(readme_file, 'r', encoding='utf-8') as f:
            content = f.read()
    
    # 检查工具矩阵是否存在
    if "| 工具名称 | 描述 | 链接 |" not in content:
        # 如果工具矩阵不存在，添加它
        content += "\n## 📦 工具矩阵\n\n"
        content += "| 工具名称 | 描述 | 链接 |\n"
        content += "|---------|------|------|\n"
    
    # 提取工具矩阵部分
    lines = content.split('\n')
    table_start = -1
    table_end = -1
    
    for i, line in enumerate(lines):
        if "| 工具名称 | 描述 | 链接 |" in line:
            table_start = i
        elif table_start != -1 and line.strip() and not line.startswith('|'):
            table_end = i
            break
    
    if table_end == -1:
        table_end = len(lines)
    
    # 检查项目是否已在表格中
    project_name = project_info["name"]
    project_link = f"./{project_name.lower()}/"
    
    project_in_table = False
    for i in range(table_start + 2, table_end):
        if project_name in lines[i]:
            project_in_table = True
            break
    
    if not project_in_table:
        # 构建新的表格行
        description = project_info.get('description', '专业工具')
        new_row = f"| {project_name} | {description} | [查看详情]({project_link}) |"
        
        # 插入新行
        lines.insert(table_end, new_row)
        
        # 写回文件
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        return True
    return False

# 从 sites.json 读取项目网站信息
def load_sites_info():
    sites_file = os.path.join(MOTHERSHIP_DIR, "sites.json")
    if os.path.exists(sites_file):
        with open(sites_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# 从 projects.json 更新 README.md
def update_readme_from_projects():
    projects_file = os.path.join(MOTHERSHIP_DIR, "projects.json")
    readme_file = os.path.join(MOTHERSHIP_DIR, "README.md")
    
    if os.path.exists(projects_file) and os.path.exists(readme_file):
        with open(projects_file, 'r', encoding='utf-8') as f:
            projects = json.load(f)
        
        # 读取 sites.json 中的项目网站信息
        sites_info = load_sites_info()
        # 创建项目名到网站 URL 的映射
        site_url_map = {}
        for site in sites_info:
            site_name = site["name"]
            if site_name not in site_url_map:
                site_url_map[site_name] = site["url"]
        
        # 读取现有 README
        with open(readme_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 按类别分组项目
        projects_by_category = {}
        for project in projects:
            category = project.get("category", "Other").title()
            if category not in projects_by_category:
                projects_by_category[category] = []
            projects_by_category[category].append(project)
        
        # 为每个类别排序项目
        for category in projects_by_category:
            projects_by_category[category] = sorted(projects_by_category[category], key=lambda x: x["name"])
        
        # 构建新的工具矩阵部分
        table_content = "## 📦 工具矩阵\n\n"
        
        # 定义类别图标
        category_icons = {
            "Ai": "🤖",
            "Database": "📊",
            "Social": "👥",
            "Productivity": "⚡",
            "Other": "📦"
        }
        
        # 为每个类别创建表格
        for category in sorted(projects_by_category.keys()):
            # 获取类别图标
            icon = category_icons.get(category, "📦")
            
            # 添加类别标题
            table_content += f"### {icon} {category} Tools\n\n"
            table_content += "| 项目名 | 描述 | 手册 | 官网 | Why Switch? |\n"
            table_content += "|-------|------|------|------|------------|\n"
            
            # 添加该类别的项目
            for project in projects_by_category[category]:
                project_name = project["name"]
                project_dir = project_name.lower().replace(' ', '-')
                
                # 从 sites.json 中获取官方网站 URL
                official_site = site_url_map.get(project_name, project.get("url", "#"))
                
                # 尝试从 marketing_init.json 中读取描述
                marketing_file = os.path.join(SAAS_DIR, project_dir, "marketing_init.json")
                description = project.get("description", "")
                
                if os.path.exists(marketing_file):
                    try:
                        with open(marketing_file, 'r', encoding='utf-8') as f:
                            marketing_data = json.load(f)
                            if "description" in marketing_data:
                                description = marketing_data["description"]
                    except Exception as e:
                        print(f"Error reading marketing_init.json for {project_name}: {e}")
                
                # 兜底逻辑：如果没有描述，根据项目名生成英文描述
                if not description or description == "专业工具":
                    # 将项目名转换为英文描述
                    project_name_parts = project_name.split()
                    # 简单的英文描述生成逻辑
                    if len(project_name_parts) > 1:
                        # 对于多个单词的项目名，使用 "Professional [项目名] tool that provides comprehensive solutions" 格式
                        description = f"Professional {project_name} tool that provides comprehensive solutions."
                    else:
                        # 对于单个单词的项目名，使用 "Professional tool for [项目名] related tasks and solutions" 格式
                        description = f"Professional tool for {project_name.lower()} related tasks."
                
                # 构建多语种手册链接
                manual_links = ""
                if os.path.exists(os.path.join(MOTHERSHIP_DIR, project_dir, 'manual')):
                    manual_links += "🇺🇸"
                if os.path.exists(os.path.join(MOTHERSHIP_DIR, project_dir, 'manual', 'es')):
                    manual_links += " 🇪🇸"
                if os.path.exists(os.path.join(MOTHERSHIP_DIR, project_dir, 'manual', 'de')):
                    manual_links += " 🇩🇪"
                if os.path.exists(os.path.join(MOTHERSHIP_DIR, project_dir, 'manual', 'ja')):
                    manual_links += " 🇯🇵"
                
                # 构建手册链接
                manual_link = f"[{manual_links}](./{project_dir}/manual/)" if manual_links else "-"
                
                # 构建 Why Switch? 链接
                why_switch_links = []
                competitors = project.get('competitors', [])
                for competitor in competitors:
                    competitor_slug = competitor.lower().replace(' ', '-')
                    why_switch_links.append(f"[{competitor}](./{project_dir}/manual/vs/{competitor_slug}.md)")
                
                why_switch = " | ".join(why_switch_links) if why_switch_links else "-"
                
                table_content += f"| {project_name} | {description} | {manual_link} | [🌐]({official_site}) | {why_switch} |\n"
            
            # 添加类别之间的空行
            table_content += "\n"
        
        # 替换现有的工具矩阵部分
        if "## 📦 工具矩阵" in content:
            # 找到工具矩阵的开始和结束位置
            lines = content.split('\n')
            start_idx = -1
            end_idx = -1
            
            for i, line in enumerate(lines):
                if "## 📦 工具矩阵" in line:
                    start_idx = i
                elif start_idx != -1 and line.startswith("## ") and line != "## 📦 工具矩阵":
                    end_idx = i
                    break
            
            if end_idx == -1:
                end_idx = len(lines)
            
            # 替换工具矩阵部分
            new_lines = lines[:start_idx] + table_content.split('\n') + lines[end_idx:]
            content = '\n'.join(new_lines)
        else:
            # 如果工具矩阵不存在，添加它
            content += "\n" + table_content
        
        # 写回文件
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    return False

# 为现有 .md 文件添加返回母舰首页的链接
def add_navigation_links():
    print("开始为现有 .md 文件添加导航链接...")
    
    # 遍历所有项目目录
    for item in os.listdir(MOTHERSHIP_DIR):
        item_path = os.path.join(MOTHERSHIP_DIR, item)
        
        # 只处理目录
        if not os.path.isdir(item_path):
            continue
        
        # 检查是否有 manual 目录
        manual_dir = os.path.join(item_path, "manual")
        if not os.path.exists(manual_dir):
            continue
        
        # 遍历 manual 目录及其子目录中的所有 .md 文件
        for root, dirs, files in os.walk(manual_dir):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    
                    # 确定文件语言
                    relative_path = os.path.relpath(root, manual_dir)
                    if relative_path == '.':
                        # 直接在 manual 目录下，默认为英文
                        lang = 'en'
                        home_link = "../.."
                    else:
                        # 在子目录中，子目录名即为语言代码
                        lang = relative_path.split(os.sep)[0]
                        # 计算相对路径到母舰首页，确保包含 README.md
                        home_link = "../.."
                    
                    # 读取文件内容
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 清理重复的导航部分
                    # 移除所有现有的导航部分
                    content = re.sub(r'##\s*导航\n\n-\s*\[Back to WangDadi Toolbox Index\].*?\n', '', content, flags=re.DOTALL)
                    
                    # 检查是否已经有正确的导航部分
                    lang_dict = i18n_dict.get(lang, i18n_dict['en'])
                    back_text = lang_dict['back_to_mothership']
                    
                    if back_text not in content:
                        # 添加正确的导航部分
                        content += f"\n## {lang_dict['navigation']}\n\n"
                        content += f"- [{back_text}]({home_link}/README.md)\n"
                        
                        # 写回文件
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        print(f"已为 {file_path} 添加导航链接")
    
    print("导航链接添加完成！")

# 主函数
def main():
    print(f"开始扫描 {SAAS_DIR} 目录...")
    
    # 扫描 saas 目录
    for item in os.listdir(SAAS_DIR):
        item_path = os.path.join(SAAS_DIR, item)
        
        # 只处理目录
        if not os.path.isdir(item_path):
            continue
        
        # 检查是否包含 marketing_init.json
        project_info = read_marketing_init(item_path)
        if project_info:
            print(f"\n发现新项目: {item}")
            print(f"项目信息: {project_info}")
            
            # 创建项目目录
            project_dir, manual_dir = create_project_directory(item)
            print(f"创建项目目录: {project_dir}")
            
            # 生成 SEO 文件
            num_files = generate_seo_files(manual_dir, project_info["keywords"], item)
            print(f"生成了 {num_files} 个 SEO 友好的 .md 文件")
            
            # 更新 projects.json
            if update_projects_json(project_info):
                print("更新了 projects.json")
            else:
                print("项目已存在于 projects.json 中")
            
            # 更新 README.md
            if update_readme(project_info):
                print("更新了 README.md")
            else:
                print("项目已存在于 README.md 中")
        else:
            print(f"跳过目录: {item} (未找到 marketing_init.json)")
    
    # 为所有现有项目重新生成多语种文件
    print("\n开始为现有项目重新生成多语种文件...")
    projects_file = os.path.join(MOTHERSHIP_DIR, "projects.json")
    if os.path.exists(projects_file):
        with open(projects_file, 'r', encoding='utf-8') as f:
            projects = json.load(f)
        
        for project in projects:
            project_name = project["name"]
            project_dir = os.path.join(MOTHERSHIP_DIR, project_name.lower().replace(' ', '-'))
            manual_dir = os.path.join(project_dir, "manual")
            
            if os.path.exists(manual_dir):
                print(f"\n重新生成 {project_name} 的多语种文件...")
                # 生成英文版
                generate_language_files(manual_dir, project["keywords"], project_name, 'en')
                # 生成其他语言版本
                for lang in ['de', 'es', 'ja']:
                    generate_language_files(manual_dir, project["keywords"], project_name, lang)
                print(f"{project_name} 的多语种文件生成完成")
    
    # 从 projects.json 更新 README.md
    if update_readme_from_projects():
        print("从 projects.json 更新了 README.md")
    
    # 为现有 .md 文件添加导航链接
    add_navigation_links()
    
    print("\n扫描完成！")

if __name__ == "__main__":
    main()