import os
import json
import requests

# 全局变量
API_KEY = "sk-acea097d87da45508303b0662a398434"
API_ENDPOINT = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"

# 清理无效 Unicode 字符
def clean_unicode(text):
    return ''.join(c for c in text if ord(c) >= 32 or c in '\n\t')

# 调用 DeepSeek API 生成内容
def generate_content():
    prompt = """You are the chief architect of champions-sp-calc, a tool for calculating hero skill points in games. Please create a comprehensive Japanese technical document for this project with the following sections:

1. Project Overview
2. Core Features (3 technical features with specific parameters and metrics)
3. Operation Steps (3 detailed steps)
4. Best Practices (2 industry recommendations)
5. Related Resources (with link to https://www.wangdadi.xyz/?utm_source=github)

Write in authentic Japanese and include technical details like millisecond-level calculations, PostgreSQL integration, etc."""
    
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

# 主函数
def main():
    # 目标文件路径
    target_file = "e:\Developer-Toolbox-by-WangDadi\champions-sp-calc\manual\ja\CHA_013.md"
    
    # 生成内容
    content = generate_content()
    
    if content:
        # 清理内容
        cleaned_content = clean_unicode(content)
        
        # 写入文件，使用 utf-8-sig 编码
        with open(target_file, 'w', encoding='utf-8-sig') as f:
            f.write(cleaned_content)
        
        print("文件已成功重写并使用 utf-8-sig 编码保存！")
        print("\n生成的内容:")
        print(cleaned_content)
    else:
        print("生成内容失败！")

if __name__ == "__main__":
    main()