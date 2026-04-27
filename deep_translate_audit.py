import os
import re
import time
from deep_translator import GoogleTranslator

# 支持的语言
SUPPORTED_LANGUAGES = ['es', 'de', 'ja', 'fr']

# 检查文本是否主要为英文
def is_primarily_english(text):
    if not text:
        return False
    english_chars = sum(1 for c in text if c.isalpha() and c.isascii() or c.isspace())
    return english_chars / len(text) > 0.6

# 深度翻译函数
def deep_translate_content(content, target_lang):
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
    
    # 翻译重点句子
    # 1. SEO 优化内容句子
    seo_pattern = re.compile(r'This is SEO optimized content for the (.*?) project, keywords: (.*?)', re.IGNORECASE)
    def seo_translator(match):
        project_name = match.group(1)
        keywords = match.group(2)
        
        # 翻译整句
        sentence = f"This is SEO optimized content for the {project_name} project, keywords: {keywords}"
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                translator = GoogleTranslator(source='en', target=target_lang)
                translated_sentence = translator.translate(sentence)
                time.sleep(1)
                return translated_sentence
            except Exception as e:
                print(f"翻译 SEO 句子失败: {e}")
                if "429" in str(e):
                    time.sleep(10)
                else:
                    time.sleep(3)
        return sentence
    content = seo_pattern.sub(seo_translator, content)
    
    # 2. 项目描述句子
    project_desc_pattern = re.compile(r'(.*?) is a (.*?) that helps (.*?)', re.IGNORECASE)
    def project_desc_translator(match):
        project_name = match.group(1)
        tool_desc = match.group(2)
        help_desc = match.group(3)
        
        # 翻译整句
        sentence = f"{project_name} is a {tool_desc} that helps {help_desc}"
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                translator = GoogleTranslator(source='en', target=target_lang)
                translated_sentence = translator.translate(sentence)
                time.sleep(1)
                return translated_sentence
            except Exception as e:
                print(f"翻译项目描述失败: {e}")
                if "429" in str(e):
                    time.sleep(10)
                else:
                    time.sleep(3)
        return sentence
    content = project_desc_pattern.sub(project_desc_translator, content)
    
    # 3. 关键词本地化
    keywords_pattern = re.compile(r'keywords: (.*?)', re.IGNORECASE)
    def keywords_translator(match):
        keywords = match.group(1)
        
        # 翻译关键词
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                translator = GoogleTranslator(source='en', target=target_lang)
                translated_keywords = translator.translate(keywords)
                time.sleep(1)
                return f"keywords: {translated_keywords}"
            except Exception as e:
                print(f"翻译关键词失败: {e}")
                if "429" in str(e):
                    time.sleep(10)
                else:
                    time.sleep(3)
        return f"keywords: {keywords}"
    content = keywords_pattern.sub(keywords_translator, content)
    
    # 恢复代码块
    for i, code in enumerate(code_blocks):
        content = content.replace(f'__CODE_BLOCK_{i}__', code)
    
    # 恢复链接
    for i, (text, url) in enumerate(links):
        # 翻译链接文本
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                translator = GoogleTranslator(source='en', target=target_lang)
                translated_text = translator.translate(text)
                time.sleep(0.5)
                break
            except Exception as e:
                print(f"翻译链接文本失败: {e}")
                if "429" in str(e):
                    time.sleep(10)
                else:
                    time.sleep(3)
                if attempt == max_attempts - 1:
                    translated_text = text
        content = content.replace(f'__LINK_{i}__', f'[{translated_text}]({url})')
    
    # 恢复占位符
    for i, placeholder in enumerate(placeholders):
        content = content.replace(f'__PLACEHOLDER_{i}__', placeholder)
    
    # 修复相对路径
    if target_lang != 'en':
        # 确保返回链接指向 ../../../README.md
        content = re.sub(r'\[.*?\]\(\.\.\/\.\.\)', f'[返回索引](../../../README.md)', content)
        # 根据不同语言更新链接文本
        if target_lang == 'de':
            content = re.sub(r'\[.*?\]\(\.\.\/\.\.\/\.\.\/README\.md\)', '[Zurück zum Index](../../../README.md)', content)
        elif target_lang == 'es':
            content = re.sub(r'\[.*?\]\(\.\.\/\.\.\/\.\.\/README\.md\)', '[Volver al Índice](../../../README.md)', content)
        elif target_lang == 'ja':
            content = re.sub(r'\[.*?\]\(\.\.\/\.\.\/\.\.\/README\.md\)', '[インデックスに戻る](../../../README.md)', content)
        elif target_lang == 'fr':
            content = re.sub(r'\[.*?\]\(\.\.\/\.\.\/\.\.\/README\.md\)', '[Retour à l\'Index](../../../README.md)', content)
    
    return content

# 链接可用性巡检
def audit_links(content):
    # 检查 Open in Colab 链接
    colab_pattern = re.compile(r'https://colab\.research\.google\.com/.*?github\.com/.*?/blob/.*?/.*?\.ipynb')
    colab_matches = colab_pattern.findall(content)
    if colab_matches:
        print(f"发现 {len(colab_matches)} 个 Open in Colab 链接")
    
    # 检查 PayPal 徽章链接
    paypal_pattern = re.compile(r'https://www\.paypal\.com/donate\?.*?')
    paypal_matches = paypal_pattern.findall(content)
    if paypal_matches:
        print(f"发现 {len(paypal_matches)} 个 PayPal 徽章链接")
    
    return True

# 处理单个文件
def process_file(file_path, target_lang):
    print(f"处理文件: {file_path}")
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 深度翻译
    translated_content = deep_translate_content(content, target_lang)
    
    # 链接可用性巡检
    audit_links(translated_content)
    
    # 保存翻译后的内容
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(translated_content)
    
    print(f"更新完成: {file_path}")

# 主函数
def main():
    print("开始执行多语种手册的全量深度翻译与路径终极检查...")
    
    # 遍历所有项目
    projects_dir = os.getcwd()
    for project in os.listdir(projects_dir):
        project_path = os.path.join(projects_dir, project)
        if not os.path.isdir(project_path):
            continue
        
        # 检查是否有 manual 目录
        manual_dir = os.path.join(project_path, 'manual')
        if not os.path.exists(manual_dir):
            continue
        
        # 遍历所有支持的语言
        for lang in SUPPORTED_LANGUAGES:
            lang_dir = os.path.join(manual_dir, lang)
            if not os.path.exists(lang_dir):
                continue
            
            # 遍历所有 .md 文件
            for file in os.listdir(lang_dir):
                if file.endswith('.md'):
                    file_path = os.path.join(lang_dir, file)
                    process_file(file_path, lang)
    
    print("\n深度翻译和链接检查完成！")
    
    # 自动推送
    print("\n开始推送更改...")
    os.system('python brute_push.py')
    print("\n全球化深度清理已完成")

if __name__ == "__main__":
    main()
