#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama Local Cleanup - 工业级长跑版
使用本地 Ollama (llama3) 进行灵魂注入
单线程顺序执行，超时300秒，自动清场
"""

import os
import re
import time
import json
import requests
from tqdm import tqdm

# 配置
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_TAGS_URL = "http://127.0.0.1:11434/api/tags"
MODEL_NAME = "llama3"
SUCCESS_LOG = "success.log"
FINAL_SOUL_LOG = "final_soul.log"

# 扫描根目录
ROOT_DIR = "E:\\Developer-Toolbox-by-WangDadi"

# 僵尸检测关键词（零容忍检测）
ZOMBIE_KEYWORDS = [
    'Describe feature', 'Describe', 'Step 1', 'Step 2', 'Step 3',
    'Practice 1', 'Place-holder', 'placeholder', 'TOO_',
    'Beschreiben', 'Schritt', 'Funktion', 'Erklärung',
    '説明', 'ステップ', '機能', '説明する', 'を説明する',
    'Describir', 'Paso', 'Función', 'Descripción'
]

# 语言目录映射
LANG_DIRS = {
    'de': {'code': 'de', 'name': 'Deutsch', 'prompt': '德语'},
    'es': {'code': 'es', 'name': 'Español', 'prompt': '西班牙语'},
    'ja': {'code': 'ja', 'name': '日本語', 'prompt': '日语'},
    'en': {'code': 'en', 'name': 'English', 'prompt': '英语'}
}

def is_zombie(content):
    """检测文件是否为僵尸文件（零容忍）"""
    content_lower = content.lower()
    
    # 关键词检测
    for keyword in ZOMBIE_KEYWORDS:
        if keyword.lower() in content_lower:
            return True
    
    # 字符数少于400的直接判定为僵尸
    if len(content) < 400:
        return True
    
    return False

def contains_forbidden(content):
    """检测是否包含禁止词汇（零容忍）"""
    forbidden = [
        'describe', 'place-holder', 'placeholder', '説明', '説明する',
        'feature 1', 'feature 2', 'feature 3', '功能点一', '功能点二', '功能点三',
        '解释功能', '功能一', '功能二', '功能三'
    ]
    content_lower = content.lower()
    for word in forbidden:
        if word.lower() in content_lower:
            return True
    return False

def detect_language(file_path):
    """检测文件语言"""
    path = file_path.replace('\\', '/')
    for lang_code in LANG_DIRS:
        if f'/{lang_code}/' in path:
            return lang_code
    return 'en'

def extract_project_name(file_path):
    """从路径提取项目名"""
    parts = file_path.replace('\\', '/').split('/')
    for i, part in enumerate(parts):
        if part == 'manual':
            if i > 0:
                return parts[i-1]
            break
    # 默认返回上级目录名
    dir_path = os.path.dirname(file_path)
    return os.path.basename(dir_path)

def is_vague_project_name(name):
    """检测项目名是否模糊/无意义"""
    vague_patterns = ['test', 'abc', 'demo', 'sample', 'temp', 'tmp', 'unk', 'unknown', 'project', 'my', 'new', 'untitled']
    name_lower = name.lower()
    return any(pattern in name_lower for pattern in vague_patterns)

def build_prompt(project_name, lang):
    """构建核爆级 Prompt（职业想象版）"""
    lang_info = LANG_DIRS.get(lang, LANG_DIRS['en'])
    
    # 如果项目名模糊，强制设定为高性能企业级云原生自动化工具
    if is_vague_project_name(project_name):
        project_desc = "高性能企业级云原生自动化工具（分布式锁支持、零拷贝内存优化、自动分片索引）"
        creative_setting = "【强制设定】你正在描述的是一个同级别的明星产品，必须凭空创造出令人惊叹的技术亮点。"
    else:
        project_desc = project_name
        creative_setting = ""
    
    prompt = f"""你是一个年薪百万的资深技术产品经理。

项目名：{project_desc}，语言：{lang_info['prompt']}。
{creative_setting}

任务：根据项目名，发挥你的顶级专业想象力，完全重构这篇技术手册。

【强制要求】：
1. 如果原始项目名模糊（如testproject、abc等），你必须将其想象成一个同级别的产品，凭空创造出3个非常硬核的技术亮点。
2. 严禁出现 'Describe', 'Place-holder', '説明', '説明する', 'feature 1', 'feature 2', 'feature 3' 或任何翻译腔词汇。
3. 严禁出现'功能点一'、'功能点二'、'功能点三'、'解释功能'等机械式表达。
4. 你写出的每一句话都必须像苹果、亚马逊或Stripe官网那样具有煽动性的技术说明。
5. 必须包含 3 个真实、硬核的技术功能点（每点至少 80 字）。
6. 必须包含 3 个详细的操作步骤和 2 个专家级性能优化建议。
7. 直接输出地道的 {lang_info['prompt']} Markdown 格式内容。
8. 底部必须保留推广链接：`https://www.wangdadi.xyz`

输出结构：
## 功能概述
<项目的核心价值和定位>

## 核心功能
### 功能亮点一
<详细描述，至少 80 字，必须像官网产品介绍那样具有煽动性>

### 功能亮点二
<详细描述，至少 80 字，必须像官网产品介绍那样具有煽动性>

### 功能亮点三
<详细描述，至少 80 字，必须像官网产品介绍那样具有煽动性>

## 快速开始
### 步骤一：安装配置
<详细步骤>

### 步骤二：初始化
<详细步骤>

### 步骤三：运行验证
<详细步骤>

## 专家建议
### 性能优化建议一
<专家级建议>

### 性能优化建议二
<专家级建议>

---

👉 `https://www.wangdadi.xyz`
"""
    return prompt

def load_success_log():
    """加载成功记录日志"""
    success_files = set()
    if os.path.exists(SUCCESS_LOG):
        try:
            with open(SUCCESS_LOG, 'r', encoding='utf-8') as f:
                success_files = set(line.strip() for line in f if line.strip())
        except Exception as e:
            print(f"⚠️ 读取成功日志失败: {e}")
    return success_files

def append_success_log(file_path):
    """追加成功记录到日志"""
    try:
        with open(SUCCESS_LOG, 'a', encoding='utf-8') as f:
            f.write(file_path + '\n')
    except Exception as e:
        print(f"⚠️ 写入成功日志失败: {e}")

def load_final_soul_log():
    """加载最终成功记录日志"""
    success_files = set()
    if os.path.exists(FINAL_SOUL_LOG):
        try:
            with open(FINAL_SOUL_LOG, 'r', encoding='utf-8') as f:
                success_files = set(line.strip() for line in f if line.strip())
        except Exception as e:
            print(f"⚠️ 读取最终日志失败: {e}")
    return success_files

def append_final_soul_log(file_path):
    """追加最终成功记录到日志"""
    try:
        with open(FINAL_SOUL_LOG, 'a', encoding='utf-8') as f:
            f.write(file_path + '\n')
    except Exception as e:
        print(f"⚠️ 写入最终日志失败: {e}")

def check_ollama_connection():
    """连接自检：验证 Ollama 服务是否可用"""
    print("🔍 正在检查 Ollama 服务连接...")
    try:
        response = requests.get(OLLAMA_TAGS_URL, timeout=10)
        if response.status_code == 200:
            print("✅ Ollama 服务连接正常")
            return True
        else:
            print(f"❌ Ollama 服务返回错误: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到 Ollama 服务")
        return False
    except Exception as e:
        print(f"❌ 连接检查失败: {e}")
        return False

def call_ollama(prompt):
    """调用本地 Ollama API（带重试机制）"""
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 1024
        }
    }
    
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = requests.post(OLLAMA_URL, json=payload, timeout=300)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            elif response.status_code == 502:
                print(f"⚠️ 502 错误，休眠 15 秒后重新检测服务状态... ({attempt+1}/{max_retries})")
                time.sleep(15)
                if not check_ollama_connection():
                    print("❌ Ollama 服务已死亡！脚本停止！")
                    return "__ENGINE_DEAD__"
                continue
            else:
                print(f"⚠️ API 返回错误: {response.status_code}")
                return ""
                
        except requests.exceptions.ConnectionError:
            print(f"⚠️ 连接失败，休眠 15 秒后重新检测服务状态... ({attempt+1}/{max_retries})")
            time.sleep(15)
            if not check_ollama_connection():
                print("❌ Ollama 服务已死亡！脚本停止！")
                return "__ENGINE_DEAD__"
            continue
        except requests.exceptions.Timeout:
            print(f"⚠️ 请求超时，休眠 15 秒后重新检测服务状态... ({attempt+1}/{max_retries})")
            time.sleep(15)
            if not check_ollama_connection():
                print("❌ Ollama 服务已死亡！脚本停止！")
                return "__ENGINE_DEAD__"
            continue
        except Exception as e:
            print(f"⚠️ 请求失败: {e}")
            return ""
    
    return ""

def process_file(file_path):
    """处理单个文件（工业级灵魂注入）"""
    # 确保使用绝对路径
    abs_file_path = os.path.abspath(file_path)
    # 读取原始内容
    try:
        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 读取失败: {file_path} - {e}")
        return False
    
    # 检测是否为僵尸文件
    if not is_zombie(content):
        return False
    
    # 检测语言
    lang = detect_language(file_path)
    lang_info = LANG_DIRS.get(lang, LANG_DIRS['en'])
    
    # 提取项目名
    project_name = extract_project_name(file_path)
    
    print(f"\n🧟 发现僵尸: {os.path.basename(file_path)}")
    print(f"   项目: {project_name} | 语言: {lang_info['name']}")
    
    # 构建 Prompt
    prompt = build_prompt(project_name, lang)
    
    # 质量校验循环（强化版：5次重试 + 自动化验货）
    max_retries = 5
    for attempt in range(max_retries):
        print(f"   生成中... (尝试 {attempt+1}/{max_retries})")
        
        # 调用 Ollama
        generated_content = call_ollama(prompt)
        
        if generated_content == "__ENGINE_DEAD__":
            print("❌ Ollama 引擎已死亡，脚本强制停止！")
            return "__ENGINE_DEAD__"
        
        if not generated_content:
            print(f"   ⚠️ 生成结果为空，等待后重试...")
            time.sleep(5)
            continue
        
        # 字数检查
        if len(generated_content) < 300:
            print(f"   ⚠️ 内容过短 ({len(generated_content)}字)，打回重写...")
            time.sleep(3)
            continue
        
        # 关键词二次拦截
        if contains_forbidden(generated_content):
            print(f"   ⚠️ 检测到禁止词汇，打回重写...")
            time.sleep(3)
            continue
        
        # 确保底部有链接
        if 'https://www.wangdadi.xyz' not in generated_content:
            generated_content += f"\n\n---\n\n👉 `https://www.wangdadi.xyz`\n"
        
        # 写入文件（实时落地）
        try:
            with open(file_path, 'w', encoding='utf-8-sig') as f:
                f.write(generated_content)
        except Exception as e:
            print(f"   ❌ 写入失败: {file_path} - {e}")
            return False
        
        # 【自动化验货】读取文件验证质量
        try:
            with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
                verified_content = f.read()
            
            # 验货项目：检查是否仍含有僵尸词汇
            quality_check_failed = False
            quality_issues = []
            
            if '説明' in verified_content or '説明する' in verified_content or 'を説明する' in verified_content:
                quality_issues.append('説明')
                quality_check_failed = True
            
            if 'feature 1' in verified_content.lower() or 'feature 2' in verified_content.lower() or 'feature 3' in verified_content.lower():
                quality_issues.append('feature N')
                quality_check_failed = True
            
            if '功能点一' in verified_content or '功能点二' in verified_content or '功能点三' in verified_content:
                quality_issues.append('功能点')
                quality_check_failed = True
            
            if len(verified_content) < 400:
                quality_issues.append(f'字数不足({len(verified_content)})')
                quality_check_failed = True
            
            if quality_check_failed:
                print(f"   ⚠️ 验货失败: {', '.join(quality_issues)}，打回重写...")
                time.sleep(3)
                continue
            
        except Exception as e:
            print(f"   ⚠️ 验货读取失败: {e}")
        
        # 所有校验通过
        print(f"   ✅ 验货通过！")
        print(f"✅ [Success] 已在本地注入灵魂: {file_path}")
        
        # 记录到成功日志（绝对路径）
        append_success_log(abs_file_path)
        # 记录到最终灵魂日志（绝对路径）
        append_final_soul_log(abs_file_path)
        
        return True
    else:
        print(f"❌ 多次重试仍不合格，跳过: {file_path}")
        return False

def find_markdown_files(root_dir):
    """查找所有 .md 文件"""
    md_files = []
    
    for root, dirs, files in os.walk(root_dir):
        # 跳过隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    
    return md_files

def main():
    print("Ollama Local Cleanup - 灵魂注入仪式启动")
    print("=" * 60)
    print(f"扫描目录: {ROOT_DIR}")
    print(f"Ollama 模型: {MODEL_NAME}")
    print("=" * 60)
    
    # 连接自检
    if not check_ollama_connection():
        print("\n❌ 请先运行 'ollama serve' 命令！")
        return
    
    # 加载成功日志
    success_files = load_success_log()
    final_soul_files = load_final_soul_log()
    all_processed = success_files.union(final_soul_files)
    print(f"📋 已加载 {len(all_processed)} 个已处理文件记录（success.log + final_soul.log）")
    
    # 查找所有 .md 文件
    all_md_files = find_markdown_files(ROOT_DIR)
    print(f"\n发现 {len(all_md_files)} 个 Markdown 文件")
    
    # 筛选僵尸文件
    zombie_files = []
    print("正在扫描僵尸文件...")
    for file_path in tqdm(all_md_files):
        # 跳过已处理的文件
        if file_path in all_processed:
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
                content = f.read()
            if is_zombie(content):
                zombie_files.append(file_path)
        except Exception as e:
            pass
    
    print(f"\n发现 {len(zombie_files)} 个僵尸文件需要处理")
    
    if not zombie_files:
        print("🎉 没有僵尸文件，任务完成！")
        return
    
    # 工业级长跑版清理（单线程顺序处理）
    success_count = 0
    failed_count = 0
    engine_dead = False
    
    print("\n开始灵魂注入（工业级长跑版）...")
    for file_path in tqdm(zombie_files, desc="清理进度"):
        # 【自动清场】处理每个文件前先检测 Ollama 引擎状态
        print(f"\n🔍 检测 Ollama 引擎状态...")
        if not check_ollama_connection():
            print("❌ Ollama 引擎已死亡！警报！脚本停止！")
            engine_dead = True
            break
        
        result = process_file(file_path)
        
        if result == "__ENGINE_DEAD__":
            print("❌ Ollama 引擎已死亡！警报！脚本停止！")
            engine_dead = True
            break
        elif result:
            success_count += 1
        else:
            failed_count += 1
        
        # 每处理 10 个文件显示一次统计
        if (success_count + failed_count) % 10 == 0:
            print(f"\n📊 进度统计: 成功 {success_count} | 失败 {failed_count}")
    
    print("\n" + "=" * 60)
    if engine_dead:
        print(f"⚠️ 引擎死亡中断！")
        print(f"✅ 成功完成: {success_count} 个文件")
        print(f"❌ 失败跳过: {failed_count} 个文件")
    else:
        print(f"任务完成！")
        print(f"✅ 成功重塑: {success_count} 个文件")
        print(f"❌ 失败跳过: {failed_count} 个文件")
    print("=" * 60)

if __name__ == "__main__":
    main()
