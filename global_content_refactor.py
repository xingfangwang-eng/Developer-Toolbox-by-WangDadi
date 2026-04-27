import os
import json
import re

# 读取项目配置
with open('projects.json', 'r', encoding='utf-8') as f:
    projects = json.load(f)

# 项目内容生成逻辑
project_content_templates = {
    "Cron Guard": {
        "focus_areas": [
            "自动化调度与监控",
            "任务执行失败处理",
            "性能优化与资源管理",
            "多环境部署策略",
            "安全性与权限控制"
        ],
        "features": [
            "智能任务调度系统",
            "实时监控与告警",
            "失败重试机制",
            "资源使用分析",
            "多环境配置管理"
        ],
        "steps": [
            "配置任务调度规则",
            "设置监控阈值",
            "部署到生产环境",
            "配置告警通知",
            "定期性能分析"
        ],
        "practices": [
            "使用版本控制管理配置",
            "实施错误处理机制",
            "定期备份任务配置",
            "监控系统资源使用",
            "设置合理的执行频率"
        ]
    },
    "Notion Table Cleaner": {
        "focus_areas": [
            "数据清理与去重",
            "格式标准化",
            "批量操作自动化",
            "性能优化",
            "数据导出与备份"
        ],
        "features": [
            "智能重复数据检测",
            "批量格式标准化",
            "自动数据清理",
            "性能优化工具",
            "多格式数据导出"
        ],
        "steps": [
            "连接 Notion 数据库",
            "配置清理规则",
            "执行数据清理",
            "验证清理结果",
            "设置定期清理任务"
        ],
        "practices": [
            "定期备份数据",
            "使用增量清理策略",
            "监控数据库性能",
            "优化查询语句",
            "定期更新清理规则"
        ]
    },
    "Postgres Surgeon": {
        "focus_areas": [
            "数据库性能调优",
            "数据恢复与修复",
            "索引优化",
            "查询性能分析",
            "存储管理"
        ],
        "features": [
            "智能性能分析",
            "数据恢复工具",
            "索引优化建议",
            "查询计划分析",
            "存储空间管理"
        ],
        "steps": [
            "连接目标数据库",
            "运行性能分析",
            "实施优化建议",
            "验证性能改进",
            "设置定期维护任务"
        ],
        "practices": [
            "定期性能监控",
            "实施增量备份",
            "优化查询语句",
            "合理设计索引",
            "监控存储空间使用"
        ]
    },
    "agents": {
        "focus_areas": [
            "AI 代理管理",
            "任务自动化",
            "智能决策系统",
            "多代理协作",
            "性能优化"
        ],
        "features": [
            "智能代理调度",
            "任务自动分配",
            "决策树优化",
            "多代理协作",
            "性能监控工具"
        ],
        "steps": [
            "配置代理参数",
            "定义任务流程",
            "部署代理系统",
            "监控运行状态",
            "优化代理性能"
        ],
        "practices": [
            "定期更新代理模型",
            "监控系统资源使用",
            "优化任务分配算法",
            "实施错误处理机制",
            "定期性能评估"
        ]
    },
    "crosspostfast": {
        "focus_areas": [
            "多平台 API 集成",
            "内容格式转换",
            "发布调度",
            "数据分析与报告",
            "用户体验优化"
        ],
        "features": [
            "多平台 API 集成",
            "智能内容转换",
            "定时发布调度",
            "性能分析报告",
            "用户界面优化"
        ],
        "steps": [
            "连接社交媒体账号",
            "配置内容转换规则",
            "设置发布时间表",
            "执行内容发布",
            "分析发布效果"
        ],
        "practices": [
            "定期更新 API 集成",
            "优化内容转换算法",
            "监控发布成功率",
            "分析用户 engagement",
            "定期系统维护"
        ]
    }
}

# 默认模板，用于处理没有特定模板的项目
default_template = {
    "focus_areas": [
        "核心功能实现",
        "性能优化",
        "用户体验设计",
        "安全性保障",
        "系统集成"
    ],
    "features": [
        "智能自动化",
        "实时监控",
        "数据分析",
        "用户友好界面",
        "安全保障"
    ],
    "steps": [
        "系统配置",
        "功能测试",
        "性能优化",
        "安全检查",
        "部署上线"
    ],
    "practices": [
        "定期维护",
        "性能监控",
        "安全更新",
        "用户反馈收集",
        "持续优化"
    ]
}

def generate_project_content(project_name, file_index):
    """为特定项目生成内容"""
    # 获取项目模板或使用默认模板
    template = project_content_templates.get(project_name, default_template)
    
    # 计算当前文件的侧重点索引
    focus_index = (file_index - 1) % len(template['focus_areas'])
    
    # 生成内容
    content = {
        "focus": template['focus_areas'][focus_index],
        "features": [],
        "steps": [],
        "practices": []
    }
    
    # 为每个文件生成3个功能、3个步骤、3个最佳实践
    for i in range(3):
        feature_index = (focus_index + i) % len(template['features'])
        step_index = (focus_index + i) % len(template['steps'])
        practice_index = (focus_index + i) % len(template['practices'])
        
        content["features"].append({
            "name": template['features'][feature_index],
            "description": f"{template['features'][feature_index]}: 提供{template['features'][feature_index].lower()}功能，支持{project_name}的核心需求，提升系统性能和用户体验。"
        })
        
        content["steps"].append({
            "name": template['steps'][step_index],
            "description": f"{template['steps'][step_index]}: 详细说明如何{template['steps'][step_index].lower()}，确保操作正确无误。"
        })
        
        content["practices"].append({
            "name": template['practices'][practice_index],
            "description": f"{template['practices'][practice_index]}: 建议{template['practices'][practice_index].lower()}，以确保系统稳定运行和持续优化。"
        })
    
    return content

def process_project(project):
    """处理单个项目"""
    project_name = project['name']
    project_dir = os.path.join(os.getcwd(), project_name.replace(' ', '-').lower())
    
    if not os.path.exists(project_dir):
        print(f"项目目录不存在: {project_dir}")
        return
    
    manual_dir = os.path.join(project_dir, 'manual')
    if not os.path.exists(manual_dir):
        print(f"manual 目录不存在: {manual_dir}")
        return
    
    # 处理英文文件
    for root, dirs, files in os.walk(manual_dir):
        # 跳过语言子目录
        if 'es' in root or 'de' in root or 'ja' in root or 'fr' in root:
            continue
        
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                
                # 提取文件索引
                file_index = int(re.search(r'_([0-9]+)\.md', file).group(1))
                
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 生成内容
                project_content = generate_project_content(project_name, file_index)
                
                # 替换占位符
                content = content.replace("Describe feature 1", project_content['features'][0]['description'])
                content = content.replace("Describe feature 2", project_content['features'][1]['description'])
                content = content.replace("Describe feature 3", project_content['features'][2]['description'])
                
                content = content.replace("Step 1: Describe Step 1", project_content['steps'][0]['description'])
                content = content.replace("Step 2: Describe Step 2", project_content['steps'][1]['description'])
                content = content.replace("Step 3: Describe Step 3", project_content['steps'][2]['description'])
                
                content = content.replace("Practice 1: Describe Practice 1", project_content['practices'][0]['description'])
                content = content.replace("Practice 2: Describe Practice 2", project_content['practices'][1]['description'])
                
                # 清除任何残留的占位符
                content = re.sub(r'Step \d+: ', '', content)
                content = re.sub(r'Practice \d+: ', '', content)
                
                # 修复关键词大小写
                content = content.replace('api', 'API')
                content = content.replace('seo', 'SEO')
                content = content.replace('url', 'URL')
                # 保持 HTTP 和 HTTPS 小写
                content = content.replace('HTTP', 'http')
                content = content.replace('HTTPS', 'https')
                
                # 更新 SEO 内容
                seo_pattern = r"This is SEO optimized content for the .*? project, keywords:.*"
                keywords = ', '.join(project['keywords'][:5])
                new_seo = f"This is SEO optimized content for the {project_name} project, keywords: {keywords}"
                content = re.sub(seo_pattern, new_seo, content)
                
                # 写回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"已更新 {file_path}")

def main():
    print("开始执行全局内容重构...")
    
    # 处理所有项目
    for project in projects:
        print(f"处理项目: {project['name']}")
        process_project(project)
    
    print("全局内容重构完成！")

if __name__ == "__main__":
    main()
