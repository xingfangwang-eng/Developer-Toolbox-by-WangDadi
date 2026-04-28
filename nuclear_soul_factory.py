#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nuclear Soul Factory - 核平重写
使用 Gemini REST API 暴力处理所有僵尸文件
"""

import os
import re
import time
import json
import requests
from tqdm import tqdm

# 配置
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# 检查环境变量
if not GEMINI_API_KEY:
    print("错误：请设置 GEMINI_API_KEY 环境变量")
    exit(1)

# 文件路径
ZOMBIE_FILE = "zombie_files.txt"
CHECKPOINT_FILE = "cleared_zombies.log"

# 语言目录
LANG_DIRS = ['de', 'es', 'ja']

def detect_language(file_path):
    """检测文件语言"""
    path = file_path.replace('\\', '/')
    for lang in LANG_DIRS:
        if f'/{lang}/' in path:
            return lang
    return 'en'

def extract_project_name(file_path):
    """从路径提取项目名"""
    parts = file_path.replace('\\', '/').split('/')
    for i, part in enumerate(parts):
        if part == 'manual':
            if i > 0:
                return parts[i-1]
            break
    return os.path.basename(os.path.dirname(file_path))

def generate_system_prompt(lang):
    """生成系统提示"""
    if lang == "de":
        return "Du bist ein führender deutscher IT-Architekt. Schreibe ausschließlich auf Deutsch. Alle technischen Begriffe müssen in deutscher Sprache formuliert werden."
    elif lang == "ja":
        return "あなたは日本の経験豊富なソフトウェアエンジニアです。完全に日本語で書いてください。すべての技術用語は日本語で表現してください。"
    elif lang == "es":
        return "Eres un experto técnico latinoamericano. Escribe exclusivamente en español. Todos los términos técnicos deben estar formulados en español."
    else:
        return "You are a senior Silicon Valley DevOps engineer. Write exclusively in English. All technical terms must be formulated in English."

def generate_content(project_name, lang):
    """调用 Gemini REST API 生成内容"""
    system_prompt = generate_system_prompt(lang)
    
    user_prompt = f"""根据项目名 '{project_name}'，生成一份详细的技术功能描述文档（{lang}语言）。

要求：
- 字数至少 300 字
- 包含具体的技术场景和使用案例
- 使用地道的专业技术用语
- 保持 Markdown 格式
- 严禁出现 'Describe', 'Feature', 'Step' 等占位符词汇

输出格式：
## 功能概述
<详细的功能描述>

## 技术特性
<列出主要技术特性>

## 使用场景
<描述典型使用场景>
"""
    
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": user_prompt
                    }
                ]
            }
        ],
        "systemInstruction": {
            "parts": [{"text": system_prompt}]
        },
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2000
        },
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    }
    
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    max_retries = 5
    for attempt in range(max_retries):
        try:
            # 严格限速：每次请求前等待 4.5 秒，确保每分钟 ≤ 14 次请求
            time.sleep(4.5)
            
            response = requests.post(
                f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}",
                json=payload,
                headers=headers,
                timeout=60
            )
            
            if response.status_code != 200:
                print(f"API 返回错误: {response.status_code}")
                print(f"错误响应: {response.text}")
                time.sleep(5)
                continue
            
            result = response.json()
            candidates = result.get('candidates', [])
            if candidates:
                content = candidates[0].get('content', {}).get('parts', [])
                if content:
                    text = content[0].get('text', '')
                    if len(text) >= 300:
                        return text
                    else:
                        print(f"内容长度不足 300 字符，重试...")
                        time.sleep(2)
                        continue
            
            time.sleep(2)
        except Exception as e:
            print(f"请求失败 (尝试 {attempt+1}/{max_retries}): {e}")
            time.sleep(5)
    
    return ""

def load_checkpoint():
    """加载已处理文件列表"""
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_checkpoint(file_path):
    """保存已处理文件"""
    with open(CHECKPOINT_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{file_path}\n")

def load_zombie_files():
    """加载僵尸文件列表"""
    if not os.path.exists(ZOMBIE_FILE):
        print(f"错误：找不到 {ZOMBIE_FILE}")
        return []
    
    with open(ZOMBIE_FILE, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def process_file(file_path):
    """处理单个文件"""
    # 检测语言
    lang = detect_language(file_path)
    
    # 提取项目名
    project_name = extract_project_name(file_path)
    print(f"处理: {file_path} | 项目: {project_name} | 语言: {lang}")
    
    # 生成内容
    generated_content = generate_content(project_name, lang)
    
    if not generated_content:
        print(f"❌ 生成失败: {file_path}")
        return False
    
    # 添加底部链接
    footer = f"\n---\n\n👉 `https://www.wangdadi.xyz/?utm_source=github_nuclear`\n"
    final_content = generated_content + footer
    
    # 写入文件
    try:
        with open(file_path, 'w', encoding='utf-8-sig') as f:
            f.write(final_content)
        print(f"✅ 处理成功: {file_path}")
        return True
    except Exception as e:
        print(f"❌ 写入失败: {file_path} - {e}")
        return False

def main():
    print("Nuclear Soul Factory 启动")
    print("=" * 60)
    
    # 加载已处理文件
    cleared_files = load_checkpoint()
    print(f"已处理文件数: {len(cleared_files)}")
    
    # 加载僵尸文件列表
    zombie_files = load_zombie_files()
    print(f"僵尸文件总数: {len(zombie_files)}")
    
    # 过滤已处理文件
    remaining_files = [f for f in zombie_files if f not in cleared_files]
    print(f"待处理文件数: {len(remaining_files)}")
    
    if not remaining_files:
        print("所有僵尸文件已处理完毕！")
        return
    
    # 开始处理
    processed_count = 0
    for file_path in tqdm(remaining_files, desc="核平重写进度"):
        if process_file(file_path):
            save_checkpoint(file_path)
            processed_count += 1
            
            # 每处理 10 个文件打印一次进度
            if processed_count % 10 == 0:
                print(f"\n已处理: {processed_count} / {len(remaining_files)}")
    
    print(f"\n处理完成！共处理 {processed_count} 个文件")

if __name__ == "__main__":
    main()
