import os

# 全局变量
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# 检测页面类型
def detect_page_type(content):
    # 僵尸页面检测：包含原始占位符
    zombie_indicators = [
        "Describe feature",
        "Step 1",
        "Beschreiben Funktion",
        "Schritt 1",
        "説明する",
        "ステップ 1",
        "Describir función",
        "Paso 1"
    ]
    
    for indicator in zombie_indicators:
        if indicator in content:
            return "Zombie"
    
    # 灵魂页面检测：不含占位符且长度超过 300 字符
    if len(content) > 300:
        return "Soul"
    
    # 其他情况
    return "Other"

# 扫描项目
def scan_projects():
    total_files = 0
    soul_pages = 0
    zombie_pages = 0
    other_pages = 0
    
    # 递归扫描所有项目的 manual/ 文件夹
    for root, dirs, files in os.walk(ROOT_DIR):
        # 跳过不需要的文件夹
        dirs[:] = [d for d in dirs if d not in ['.git', 'venv', '__pycache__']]
        
        # 检查是否在 manual 文件夹中
        if 'manual' in root.split(os.sep):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    total_files += 1
                    
                    # 读取文件内容
                    try:
                        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
                            content = f.read()
                        
                        # 检测页面类型
                        page_type = detect_page_type(content)
                        if page_type == "Soul":
                            soul_pages += 1
                        elif page_type == "Zombie":
                            zombie_pages += 1
                        else:
                            other_pages += 1
                    except Exception as e:
                        print(f"读取文件失败 {file_path}: {e}")
                        other_pages += 1
    
    return total_files, soul_pages, zombie_pages, other_pages

# 生成报表
def generate_report(total_files, soul_pages, zombie_pages, other_pages):
    # 计算资产完备率
    if total_files > 0:
        completion_rate = (soul_pages / total_files) * 100
    else:
        completion_rate = 0
    
    # 打印表格
    print("\n" + "=" * 60)
    print("🎯 资产审计报表")
    print("=" * 60)
    print(f"| {'指标':<10} | {'数值':<15} |")
    print("|" + "-" * 11 + "|" + "-" * 16 + "|")
    print(f"| {'总文件数':<10} | {total_files:<15} |")
    print(f"| {'灵魂页面数':<10} | {soul_pages:<15} |")
    print(f"| {'僵尸页面数':<10} | {zombie_pages:<15} |")
    print(f"| {'其他页面数':<10} | {other_pages:<15} |")
    print(f"| {'资产完备率':<10} | {completion_rate:.2f}%{'':<8} |")
    print("=" * 60)
    
    # 打印详细信息
    print(f"\n📊 审计结果分析:")
    print(f"- 总审计文件数: {total_files}")
    print(f"- 有效钓鱼资产: {soul_pages} (灵魂页面)")
    print(f"- 需要补救的垃圾: {zombie_pages} (僵尸页面)")
    print(f"- 其他页面: {other_pages}")
    print(f"- 资产完备率: {completion_rate:.2f}%")
    
    if completion_rate >= 90:
        print("\n🎉 优秀！资产完备率达到 90% 以上，钓鱼资产质量良好。")
    elif completion_rate >= 70:
        print("\n✅ 良好！资产完备率达到 70% 以上，钓鱼资产质量不错。")
    elif completion_rate >= 50:
        print("\n⚠️  一般！资产完备率达到 50% 以上，需要进一步优化。")
    else:
        print("\n❌ 警告！资产完备率低于 50%，需要大量补救工作。")

# 主函数
def main():
    print("开始资产审计...")
    print("正在扫描所有项目的 manual/ 文件夹...")
    
    # 扫描项目
    total_files, soul_pages, zombie_pages, other_pages = scan_projects()
    
    # 生成报表
    generate_report(total_files, soul_pages, zombie_pages, other_pages)

if __name__ == "__main__":
    main()