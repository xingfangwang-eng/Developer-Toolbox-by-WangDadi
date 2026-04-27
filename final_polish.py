import os
import re
from tqdm import tqdm

# 全局变量
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# 清理单个文件
def polish_file(file_path):
    # 读取文件内容
    try:
        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"读取文件失败 {file_path}: {e}")
        return False
    
    # 确定文件语言
    lang = "en"  # 默认英语
    parts = file_path.split(os.sep)
    for part in parts:
        if part == "de":
            lang = "de"
            break
        elif part == "es":
            lang = "es"
            break
        elif part == "ja":
            lang = "ja"
            break
    
    # 确定项目名和文件名
    file_name = os.path.basename(file_path)
    file_id = os.path.splitext(file_name)[0]  # 去掉后缀
    
    # 确定项目名
    project_name = ""
    for part in parts:
        if "manual" in part:
            # 找到 manual 文件夹的上一级作为项目名
            manual_index = parts.index(part)
            if manual_index > 0:
                project_name = parts[manual_index - 1]
            break
    
    # 清理并修改内容
    new_lines = []
    in_related_resources = False
    
    for line in lines:
        # 删除 SEO 废话
        if re.search(r'This is SEO optimized content for the|keywords:', line):
            continue
        
        # 处理 H1 标题
        if line.startswith('# ') and not new_lines:  # 第一行
            new_title = f"# {project_name} - {file_id}"
            new_lines.append(new_title + '\n')
            continue
        
        # 处理相关资源部分
        if 'Related Resources' in line or 'Verwandte Ressourcen' in line:
            in_related_resources = True
            new_lines.append(line)
        elif in_related_resources:
            # 替换 example.com 链接
            if 'example.com' in line:
                new_line = re.sub(r'https?://[^\s`]+example\.com[^\s`]+', 'https://www.wangdadi.xyz', line)
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    # 添加或更新页脚
    # 首先检查是否已有页脚
    has_footer = False
    for line in new_lines:
        if 'wangdadi.xyz' in line:
            has_footer = True
            break
    
    if not has_footer:
        # 添加页脚
        footer = ''
        if lang == "de":
            footer = '\n---\n\n👉 Haben Sie genug von unordentlichen Daten? Reinigen Sie Ihre CSV-Dateien jetzt unter: `https://wangdadi.xyz`\n'
        elif lang == "es":
            footer = '\n---\n\n👉 ¿Cansado de los datos desordenados? Limpie sus archivos CSV ahora en: `https://wangdadi.xyz`\n'
        elif lang == "ja":
            footer = '\n---\n\n👉 データの乱れにお困りですか？今すぐCSVファイルをクリーンアップ： `https://wangdadi.xyz`\n'
        # 英语保持原样，不添加页脚
        
        if footer:
            new_lines.append(footer)
    
    # 写入修改后的内容
    try:
        with open(file_path, 'w', encoding='utf-8-sig') as f:
            f.writelines(new_lines)
        return True
    except Exception as e:
        print(f"写入文件失败 {file_path}: {e}")
        return False

# 主函数
def main():
    # 收集所有 .md 文件
    md_files = []
    
    for root, dirs, files in os.walk(ROOT_DIR):
        # 跳过不需要的文件夹
        dirs[:] = [d for d in dirs if d not in ['.git', 'venv', '__pycache__']]
        
        # 收集 .md 文件
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                md_files.append(file_path)
    
    total_files = len(md_files)
    print(f"共发现 {total_files} 个 .md 文件")
    
    # 清理文件
    processed_count = 0
    success_count = 0
    
    for file_path in tqdm(md_files, desc="清理进度"):
        processed_count += 1
        if polish_file(file_path):
            success_count += 1
    
    print(f"\n清理完成！")
    print(f"总文件数: {total_files}")
    print(f"处理文件数: {processed_count}")
    print(f"成功清理文件数: {success_count}")

if __name__ == "__main__":
    main()