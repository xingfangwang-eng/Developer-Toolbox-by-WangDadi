import os
import json
import requests

# 全局变量
API_KEY = "sk-acea097d87da45508303b0662a398434"
API_ENDPOINT = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"

# 从路径中提取项目名和语言
def extract_info(file_path):
    # 提取项目名（文件夹名）
    parts = file_path.split(os.sep)
    project_name = "test-project"
    lang = "en"
    return project_name, lang

# 调用 DeepSeek API 重写内容
def rewrite_content(content, project_name, keywords, lang):
    prompt = '你不再是翻译官，你是这个项目的首席架构师。\n项目名：' + project_name + '，关键词：' + keywords + '，目标语言：' + lang + '。\n请彻底重写这段 Markdown，要求如下：\n1. 严禁翻译原本的 "Describe feature" 或 "説明する" 等词汇。\n2. 根据项目名和关键词，发挥想象力编写 3 个真实的、硬核的技术功能。例如：如果是 champions-sp-calc，你应该写它如何精准计算英雄技能点分配、支持多版本数据对比等。\n3. 必须包含具体的参数名、技术指标（如：ミリ秒単位の計算、PostgreSQLとの連携）。\n4. 语言必须是 100% 地道的 ' + lang + '。\n5. 彻底删除 Related Resources 里所有包含 example.com 的假链接。\n6. 替换为：👉 `https://www.wangdadi.xyz/?utm_source=github`。\n7. 必须生成 3 个详细的操作步骤，内容要显得极度专业。\n8. 生成 2 个针对该工具的行业最佳实践建议。\n9. 直接输出正文，不要包含任何"好的，这是重写后的内容"之类的废话。\n\n原文：\n' + content
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2000,
        "temperature": 0.7
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    try:
        response = requests.post(API_ENDPOINT, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"API 请求失败: {e}")
        return None

# 处理单个文件
def process_file(file_path):
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
            content = f.read()
        
        # 提取项目信息
        project_name, lang = extract_info(file_path)
        
        # 调用 API 重写
        rewritten_content = rewrite_content(content, project_name, "test,demo", lang)
        
        if rewritten_content:
            # 写入新内容
            with open(file_path, 'w', encoding='utf-8-sig') as f:
                f.write(rewritten_content)
            
            print("文件重写成功！")
            print("\n重写后的内容：")
            print(rewritten_content)
            return True
    except Exception as e:
        print(f"处理文件失败 {file_path}: {e}")
    
    return False

# 主函数
def main():
    test_file = "test_sample.md"
    print(f"正在处理测试文件: {test_file}")
    process_file(test_file)

if __name__ == "__main__":
    main()
