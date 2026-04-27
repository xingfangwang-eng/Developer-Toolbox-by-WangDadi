import os
import re

def generate_advantage_description(tool_name, tool_type):
    """为工具生成优势描述"""
    descriptions = {
        'agents': f"{tool_name}是一款专业的AI代理管理工具，通过智能调度和任务自动分配，大幅提升工作效率。其核心优势在于决策树优化算法，能够根据复杂场景自动调整代理行为，实现智能化任务处理。无论是企业级应用还是个人项目，{tool_name}都能提供稳定可靠的代理服务，减少人工干预，降低运营成本。此外，其直观的用户界面和丰富的API接口，使其易于集成到现有系统中，为用户带来无缝的智能代理体验。",
        'autotask': f"{tool_name}是一款高效的任务自动化工具，通过智能识别和处理重复性任务，显著提升工作效率。其核心优势在于强大的任务调度系统，能够根据优先级和资源情况自动分配任务，确保关键任务优先处理。无论是日常办公还是复杂项目管理，{tool_name}都能提供稳定可靠的自动化解决方案，减少人工操作，降低错误率。此外，其灵活的配置选项和丰富的集成能力，使其易于适应各种业务场景，为用户带来高效便捷的自动化体验。",
        'boothell': f"{tool_name}是一款专业的启动优化工具，通过深度分析系统启动流程，识别并解决启动瓶颈，显著提升系统启动速度。其核心优势在于智能启动项管理，能够根据用户使用习惯自动优化启动顺序，减少不必要的启动项，释放系统资源。无论是个人电脑还是企业服务器，{tool_name}都能提供稳定可靠的启动优化方案，缩短启动时间，提高系统响应速度。此外，其直观的用户界面和详细的启动分析报告，使用户能够清晰了解系统启动状态，做出更明智的优化决策。",
        'cineskin': f"{tool_name}是一款专业的视频皮肤处理工具，通过先进的图像处理算法，为视频添加高质量的皮肤效果，提升视频视觉质量。其核心优势在于智能皮肤识别和美化功能，能够自动识别视频中的人物皮肤，进行自然的美化处理，同时保持原始图像的真实性。无论是专业视频制作还是个人短视频创作，{tool_name}都能提供稳定可靠的皮肤处理方案，使视频中的人物更加光彩照人。此外，其直观的操作界面和丰富的调整选项，使用户能够轻松实现专业级的皮肤效果，为视频增添魅力。",
        'fanguard': f"{tool_name}是一款专业的安全防护工具，通过实时监控和智能分析，为系统提供全方位的安全保障。其核心优势在于先进的威胁检测算法，能够快速识别并应对各种安全威胁，包括病毒、恶意软件和网络攻击。无论是个人电脑还是企业网络，{tool_name}都能提供稳定可靠的安全防护方案，保护用户数据和系统安全。此外，其轻量级设计和低资源占用，确保在提供强大防护的同时，不会影响系统性能，为用户带来安心的使用体验。",
        'humbled': f"{tool_name}是一款专业的谦逊学习工具，通过智能算法分析用户的学习行为和知识水平，为用户提供个性化的学习路径和内容推荐。其核心优势在于自适应学习系统，能够根据用户的学习进度和掌握程度，自动调整学习内容和难度，确保学习效果最大化。无论是学生还是职场人士，{tool_name}都能提供稳定可靠的学习辅助方案，帮助用户高效掌握知识，提升能力。此外，其直观的学习进度跟踪和详细的学习分析报告，使用户能够清晰了解自己的学习状态，做出更有效的学习规划。",
        'killsaas': f"{tool_name}是一款专业的SaaS管理工具，通过智能分析和优化，帮助企业降低SaaS订阅成本，提高SaaS使用效率。其核心优势在于全面的SaaS资产发现和管理功能，能够自动识别企业所有的SaaS应用，分析使用情况，优化订阅计划，减少不必要的支出。无论是大型企业还是中小型企业，{tool_name}都能提供稳定可靠的SaaS管理方案，帮助企业更好地控制SaaS支出，提升ROI。此外，其直观的管理界面和详细的使用分析报告，使企业能够清晰了解SaaS使用情况，做出更明智的决策。",
        'noadobe': f"{tool_name}是一款专业的无Adobe替代工具，通过提供与Adobe产品功能相当的功能，为用户提供低成本、高效率的创意解决方案。其核心优势在于兼容Adobe文件格式，同时提供更简洁、更直观的用户界面，降低学习成本，提高工作效率。无论是专业设计师还是创意爱好者，{tool_name}都能提供稳定可靠的创意工具，满足各种设计需求。此外，其开源特性和社区支持，使其不断进化和完善，为用户带来持续的价值。",
        'noaimd': f"{tool_name}是一款专业的无AI markdown工具，通过提供纯手工编写和管理markdown文档的功能，为用户提供更专注、更纯粹的写作体验。其核心优势在于简洁的界面和强大的编辑功能，能够满足用户对markdown文档的各种编辑需求，同时避免AI辅助带来的干扰和依赖。无论是技术文档还是个人笔记，{tool_name}都能提供稳定可靠的markdown编辑方案，帮助用户创作出高质量的文档。此外，其丰富的导出选项和版本控制功能，使用户能够轻松管理和分享文档，提升工作效率。",
        'noseotop': f"{tool_name}是一款专业的SEO优化工具，通过智能分析和优化，帮助网站提升搜索引擎排名，增加 organic流量。其核心优势在于全面的SEO分析功能，能够识别网站的SEO问题，提供针对性的优化建议，同时监控优化效果。无论是企业网站还是个人博客，{tool_name}都能提供稳定可靠的SEO优化方案，帮助网站在搜索引擎中获得更好的曝光。此外，其直观的分析报告和实时监控功能，使用户能够清晰了解网站的SEO状态，做出更有效的优化决策。",
        'rugradar': f"{tool_name}是一款专业的地毯检测工具，通过先进的图像识别算法，为用户提供地毯质量和状况的详细分析。其核心优势在于高精度的地毯缺陷检测功能，能够识别各种地毯问题，包括磨损、污渍和损坏，同时提供修复建议。无论是家庭用户还是商业场所，{tool_name}都能提供稳定可靠的地毯检测方案，帮助用户及时发现和解决地毯问题，延长地毯使用寿命。此外，其直观的检测报告和用户友好的界面，使用户能够轻松理解检测结果，做出明智的决策。"
    }
    
    # 默认描述
    default_description = f"{tool_name}是一款专业的{tool_type}工具，通过先进的技术和智能算法，为用户提供高效、可靠的解决方案。其核心优势在于强大的功能和用户友好的界面，能够满足用户在{tool_type}领域的各种需求。无论是专业用户还是初学者，{tool_name}都能提供稳定可靠的服务，帮助用户实现目标。此外，其持续的更新和改进，使其不断适应市场需求，为用户带来持续的价值。"
    
    return descriptions.get(tool_type, default_description)

def add_promotion_text(content):
    """添加推广文本"""
    promotion_text = "\n\n**👉 Ready for professional surgery? Fix your database now at: `https://wangdadi.xyz`**"
    return content + promotion_text

def process_file(file_path):
    """处理单个文件"""
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查文件是否已经包含Tool Advantages部分
        if '### Tool Advantages' in content or '## Tool Advantages' in content:
            return True
        
        # 即使文件中已经包含推广语，也需要添加Tool Advantages部分
        # 所以这里不再检查推广语
        
        # 提取工具名称和类型
        match = re.search(r'# (\w+) - (\w+)', content)
        if match:
            tool_type = match.group(1)
            tool_name = match.group(2)
        else:
            # 从文件路径提取信息
            parts = file_path.split('\\')
            tool_type = parts[-3]
            tool_name = os.path.splitext(parts[-1])[0]
        
        # 生成优势描述
        advantage_description = generate_advantage_description(tool_name, tool_type)
        
        # 找到合适的位置插入描述
        # 通常在Overview部分之后，Detailed Content部分之前
        if '## Overview' in content and '## Detailed Content' in content:
            overview_end = content.find('## Overview') + len('## Overview')
            detailed_content_start = content.find('## Detailed Content', overview_end)
            new_content = content[:detailed_content_start] + f"\n\n### Tool Advantages\n\n{advantage_description}\n\n" + content[detailed_content_start:]
        else:
            # 如果没有找到合适位置，在文件开头添加
            new_content = content + f"\n\n## Tool Advantages\n\n{advantage_description}\n\n"
        
        # 检查文件是否已经包含推广语，如果没有则添加
        if 'Ready for professional surgery? Fix your database now at:' not in content:
            new_content = add_promotion_text(new_content)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
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
                if process_file(file_path):
                    success_count += 1
                else:
                    error_count += 1
                
                # 每处理100个文件打印一次进度
                if (success_count + error_count) % 100 == 0:
                    print(f"Processed {success_count + error_count} files: {success_count} success, {error_count} error")
    
    print(f"\nProcessing complete!\nSuccess: {success_count}\nError: {error_count}")

if __name__ == "__main__":
    main()
