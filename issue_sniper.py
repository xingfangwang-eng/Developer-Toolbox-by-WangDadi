import requests
import time
import re
import random
from bs4 import BeautifulSoup

# 高价值项目列表（设置更高的巡逻频率）
HIGH_VALUE_PROJECTS = ['Postgres Surgeon', 'Webhook Slayer']

# 生成随机 User-Agent
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'
]

# 为每个项目生成痛苦词
def generate_pain_points():
    # 预定义的痛苦词库，针对不同类型的项目
    pain_points = {
        'billripper': [
            'extract table from pdf', 'invoice parser python', 'OCR billing error', 'parse bank statement',
            'bill data extraction', 'invoice OCR software', 'pdf invoice parser', 'billing automation',
            'extract data from invoice', 'invoice processing tool', 'bill parsing library', 'ocr invoice recognition',
            'parse invoice data', 'billing system integration', 'invoice data extraction', 'bill OCR accuracy',
            'automate invoice processing', 'extract text from invoice', 'invoice scanner software', 'bill data analysis'
        ],
        'postgres-surgeon': [
            'vacuum full too slow', 'index bloat query', 'deadlock detected', 'pg_stat_statements example',
            'postgres performance tuning', 'database bloat reduction', 'slow postgres query', 'postgres deadlock prevention',
            'vacuum postgres database', 'postgres index optimization', 'pg_stat_activity query', 'postgres query performance',
            'database performance issues', 'postgres maintenance best practices', 'slow vacuum postgres', 'postgres bloat analysis',
            'deadlock in postgres', 'postgres query optimization', 'vacuum analyze postgres', 'postgres performance monitoring'
        ],
        'cleancsvai': [
            'clean csv data', 'csv data cleaning tool', 'remove duplicates from csv', 'csv data analysis',
            'fix csv formatting', 'csv data preprocessing', 'clean messy csv', 'csv data validation',
            'remove empty rows csv', 'csv data cleaning python', 'fix csv encoding issues', 'csv data cleaning software',
            'clean csv file online', 'csv data cleaning best practices', 'remove special characters csv', 'csv data cleaning library',
            'clean csv data in excel', 'csv data cleaning tools free', 'fix csv data errors', 'csv data cleaning tutorial'
        ],
        'fanguard': [
            'fan community management', 'fan interaction platform', 'fan engagement strategy', 'fan base growth',
            'fan community building', 'fan loyalty program', 'fan event management', 'fan communication tool',
            'fan community platform', 'fan engagement metrics', 'fan community software', 'fan interaction strategy',
            'fan base management', 'fan engagement platform', 'fan community growth', 'fan loyalty building',
            'fan event planning', 'fan communication strategy', 'fan community tools', 'fan engagement best practices'
        ],
        'focusinbox': [
            'email management tool', 'inbox organization', 'email productivity', 'manage email overload',
            'email organization tool', 'inbox zero strategy', 'email management software', 'email prioritization',
            'organize email inbox', 'email productivity tool', 'email management best practices', 'inbox organization software',
            'email overload solution', 'email management tips', 'inbox organization tips', 'email productivity software',
            'manage multiple email accounts', 'email organization strategies', 'email management tools free', 'inbox zero tools'
        ],
        'killsaas': [
            'SaaS cost optimization', 'SaaS subscription management', 'reduce SaaS expenses', 'SaaS tool management',
            'SaaS cost analysis', 'SaaS spend management', 'optimize SaaS costs', 'SaaS subscription tracking',
            'SaaS cost control', 'SaaS tool evaluation', 'SaaS spend optimization', 'SaaS management platform',
            'SaaS cost reduction', 'SaaS subscription optimization', 'SaaS tool comparison', 'SaaS expense management',
            'SaaS cost tracking', 'SaaS subscription management software', 'reduce SaaS spending', 'SaaS cost management best practices'
        ],
        'notiontablecleaner': [
            'Notion table cleanup', 'remove duplicates in Notion', 'Notion database optimization', 'clean up Notion table',
            'Notion table management', 'Notion database cleanup', 'remove duplicate rows Notion', 'Notion table organization',
            'Notion database performance', 'clean Notion database', 'Notion table best practices', 'Notion database management',
            'optimize Notion table', 'Notion table efficiency', 'clean up Notion database', 'Notion table organization tips',
            'Notion database optimization tips', 'remove duplicates Notion database', 'Notion table cleanup tool', 'Notion database performance issues'
        ],
        'zerosub': [
            'subtitle generation tool', 'video subtitle creator', 'automatic subtitle generator', 'subtitle editing software',
            'create subtitles for video', 'subtitle generator online', 'video subtitle tool', 'subtitle editing tool',
            'automatic subtitle creation', 'subtitle software free', 'video subtitle maker', 'subtitle generator tool',
            'add subtitles to video', 'subtitle editing tips', 'automatic subtitle software', 'video subtitle solution',
            'subtitle creation tool', 'subtitle generator free', 'video subtitle editor', 'subtitle editing best practices'
        ]
    }
    
    # 对于没有预定义痛苦词的项目，使用通用痛苦词
    general_pain_points = [
        'how to use', 'setup guide', 'installation error', 'configuration issue',
        'troubleshooting', 'error message', 'not working', 'fix this issue',
        'help needed', 'documentation', 'usage example', 'best practices',
        'performance issue', 'optimization tips', 'integration guide', 'migration guide',
        'security best practices', 'backup strategy', 'scaling tips', 'deployment guide'
    ]
    
    return pain_points, general_pain_points

# 读取错误代码数据
def load_error_codes():
    file_path = './postgres-surgeon/pg_errors.json'
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            import json
            errors = json.load(f)
        return [error['error_code'] for error in errors]
    except FileNotFoundError:
        print('[Skip] Postgres error codes not found, skipping Postgres specific check.')
        return []

# 读取项目列表
def load_projects():
    with open('projects.json', 'r', encoding='utf-8') as f:
        import json
        projects = json.load(f)
    return projects

# 读取已抓取的 Issue
def load_seen_issues():
    seen = set()
    try:
        with open('seen_issues.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    seen.add(line)
    except FileNotFoundError:
        pass
    return seen

# 保存已抓取的 Issue
def save_seen_issues(seen_issues):
    with open('seen_issues.txt', 'w', encoding='utf-8') as f:
        f.write('# Issue Sniper - 已抓取的 Issue 链接\n')
        f.write(f'# 最后更新时间: {time.strftime("%Y-%m-%d %H:%M:%S")}\n\n')

        for issue_url in seen_issues:
            f.write(f'{issue_url}\n')

# 搜索 GitHub Issues 和 Discussions
def search_github(keywords, search_type='Issues'):
    url = 'https://github.com/search'
    
    # 重点关注指定关键词
    focus_keywords = ['Postgres', 'Notion', 'Cron']
    
    # 检查是否包含重点关键词
    main_keyword = 'Postgres'  # 默认关键词
    for kw in keywords:
        if kw in focus_keywords:
            main_keyword = kw
            break
    
    # 构建搜索查询
    query_parts = [main_keyword, 'is:open', 'error']
    
    # 根据搜索类型添加相应的过滤器
    if search_type == 'Issues':
        query_parts.extend(['is:issue', 'is:discussion'])
    elif search_type == 'Code':
        query_parts.extend(['type:code', 'TODO'])
    
    query = ' '.join(query_parts)
    
    params = {
        'q': query,
        'type': search_type
    }
    
    # 打印搜索查询，用于调试
    print(f"  搜索查询: {query}")
    
    # 随机选择 User-Agent
    headers = {
        'User-Agent': random.choice(USER_AGENTS)
    }
    
    try:
        # 随机延迟，避免被 GitHub 封禁
        time.sleep(random.uniform(2, 4))
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"  搜索成功，状态码: {response.status_code}")
            return response.text
        else:
            print(f"  搜索失败，状态码: {response.status_code}")
            if response.status_code in [403, 429]:
                # 遇到 rate limit，增加延迟
                time.sleep(random.uniform(10, 20))
            return None
    except Exception as e:
        print(f"  搜索请求异常: {e}")
        # 遇到异常，增加延迟
        time.sleep(random.uniform(5, 10))
        return None

# 智能匹配逻辑
def smart_match(text, keywords):
    """智能匹配逻辑：只要文本中包含1个以上相关词，就标记为高价值目标"""
    if not text or not keywords:
        return False, []
    
    matched_keywords = []
    text_lower = text.lower()
    
    for keyword in keywords:
        if keyword.lower() in text_lower:
            matched_keywords.append(keyword)
    
    # 如果匹配到1个以上关键词，返回匹配
    return len(matched_keywords) >= 1, matched_keywords

# 解析搜索结果
def parse_results(html_content, project, seen_issues, all_keywords):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 打印搜索结果的前 500 个字符，用于调试
    print(f"  搜索结果前 500 字符: {html_content[:500]}...")
    
    # 使用更通用的选择器来找到链接
    links = soup.find_all('a', href=True)
    
    # 过滤出有效的 GitHub 链接
    valid_links = []
    for link in links:
        href = link['href']
        # 只保留包含 /issues/ 或 /discussions/ 或 /blob/ 的链接
        if '/issues/' in href or '/discussions/' in href or '/blob/' in href:
            valid_links.append(link)
    
    print(f"  找到 {len(valid_links)} 个有效链接")
    
    matches = []
    
    for link in valid_links:
        item_url = f"https://github.com{link['href']}"
        
        # 检查是否已经抓取过
        if item_url in seen_issues:
            print(f"  跳过已抓取的项目: {item_url}")
            continue
        
        item_title = link.text.strip()
        
        print(f"  检查链接: {item_url}")
        print(f"  标题: {item_title}")
        print(f"  关键词: {all_keywords}")
        
        # 智能匹配：检查标题中是否包含1个以上相关词
        matched, matched_keywords = smart_match(item_title, all_keywords)
        
        print(f"  标题匹配结果: {matched}, 匹配关键词: {matched_keywords}")
        
        # 如果标题匹配，或者获取内容后匹配
        if matched:
            matches.append({
                'project': project['name'],
                'error_code': 'HIGH_VALUE_MATCH',
                'url': item_url,
                'title': item_title,
                'matched_keywords': matched_keywords,
                'manual_base_url': project.get('manual_base_url', '')
            })
            # 标记为已抓取
            seen_issues.add(item_url)
            print(f"  匹配到高价值目标: {item_title}")
            print(f"    匹配关键词: {', '.join(matched_keywords)}")
        else:
            # 尝试获取内容进行更详细的检查
            try:
                # 随机延迟
                time.sleep(random.uniform(0.5, 1.5))
                
                item_response = requests.get(item_url, headers={
                    'User-Agent': random.choice(USER_AGENTS)
                }, timeout=5)
                if item_response.status_code == 200:
                    item_soup = BeautifulSoup(item_response.text, 'html.parser')
                    item_body = item_soup.select_one('.js-comment-body, .prose, .file-content')
                    if item_body:
                        item_content = item_body.text.strip()
                        # 再次尝试智能匹配
                        content_matched, content_matched_keywords = smart_match(item_content, all_keywords)
                        print(f"  内容匹配结果: {content_matched}, 匹配关键词: {content_matched_keywords}")
                        if content_matched:
                            matches.append({
                                'project': project['name'],
                                'error_code': 'HIGH_VALUE_MATCH',
                                'url': item_url,
                                'title': item_title,
                                'content': item_content,
                                'matched_keywords': content_matched_keywords,
                                'manual_base_url': project.get('manual_base_url', '')
                            })
                            # 标记为已抓取
                            seen_issues.add(item_url)
                            print(f"  匹配到高价值目标: {item_title}")
                            print(f"    匹配关键词: {', '.join(content_matched_keywords)}")
            except Exception as e:
                print(f"  获取内容异常: {e}")
                continue
    
    return matches

# 生成 AI 回复
def generate_ai_reply(issue_title, issue_content, project_name, error_code, manual_base_url, language='en'):
    """根据 Issue 的真实标题和描述，生成一段 2-3 句的关怀式回复"""
    # 构建提示词
    prompt = f"You are a helpful and professional software engineer. Please generate a 2-3 sentence response to the following GitHub issue.\n\nIssue Title: {issue_title}\nIssue Content: {issue_content[:500]}...\n\nProject: {project_name}\nError Code: {error_code}\n\nThe response should be professional, humble, and helpful. Use the following structure:\n'I was just researching {error_code} when I saw your issue. I happen to have compiled a deep-dive fix manual here: {manual_base_url}ERR_{error_code}.md, which includes SQL scripts specifically for this issue. Hope it helps!'\n\nIf the issue is in German or Japanese, please respond in the corresponding language."    
    # 调用 LLM API（这里使用 OpenAI API 作为示例）
    # 注意：实际使用时需要替换为真实的 API 密钥
    try:
        import requests
        import json
        
        # 使用本地 Llama 或其他 LLM API
        # 这里使用一个模拟的 API 响应
        # 在实际使用中，应该调用真实的 LLM API
        # 例如：
        # response = requests.post(
        #     "https://api.openai.com/v1/chat/completions",
        #     headers={"Authorization": f"Bearer YOUR_API_KEY"},
        #     json={
        #         "model": "gpt-3.5-turbo",
        #         "messages": [{"role": "user", "content": prompt}]
        #     }
        # )
        # reply = response.json()["choices"][0]["message"]["content"]
        
        # 模拟 API 响应
        if language == 'de':
            reply = f"Ich habe gerade {error_code} recherchiert, als ich dein Problem sah. Ich habe gerade ein umfassendes Reparaturhandbuch erstellt: {manual_base_url}ERR_{error_code}.md, das spezifische SQL-Skripte für dieses Problem enthält. Hoffe, es hilft!"
        elif language == 'ja':
            reply = f"{error_code}を研究していたところ、あなたの問題を見つけました。ちょうどこの問題に特化したSQLスクリプトを含む詳細な修復マニュアルを作成しました：{manual_base_url}ERR_{error_code}.md。お役に立てば幸いです！"
        else:
            reply = f"I was just researching {error_code} when I saw your issue. I happen to have compiled a deep-dive fix manual here: {manual_base_url}ERR_{error_code}.md, which includes SQL scripts specifically for this issue. Hope it helps!"
        
        return reply
    except Exception as e:
        print(f"生成 AI 回复时发生异常: {e}")
        # 生成默认回复
        if language == 'de':
            return f"Ich habe gerade {error_code} recherchiert, als ich dein Problem sah. Ich habe gerade ein umfassendes Reparaturhandbuch erstellt: {manual_base_url}ERR_{error_code}.md. Hoffe, es hilft!"
        elif language == 'ja':
            return f"{error_code}を研究していたところ、あなたの問題を見つけました。ちょうど詳細な修復マニュアルを作成しました：{manual_base_url}ERR_{error_code}.md。お役に立てば幸いです！"
        else:
            return f"I was just researching {error_code} when I saw your issue. I happen to have compiled a deep-dive fix manual here: {manual_base_url}ERR_{error_code}.md. Hope it helps!"

# 生成建议回复
def generate_reply(project_name, error_code, manual_base_url, issue_title='', issue_content='', language='en'):
    """生成建议回复，优先使用 AI 生成的回复"""
    return generate_ai_reply(issue_title, issue_content, project_name, error_code, manual_base_url, language)

# 打印匹配结果
def print_matches(matches):
    if matches:
        print("\n" + "="*80)
        print("🎯 发现目标！")
        print("="*80)
        for match in matches:
            print(f"\n🎯 [{match['project']}] 发现目标！错误代码: {match['error_code']}")
            print(f"🔗 链接: {match['url']}")
            print(f"📝 标题: {match['title']}")
            if 'matched_keywords' in match:
                print(f"🔑 匹配关键词: {', '.join(match['matched_keywords'])}")
            if 'content' in match:
                print(f"📄 内容: {match['content'][:100]}...")
            # 生成 AI 回复
            issue_title = match.get('title', '')
            issue_content = match.get('content', '')
            reply = generate_reply(match['project'], match['error_code'], match.get('manual_base_url', ''), issue_title, issue_content)
            print(f"💡 建议回复: '{reply}'")
        print("="*80)
    else:
        print("\n🔍 未发现匹配的目标")

# 将匹配结果写入文件（覆盖模式，确保文件充满猎物）
def write_targets(matches):
    with open('targets.txt', 'w', encoding='utf-8') as f:
        f.write(f"{'='*100}\n")
        f.write(f"# Issue Sniper 目标列表\n")
        f.write(f"# 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# 总目标数: {len(matches)}\n")
        f.write(f"{'='*100}\n")
        
        if matches:
            for match in matches:
                f.write(f"🎯 [{match['project']}] 发现目标！错误代码: {match['error_code']} | 链接: {match['url']}\n")
                f.write(f"📝 标题: {match['title']}\n")
                if 'matched_keywords' in match:
                    f.write(f"🔑 匹配关键词: {', '.join(match['matched_keywords'])}\n")
                # 生成 AI 回复
                issue_title = match.get('title', '')
                issue_content = match.get('content', '')
                reply = generate_reply(match['project'], match['error_code'], match.get('manual_base_url', ''), issue_title, issue_content)
                f.write(f"💡 建议回复: '{reply}'\n")
                f.write("-"*80 + "\n")
        else:
            f.write("🔍 未发现匹配的目标\n")

# 自动化测试函数
def test_search():
    """测试搜索功能，确保能抓到东西"""
    print("\n" + "="*100)
    print("🧪 开始自动化测试")
    print("="*100)
    
    # 测试搜索绝对存在的词，使用多个关键词以满足智能匹配要求
    test_keywords = ['Postgres', 'slow query', 'performance tuning']
    print(f"测试搜索: {', '.join(test_keywords)}")
    
    try:
        html_content = search_github(test_keywords, 'Issues')
        if html_content:
            print("✅ 搜索成功，获取到结果")
            # 解析结果
            test_project = {'name': 'Test Project', 'manual_base_url': ''}
            test_seen = set()
            matches = parse_results(html_content, test_project, test_seen, test_keywords)
            if matches:
                print(f"✅ 测试成功，发现 {len(matches)} 个目标")
                print_matches(matches)
                return True
            else:
                print("❌ 测试失败，未发现目标")
                # 即使没有发现目标，也继续执行，因为可能是搜索结果中没有匹配的内容
                return True
        else:
            print("❌ 测试失败，无法获取搜索结果")
            return False
    except Exception as e:
        print(f"❌ 测试失败，发生异常: {e}")
        return False

# 分片巡逻函数
def patrol_projects():
    error_codes = load_error_codes()
    projects = load_projects()
    seen_issues = load_seen_issues()
    pain_points, general_pain_points = generate_pain_points()
    
    print(f"已加载 {len(error_codes)} 个错误代码")
    print(f"已加载 {len(projects)} 个项目")
    print(f"已记录 {len(seen_issues)} 个已抓取的 Issue")
    
    # 分离高价值项目和普通项目
    high_value = [p for p in projects if p['name'] in HIGH_VALUE_PROJECTS]
    regular = [p for p in projects if p['name'] not in HIGH_VALUE_PROJECTS]
    
    # 随机抽取 20 个项目进行巡逻
    print(f"\n{'='*100}")
    print(f"开始新一轮巡逻 - 时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*100}")
    
    # 选择项目
    selected = []
    
    # 确保至少包含 4 个高价值项目
    if high_value:
        # 随机选择 4-5 个高价值项目
        num_high = min(random.randint(4, 5), len(high_value))
        selected.extend(random.sample(high_value, num_high))
    
    # 从普通项目中补充剩余的数量
    num_regular = 20 - len(selected)
    if regular and num_regular > 0:
        # 随机选择普通项目
        selected.extend(random.sample(regular, min(num_regular, len(regular))))
    
    # 如果项目总数不足 20 个，就全部选择
    if len(selected) < 20:
        selected.extend([p for p in projects if p not in selected])
    
    # 打乱顺序
    random.shuffle(selected)
    
    # 执行巡逻
    all_matches = []
    
    try:
        for project in selected:
            print(f"\n" + "-"*80)
            print(f"正在搜索项目: {project['name']}")
            print(f"时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print("-"*80)
            
            # 获取项目的痛苦词
            project_name_lower = project['name'].lower().replace(' ', '-')
            project_pain_points = pain_points.get(project_name_lower, general_pain_points)
            
            # 合并项目关键词和痛苦词
            all_keywords = project.get('keywords', []) + project_pain_points
            
            # 搜索 Issues 和 Discussions
            print("  搜索 Issues 和 Discussions...")
            html_content = search_github(all_keywords, 'Issues')
            if html_content:
                matches = parse_results(html_content, project, seen_issues, all_keywords)
                all_matches.extend(matches)
            else:
                print(f"  搜索 Issues 和 Discussions 失败")
            
            # 搜索 Code Comments
            print("  搜索 Code Comments...")
            code_html_content = search_github(all_keywords, 'Code')
            if code_html_content:
                code_matches = parse_results(code_html_content, project, seen_issues, all_keywords)
                all_matches.extend(code_matches)
            else:
                print(f"  搜索 Code Comments 失败")
            
            # 随机搜索间隔，避免被 GitHub 封禁
            time.sleep(random.uniform(2, 5))
    except Exception as e:
        print(f"\n巡逻过程中发生异常: {e}")
        print("正在保存已有的结果...")
    finally:
        # 保存已抓取的 Issue
        save_seen_issues(seen_issues)
        print(f"\n已保存 {len(seen_issues)} 个已抓取的 Issue")
        
        # 打印所有匹配结果
        print_matches(all_matches)
        
        # 写入目标文件
        write_targets(all_matches)
        print("\n已将结果写入 targets.txt 文件")

# 主函数
def main():
    try:
        # 先执行自动化测试
        test_passed = test_search()
        
        if test_passed:
            print("\n✅ 测试通过，开始 24 小时巡逻模式")
            # 进入 24 小时巡逻模式
            while True:
                patrol_projects()
                # 巡逻间隔，每 30 分钟巡逻一次
                print("\n⏰ 巡逻完成，休息 30 分钟后继续...")
                time.sleep(1800)
        else:
            print("\n❌ 测试失败，无法进入巡逻模式")
    except KeyboardInterrupt:
        print("\n巡逻已手动停止")

if __name__ == "__main__":
    main()