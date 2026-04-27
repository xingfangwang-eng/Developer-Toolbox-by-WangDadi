import os
import json

# 占位符列表（不区分大小写）
PLACEHOLDERS = [
    'Describe feature',
    'Describe Step',
    'Beschreiben',
    'Describir',
    '説明'
]

# 结果统计
total_files = 0
critical_files = 0
critical_file_paths = []

# 遍历目录
def audit_directory(directory):
    global total_files, critical_files, critical_file_paths
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                total_files += 1
                
                # 读取文件内容
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().lower()
                    
                    # 检查是否包含占位符
                    is_critical = False
                    for placeholder in PLACEHOLDERS:
                        if placeholder.lower() in content:
                            is_critical = True
                            break
                    
                    if is_critical:
                        print(f"找到僵尸文件: {file_path}")
                        critical_files += 1
                        critical_file_paths.append(file_path)
                except Exception as e:
                    print(f"[ERROR] 无法读取文件 {file_path}: {e}")
                    critical_files += 1
                    critical_file_paths.append(file_path)

# 主函数
def main():
    print("开始执行体检脚本...")
    
    # 遍历当前目录
    base_directory = os.path.dirname(os.path.abspath(__file__))
    audit_directory(base_directory)
    
    # 生成报告
    print("\n=== 体检报告 ===")
    print(f"总文件数: {total_files}")
    print(f"僵尸文件数: {critical_files}")
    print(f"就绪文件数: {total_files - critical_files}")
    
    # 生成待办清单
    todo_list = {
        "total_files": total_files,
        "critical_files": critical_files,
        "ready_files": total_files - critical_files,
        "critical_file_paths": critical_file_paths
    }
    
    with open('todo_list.json', 'w', encoding='utf-8') as f:
        json.dump(todo_list, f, ensure_ascii=False, indent=2)
    
    print("\n待办清单已生成到 todo_list.json")
    print(f"真实的僵尸文件数量: {critical_files}")

if __name__ == "__main__":
    main()