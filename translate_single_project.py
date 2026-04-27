import os
import re
import time
from deep_translator import GoogleTranslator

# 检查文本是否主要为英文
def is_primarily_english(text):
    if not text:
        return False
    english_chars = sum(1 for c in text if c.isalpha() and c.isascii() or c.isspace())
    return english_chars / len(text) > 0.6

# 保护格式的翻译函数（逐行翻译）
def translate_content(content, target_lang):
    # 保存代码块
    code_blocks = []
    code_pattern = re.compile(r'```[\s\S]*?```')
    def code_replacer(match):
        code_blocks.append(match.group(0))
        return f'__CODE_BLOCK_{len(code_blocks)-1}__'
    content = code_pattern.sub(code_replacer, content)
    
    # 保存链接
    links = []
    link_pattern = re.compile(r'\[(.*?)\]\((.*?)\)')
    def link_replacer(match):
        text = match.group(1)
        url = match.group(2)
        links.append((text, url))
        return f'__LINK_{len(links)-1}__'
    content = link_pattern.sub(link_replacer, content)
    
    # 保存占位符
    placeholders = []
    placeholder_pattern = re.compile(r'\{[^}]+\}')
    def placeholder_replacer(match):
        placeholders.append(match.group(0))
        return f'__PLACEHOLDER_{len(placeholders)-1}__'
    content = placeholder_pattern.sub(placeholder_replacer, content)
    
    # 逐行翻译
    lines = content.split('\n')
    translated_lines = []
    
    for line in lines:
        # 跳过空行
        if not line.strip():
            translated_lines.append(line)
            continue
        
        # 翻译该行
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                translator = GoogleTranslator(source='en', target=target_lang)
                translated_line = translator.translate(line)
                
                # 二次确认：如果目标是德语或西班牙语，但返回的仍然是英文，重试
                if (target_lang in ['de', 'es'] and is_primarily_english(translated_line)):
                    print(f"警告：翻译可能失败，尝试重试 ({attempt+1}/{max_attempts})")
                    time.sleep(3)
                    continue
                
                # 添加翻译延迟，避免被 Google 封禁
                time.sleep(2)
                translated_lines.append(translated_line)
                break
            except Exception as e:
                print(f"翻译失败: {e}")
                # 如果是 429 错误，等待更长时间
                if "429" in str(e):
                    print("遇到 429 错误，等待 15 秒后重试...")
                    time.sleep(15)
                else:
                    time.sleep(5)
                
                # 如果所有尝试都失败，使用原文
                if attempt == max_attempts - 1:
                    translated_lines.append(line)
    
    # 合并翻译后的行
    translated_content = '\n'.join(translated_lines)
    
    # 恢复代码块
    for i, code in enumerate(code_blocks):
        translated_content = translated_content.replace(f'__CODE_BLOCK_{i}__', code)
    
    # 恢复链接
    for i, (text, url) in enumerate(links):
        # 翻译链接文本
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                translated_text = GoogleTranslator(source='en', target=target_lang).translate(text)
                time.sleep(1)
                break
            except Exception as e:
                print(f"翻译链接文本失败: {e}")
                if "429" in str(e):
                    time.sleep(10)
                else:
                    time.sleep(3)
                if attempt == max_attempts - 1:
                    translated_text = text
        translated_content = translated_content.replace(f'__LINK_{i}__', f'[{translated_text}]({url})')
    
    # 恢复占位符
    for i, placeholder in enumerate(placeholders):
        translated_content = translated_content.replace(f'__PLACEHOLDER_{i}__', placeholder)
    
    return translated_content

# 翻译单个项目的文件
def translate_project(project_name):
    print(f"开始翻译项目: {project_name}")
    
    # 构建项目路径
    project_dir = os.path.join(os.getcwd(), project_name.lower().replace(' ', '-'))
    manual_dir = os.path.join(project_dir, 'manual')
    
    if not os.path.exists(manual_dir):
        print(f"项目 {project_name} 的 manual 目录不存在")
        return
    
    # 获取所有 .md 文件
    md_files = []
    for file in os.listdir(manual_dir):
        if file.endswith('.md'):
            md_files.append(os.path.join(manual_dir, file))
    
    print(f"找到 {len(md_files)} 个 .md 文件")
    
    # 翻译每个文件到德语
    target_lang = 'de'
    target_dir = os.path.join(manual_dir, target_lang)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    for file_path in md_files:
        print(f"\n翻译文件: {os.path.basename(file_path)}")
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 翻译内容
        translated_content = translate_content(content, target_lang)
        
        # 保存翻译后的文件
        target_file = os.path.join(target_dir, os.path.basename(file_path))
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        
        print(f"翻译完成: {target_file}")
    
    print(f"\n项目 {project_name} 的德语翻译完成！")

# 主函数
def main():
    # 选择一个项目进行翻译
    project_name = "Cron Guard"
    translate_project(project_name)

if __name__ == "__main__":
    main()
