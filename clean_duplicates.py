import os
import re

def clean_duplicate_content(file_path):
    """清理文件中的重复内容"""
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 清理重复的Tool Advantages部分
        # 保留第一个Tool Advantages部分，删除后续的
        pattern = r'(### Tool Advantages|## Tool Advantages).*?(?=(### Tool Advantages|## Tool Advantages|$))'
        matches = re.findall(pattern, content, re.DOTALL)
        if len(matches) > 1:
            # 找到第一个Tool Advantages部分的结束位置
            first_advantage_end = content.find('### Tool Advantages')
            if first_advantage_end == -1:
                first_advantage_end = content.find('## Tool Advantages')
            
            # 找到第二个Tool Advantages部分的开始位置
            second_advantage_start = content.find('### Tool Advantages', first_advantage_end + 1)
            if second_advantage_start == -1:
                second_advantage_start = content.find('## Tool Advantages', first_advantage_end + 1)
            
            if second_advantage_start != -1:
                # 找到第二个Tool Advantages部分的结束位置
                second_advantage_end = content.find('## Detailed Content', second_advantage_start)
                if second_advantage_end == -1:
                    second_advantage_end = len(content)
                
                # 移除重复的部分
                content = content[:first_advantage_end] + content[second_advantage_end:]
        
        # 清理重复的推广语
        promotion_pattern = r'\*\*👉 Ready for professional surgery\? Fix your database now at: `https://wangdadi\.xyz`\*\*'
        promotion_matches = re.findall(promotion_pattern, content)
        if len(promotion_matches) > 1:
            # 只保留最后一个推广语
            last_promotion_start = content.rfind('**👉 Ready for professional surgery? Fix your database now at: `https://wangdadi.xyz`**')
            if last_promotion_start != -1:
                # 移除所有推广语，然后只添加最后一个
                content = re.sub(promotion_pattern, '', content)
                content += '\n\n**👉 Ready for professional surgery? Fix your database now at: `https://wangdadi.xyz`**'
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Error cleaning {file_path}: {str(e)}")
        return False

def main():
    """主函数"""
    root_dir = "e:\\Developer-Toolbox-by-WangDadi"
    success_count = 0
    error_count = 0
    
    # 遍历所有目录和文件
    for root, dirs, files in os.walk(root_dir):
        # 跳过根目录的Python文件
        if root == root_dir:
            continue
        
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                if clean_duplicate_content(file_path):
                    success_count += 1
                else:
                    error_count += 1
                
                # 每处理100个文件打印一次进度
                if (success_count + error_count) % 100 == 0:
                    print(f"Processed {success_count + error_count} files: {success_count} success, {error_count} error")
    
    print(f"\nCleaning complete!\nSuccess: {success_count}\nError: {error_count}")

if __name__ == "__main__":
    main()
