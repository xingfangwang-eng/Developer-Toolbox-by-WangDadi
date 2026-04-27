import os
import re
from tqdm import tqdm

# 全局变量
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# 修复单个文件的链接
def fix_file_links(file_path):
    # 确定文件的语言
    lang = "en"  # 默认英文版
    
    # 检查文件路径中的语言文件夹
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
    
    # 读取文件内容
    try:
        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"读取文件失败 {file_path}: {e}")
        return False
    
    # 定义标准链接格式
    standard_link = f'https://www.wangdadi.xyz/?utm_source=github_local&lang={lang}'
    
    # 检查并替换最后5行中的链接
    modified = False
    for i in range(max(0, len(lines) - 5), len(lines)):
        # 使用正则表达式查找包含 wangdadi.xyz 的链接
        if re.search(r'wangdadi\.xyz', lines[i]):
            # 替换整行中的链接
            lines[i] = re.sub(r'https?://[^\s`]+wangdadi\.xyz[^\s`]+', standard_link, lines[i])
            modified = True
    
    # 如果有修改，写入文件
    if modified:
        try:
            with open(file_path, 'w', encoding='utf-8-sig') as f:
                f.writelines(lines)
            return True
        except Exception as e:
            print(f"写入文件失败 {file_path}: {e}")
            return False
    
    # 即使没有找到链接，也强制在文件末尾添加标准链接
    # 确保每个文件都有正确的链接
    try:
        # 检查文件末尾是否已经有相关资源部分
        has_related_resources = False
        for i in range(max(0, len(lines) - 10), len(lines)):
            if 'Related Resources' in lines[i]:
                has_related_resources = True
                break
        
        if not has_related_resources:
            # 添加相关资源部分和标准链接
            lines.append('\n---\n\n')
            lines.append('## Related Resources\n')
            lines.append(f'- 👉 `{standard_link}`\n')
            modified = True
        
        if modified:
            with open(file_path, 'w', encoding='utf-8-sig') as f:
                f.writelines(lines)
            return True
    except Exception as e:
        print(f"添加链接失败 {file_path}: {e}")
    
    return False

# 主函数
def main():
    # 收集所有需要修复的 .md 文件
    md_files = []
    
    # 递归扫描所有 .md 文件
    for root, dirs, files in os.walk(ROOT_DIR):
        # 跳过不需要的文件夹
        dirs[:] = [d for d in dirs if d not in ['.git', 'venv']]
        
        # 收集所有 .md 文件
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                md_files.append(file_path)
    
    total_files = len(md_files)
    print(f"共发现 {total_files} 个需要修复的 .md 文件")
    
    # 修复文件链接
    fixed_count = 0
    
    for file_path in tqdm(md_files, desc="修复链接进度"):
        if fix_file_links(file_path):
            fixed_count += 1
    
    print(f"\n修复完成！")
    print(f"总文件数: {total_files}")
    print(f"成功修复文件数: {fixed_count}")

if __name__ == "__main__":
    main()