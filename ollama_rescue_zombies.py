import os
import json
import requests
import time
import re
from tqdm import tqdm

# 全局变量
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OLLAMA_API_ENDPOINT = "http://localhost:11434/api/generate"
MODEL = "llama3"
THREAD_COUNT = 1  # 单线程模式确保质量

# 状态文件
RECOVERY_STATUS_FILE = os.path.join(ROOT_DIR, "recovery_status.json")

# 加载恢复状态
def load_recovery_status():
    if os.path.exists(RECOVERY_STATUS_FILE):
        try:
            with open(RECOVERY_STATUS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载恢复状态失败: {e}")
            return {"processed": [], "zombie_files": []}
    return {"processed": [], "zombie_files": []}

# 保存恢复状态
def save_recovery_status(status):
    try:
        with open(RECOVERY_STATUS_FILE, 'w', encoding='utf-8') as f:
            json.dump(status, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存恢复状态失败: {e}")

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

# 收集僵尸文件
def collect_zombie_files():
    zombie_files = []
    
    # 递归扫描所有项目的 manual/ 文件夹
    for root, dirs, files in os.walk(ROOT_DIR):
        # 跳过不需要的文件夹
        dirs[:] = [d for d in dirs if d not in ['.git', 'venv', '__pycache__']]
        
        # 检查是否在 manual 文件夹中
        if 'manual' in root.split(os.sep):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    
                    # 读取文件内容
                    try:
                        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
                            content = f.read()
                        
                        # 检测页面类型
                        page_type = detect_page_type(content)
                        if page_type == "Zombie":
                            zombie_files.append(file_path)
                    except Exception as e:
                        print(f"读取文件失败 {file_path}: {e}")
    
    return zombie_files

# 识别文件语言
def detect_file_language(file_path):
    parts = file_path.split(os.sep)
    for part in parts:
        if part == "de":
            return "de"
        elif part == "es":
            return "es"
        elif part == "ja":
            return "ja"
    return "en"  # 默认英语

# 生成系统提示
def generate_system_prompt(lang):
    if lang == "de":
        return "Du bist ein führender deutscher IT-Architekt. Schreibe ausschließlich auf Deutsch. Alle technischen Begriffe müssen in deutscher Sprache formuliert werden. Vermeide jegliche englische Wörter oder Phrasen."
    elif lang == "ja":
        return "あなたは日本の経験豊富なソフトウェアエンジニアです。完全に日本語で書いてください。すべての技術用語は日本語で表現してください。英語の単語やフレーズは一切使用しないでください。"
    elif lang == "es":
        return "Eres un experto técnico latinoamericano. Escribe exclusivamente en español. Todos los términos técnicos deben estar formulados en español. Evita cualquier palabra o frase en inglés."
    else:  # en
        return "You are a senior Silicon Valley DevOps engineer. Write exclusively in English. All technical terms must be formulated in English."

# 过滤语言
def filter_language(content, lang):
    """过滤内容，确保使用正确的语言"""
    if lang == "de":
        # 移除英语单词（简单实现）
        import re
        # 保留德语技术术语，移除明显的英语单词
        english_words = set(['Describe', 'Feature', 'Step', 'function', 'class', 'import', 'def'])
        for word in english_words:
            content = re.sub(rf'\b{word}\b', '', content, flags=re.IGNORECASE)
    elif lang == "ja":
        # 移除英语单词
        import re
        # 保留日语技术术语，移除明显的英语单词
        english_words = set(['Describe', 'Feature', 'Step', 'function', 'class', 'import', 'def'])
        for word in english_words:
            content = re.sub(rf'\b{word}\b', '', content, flags=re.IGNORECASE)
    elif lang == "es":
        # 移除英语单词
        import re
        # 保留西班牙语技术术语，移除明显的英语单词
        english_words = set(['Describe', 'Feature', 'Step', 'function', 'class', 'import', 'def'])
        for word in english_words:
            content = re.sub(rf'\b{word}\b', '', content, flags=re.IGNORECASE)
    
    return content

# 提取项目信息
def extract_project_info(file_path):
    # 提取项目名
    parts = file_path.split(os.sep)
    project_name = ""
    for i, part in enumerate(parts):
        if part == "manual":
            if i > 0:
                project_name = parts[i-1]
            break
    
    # 提取文件名（不含后缀）
    file_name = os.path.basename(file_path)
    file_id = os.path.splitext(file_name)[0]
    
    # 生成关键词
    keywords = [project_name, file_id]
    if "agent" in project_name.lower():
        keywords.extend(["AI", "automation", "workflow"])
    elif "postgres" in project_name.lower():
        keywords.extend(["database", "SQL", "performance"])
    elif "cron" in project_name.lower():
        keywords.extend(["scheduling", "automation", "jobs"])
    elif "notion" in project_name.lower():
        keywords.extend(["productivity", "collaboration", "database"])
    
    return project_name, keywords

# 清理占位符
def clean_placeholders(content):
    # 定义所有占位符
    placeholders = [
        'Describe feature',
        'Step 1',
        'Beschreiben Funktion',
        'Schritt 1',
        '説明する',
        'ステップ 1',
        'Describir función',
        'Paso 1'
    ]
    
    # 移除所有占位符
    for placeholder in placeholders:
        content = content.replace(placeholder, '')
    
    # 清理多余的空行
    content = '\n'.join([line for line in content.split('\n') if line.strip()])
    
    return content

# 生成内容
def generate_content(content, project_name, keywords, lang):
    # 生成系统提示
    system_prompt = generate_system_prompt(lang)
    
    # 生成语言特定的用户提示
    if lang == "de":
        user_prompt = f"""Ich gebe dir den Projektnamen {project_name} und die Schlüsselwörter {', '.join(keywords)}.

Deine Aufgabe ist es, den folgenden Text in eine professionelle, technisch tiefe Dokumentation zu verwandeln. Füge konkrete technische Szenarien hinzu und stelle dir 3 echte technische Herausforderungen vor und gib Lösungen an.

WICHTIG: Entferne alle Platzhalter wie 'Describe feature', 'Step 1' usw. vollständig und schreibe ausschließlich auf Deutsch.

Text:
{content}

IMPORTANT: Output ONLY the Markdown content. Do NOT include any introductory text like 'Here is the translation'. No conversational filler. Just the code.
"""
    elif lang == "ja":
        user_prompt = f"""プロジェクト名 {project_name} とキーワード {', '.join(keywords)} を提供します。

以下のテキストを専門的で技術的に深いドキュメントに変換するのがあなたの役割です。具体的な技術シナリオを追加し、3つの実際の技術的課題を想像して解決策を提示してください。

重要：'Describe feature'、'Step 1' などのすべてのプレースホルダーを完全に削除し、完全に日本語で書いてください。

テキスト：
{content}

IMPORTANT: Output ONLY the Markdown content. Do NOT include any introductory text like 'Here is the translation'. No conversational filler. Just the code.
"""
    elif lang == "es":
        user_prompt = f"""Te doy el nombre del proyecto {project_name} y las palabras clave {', '.join(keywords)}.

Tu tarea es transformar el siguiente texto en una documentación profesional y técnicamente profunda. Agrega escenarios técnicos concretos e imagina 3 desafíos técnicos reales y proporciona soluciones.

IMPORTANTE: Elimina completamente todos los marcadores como 'Describe feature', 'Step 1', etc. y escribe exclusivamente en español.

Texto:
{content}

IMPORTANT: Output ONLY the Markdown content. Do NOT include any introductory text like 'Here is the translation'. No conversational filler. Just the code.
"""
    else:  # en
        user_prompt = f"""I'll give you project name {project_name} and keywords {', '.join(keywords)}.

Your task is to transform the following text into professional, technically deep documentation. Add concrete technical scenarios and imagine 3 real technical challenges and provide solutions.

IMPORTANT: Completely remove all placeholders like 'Describe feature', 'Step 1', etc. and write exclusively in English.

Text:
{content}

IMPORTANT: Output ONLY the Markdown content. Do NOT include any introductory text like 'Here is the translation'. No conversational filler. Just the code.
"""
    
    # 构建请求
    payload = {
        "model": MODEL,
        "prompt": user_prompt,
        "system": system_prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "max_tokens": 2000
        }
    }
    
    # 创建持久会话
    session = requests.Session()
    # 配置连接池
    session.mount('http://', requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=10))
    session.mount('https://', requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=10))
    
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = session.post(OLLAMA_API_ENDPOINT, json=payload, timeout=180)
            response.raise_for_status()
            result = response.json()
            generated_content = result.get("response", "")
            
            # 后处理：清理占位符和过滤语言
            cleaned_content = clean_placeholders(generated_content)
            filtered_content = filter_language(cleaned_content, lang)
            return filtered_content
        except requests.exceptions.ConnectionError:
            print(f"连接错误 (尝试 {attempt+1}/{max_retries})，正在等待 10 秒...")
            time.sleep(10)
        except requests.exceptions.HTTPError as e:
            if hasattr(e, 'response') and e.response.status_code == 502:
                print(f"502 错误 (尝试 {attempt+1}/{max_retries})，正在等待 10 秒...")
                time.sleep(10)
            else:
                print(f"HTTP 错误 (尝试 {attempt+1}/{max_retries}): {e}")
                time.sleep(5)
        except Exception as e:
            print(f"生成内容失败 (尝试 {attempt+1}/{max_retries}): {e}")
            time.sleep(5)
    
    return ""

# 质量检查
def check_quality(content, lang):
    # 检查长度（放宽到400字符）
    if len(content) < 400:
        return False, "内容长度不足 400 字符"
    
    # 检查是否包含占位符
    placeholder_patterns = [
        r'Describe feature',
        r'Step 1',
        r'Practice 1',
        r'Beschreiben Funktion',
        r'Schritt 1',
        r'説明する',
        r'ステップ 1',
        r'Describir función',
        r'Paso 1'
    ]
    
    for pattern in placeholder_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return False, "内容仍包含占位符"
    
    # 新逻辑：只要没有占位符且长度足够，就通过
    return True, "质量检查通过"

# 处理单个文件
def process_file(file_path, status):
    # 跳过已处理的文件
    if file_path in status["processed"]:
        return True
    
    # 识别语言
    lang = detect_file_language(file_path)
    
    # 读取文件内容
    try:
        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f"读取文件失败 {file_path}: {e}")
        return False
    
    # 提取项目信息
    project_name, keywords = extract_project_info(file_path)
    
    # 生成内容
    max_attempts = 2  # 减少到2次尝试
    for attempt in range(max_attempts):
        generated_content = generate_content(content, project_name, keywords, lang)
        
        # 检查质量
        quality_passed, quality_message = check_quality(generated_content, lang)
        
        if quality_passed:
            # 添加底部链接
            footer = f"\n---\n\n👉 `https://www.wangdadi.xyz/?utm_source=github_llama3`\n"
            final_content = generated_content + footer
            
            # 写入文件
            try:
                with open(file_path, 'w', encoding='utf-8-sig') as f:
                    f.write(final_content)
                
                # 更新状态
                status["processed"].append(file_path)
                save_recovery_status(status)
                return True
            except Exception as e:
                print(f"写入文件失败 {file_path}: {e}")
                return False
        else:
            print(f"质量检查失败 (尝试 {attempt+1}/{max_attempts}): {quality_message}")
            time.sleep(2)
    
    # 自动降级处理：记录到manual_fix.txt
    with open('manual_fix.txt', 'a', encoding='utf-8-sig') as f:
        f.write(f"{project_name}\n")
    print(f"项目 {project_name} 已记录到 manual_fix.txt，需要手动修复")
    return False

# 主函数
def main():
    print("开始救援僵尸页面...")
    
    # 加载状态
    status = load_recovery_status()
    
    # 收集僵尸文件
    if not status["zombie_files"]:
        print("收集僵尸文件...")
        status["zombie_files"] = collect_zombie_files()
        save_recovery_status(status)
    
    total_files = len(status["zombie_files"])
    print(f"共发现 {total_files} 个僵尸页面")
    print(f"已处理 {len(status['processed'])} 个页面")
    
    # 处理文件
    remaining_files = [f for f in status["zombie_files"] if f not in status["processed"]]
    print(f"剩余 {len(remaining_files)} 个页面需要处理")
    
    # 开始处理
    print("\n开始全量处理...")
    success_count = 0
    failure_count = 0
    
    for file_path in tqdm(remaining_files, desc="处理进度"):
        if process_file(file_path, status):
            success_count += 1
        else:
            failure_count += 1
    
    print(f"\n处理完成！")
    print(f"成功处理: {success_count} 个页面")
    print(f"处理失败: {failure_count} 个页面")
    print(f"总处理数: {success_count + failure_count} 个页面")

if __name__ == "__main__":
    main()