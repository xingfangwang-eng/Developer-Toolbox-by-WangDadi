import os
import json
import random
import subprocess

# 读取 projects.json 文件
def load_projects():
    projects_file = os.path.join(os.getcwd(), 'projects.json')
    with open(projects_file, 'r', encoding='utf-8') as f:
        return json.load(f)

# 生成对比文件目录
def create_vs_directory(project_dir):
    vs_dir = os.path.join(project_dir, 'manual', 'vs')
    if not os.path.exists(vs_dir):
        os.makedirs(vs_dir)
    return vs_dir

# 生成代码示例
def generate_code_example(project_name, keywords):
    project_name_lower = project_name.lower()
    
    # 数据库相关代码
    if any('postgres' in kw.lower() or 'database' in kw.lower() for kw in keywords):
        return '''```sql
-- 优化 PostgreSQL 查询示例
EXPLAIN ANALYZE SELECT * FROM users 
WHERE created_at > NOW() - INTERVAL '30 days'
AND active = true
ORDER BY last_login DESC
LIMIT 10;
```'''
    
    # Python 相关代码
    elif any('python' in kw.lower() or 'script' in kw.lower() for kw in keywords):
        return '''```python
# 自动化任务示例
import schedule
import time

def job():
    print("执行定时任务...")
    # 在这里添加你的任务逻辑

schedule.every(1).hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
```'''
    
    # JSON 相关代码
    elif any('api' in kw.lower() or 'webhook' in kw.lower() for kw in keywords):
        return '''```json
{
  "webhook": {
    "event": "payment.succeeded",
    "data": {
      "amount": 1000,
      "currency": "USD",
      "customer_id": "cus_123456"
    },
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```'''
    
    # 默认代码示例
    else:
        return '''```python
# 通用脚本示例
def process_data(data):
    """处理数据的函数"""
    results = []
    for item in data:
        if item['status'] == 'active':
            results.append(item)
    return results

# 示例用法
data = [
    {"id": 1, "status": "active", "value": 100},
    {"id": 2, "status": "inactive", "value": 200}
]

processed = process_data(data)
print(f"处理结果: {processed}")
```'''

# 生成对比文件内容
def generate_comparison_content(project_name, competitor, keywords):
    # 随机选择排版风格
    style = random.randint(1, 3)
    
    # 生成代码示例
    code_example = generate_code_example(project_name, keywords)
    
    # 风格 1
    if style == 1:
        content = f"# Best {competitor} Alternative: Why {project_name} is the Pro Choice\n\n"
        content += "## 客观对比\n\n"
        content += "我们提供客观、公正的对比，帮助您做出最适合自己的选择。\n\n"
        content += "## 核心对比\n\n"
        content += "| 特性 | {competitor} | {project_name} |\n"
        content += "|------|-------------|---------------|\n"
        content += "| Feature | 臃肿 | 精准 |\n"
        content += "| Learning Curve | 2小时 | 2秒 |\n"
        content += "| Price | $20/月订阅 | $9.9 一次性买断 |\n\n"
        content += "## 代码示例\n\n"
        content += code_example + "\n\n"
        content += "## 立即体验\n\n"
        content += "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)\n\n"
        content += "[![PayPal](https://www.paypalobjects.com/en_US/i/btn/btn_buynow_LG.gif)](https://paypal.me/)\n\n"
        content += f"## 免责声明\n\n"
        content += f"Disclaimer: {competitor} is a trademark of its respective owner. This comparison is for informational purposes based on publicly available data."
    
    # 风格 2
    elif style == 2:
        content = f"# {project_name} vs {competitor}: The Ultimate Showdown\n\n"
        content += "### 为什么选择 {project_name}？\n\n"
        content += "我们提供客观的对比分析，帮助您了解 {project_name} 如何超越 {competitor}。\n\n"
        content += "### 详细对比\n\n"
        content += "| 方面 | {competitor} | {project_name} |\n"
        content += "|------|-------------|---------------|\n"
        content += "| 专注点 | 臃肿 | 精准 |\n"
        content += "| 学习曲线 | 2小时 | 2秒 |\n"
        content += "| 价格 | $20/月订阅 | $9.9 一次性买断 |\n\n"
        content += "### 实用代码\n\n"
        content += code_example + "\n\n"
        content += "### 开始使用\n\n"
        content += "[Open In Colab](https://colab.research.google.com/)\n\n"
        content += "[Buy Now](https://paypal.me/)\n\n"
        content += f"### 法律声明\n\n"
        content += f"Disclaimer: {competitor} is a trademark of its respective owner. This comparison is for informational purposes based on publicly available data."
    
    # 风格 3
    else:
        content = f"# {project_name}: The Superior Alternative to {competitor}\n\n"
        content += "## 对比分析\n\n"
        content += "我们的分析基于公开数据，旨在帮助您做出明智的选择。\n\n"
        content += "## 特性对比\n\n"
        content += "| 特性 | {competitor} | {project_name} |\n"
        content += "|------|-------------|---------------|\n"
        content += "| 功能专注 | 臃肿 | 精准 |\n"
        content += "| 上手难度 | 2小时 | 2秒 |\n"
        content += "| 定价模式 | $20/月订阅 | $9.9 一次性买断 |\n\n"
        content += "## 代码示例\n\n"
        content += code_example + "\n\n"
        content += "## 立即行动\n\n"
        content += "<a href='https://colab.research.google.com/' target='_blank'>Open In Colab</a>\n\n"
        content += "<a href='https://paypal.me/' target='_blank'>Buy Now</a>\n\n"
        content += f"## 免责声明\n\n"
        content += f"Disclaimer: {competitor} is a trademark of its respective owner. This comparison is for informational purposes based on publicly available data."
    
    return content

# 生成对比文件
def generate_comparison_files():
    projects = load_projects()
    total_files = 0
    
    for project in projects:
        project_name = project['name']
        project_dir = os.path.join(os.getcwd(), project_name.lower().replace(' ', '-'))
        
        # 检查项目目录是否存在
        if not os.path.exists(project_dir):
            continue
        
        # 创建 vs 目录
        vs_dir = create_vs_directory(project_dir)
        
        # 获取竞争对手
        competitors = project.get('competitors', [])
        
        # 为每个竞争对手生成对比文件
        for competitor in competitors:
            # 生成文件名
            file_name = f"{competitor.lower().replace(' ', '-')}.md"
            file_path = os.path.join(vs_dir, file_name)
            
            # 生成内容
            content = generate_comparison_content(project_name, competitor, project['keywords'])
            
            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            total_files += 1
            print(f"生成文件: {file_path}")
    
    return total_files

# 调用 global_exploit.py 进行翻译
def translate_files():
    print("\n开始翻译对比文件...")
    result = subprocess.run(['python', 'global_exploit.py'], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("翻译过程中的错误:")
        print(result.stderr)

# 主函数
def main():
    print("开始生成竞品对比文件...")
    total_files = generate_comparison_files()
    print(f"\n生成完成！共生成 {total_files} 个对比文件。")
    
    # 翻译文件
    translate_files()
    
    print("\n所有任务完成！")

if __name__ == "__main__":
    main()
