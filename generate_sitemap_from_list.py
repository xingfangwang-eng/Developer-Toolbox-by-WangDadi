import os
import re
import time

# 全局变量
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SITEMAP_FILE = os.path.join(ROOT_DIR, 'sitemap.xml')

# 从用户提供的文本中提取 URL
def extract_urls(text):
    # 使用正则表达式提取 URL
    url_pattern = r'https?://[^\s,]+'
    urls = re.findall(url_pattern, text)
    
    # 去重
    unique_urls = list(set(urls))
    
    return unique_urls

# 生成 sitemap.xml
def generate_sitemap(urls):
    # 生成 XML 头部
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'''
    
    # 添加每个 URL
    for url in urls:
        # 确保 URL 格式正确
        clean_url = url.strip()
        lastmod = time.strftime('%Y-%m-%d')
        
        xml_content += f'''
    <url>
        <loc>{clean_url}</loc>
        <lastmod>{lastmod}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
'''
    
    # 关闭 urlset 标签
    xml_content += '''</urlset>
'''
    
    return xml_content

# 保存 sitemap.xml
def save_sitemap(xml_content):
    try:
        with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        return True
    except Exception as e:
        print(f"保存 sitemap.xml 失败: {e}")
        return False

# 主函数
def main():
    print("开始生成 sitemap.xml...")
    
    # 用户提供的文本
    user_text = '''3月17日， `https://noseotop.wangdadi.xyz/` 
 3月17日， `https://nukeprivacy.wangdadi.xyz` 
 3月17日， `https://killbillcard.wangdadi.xyz/` 
 3月18日， `https://zerocloud.wangdadi.xyz` 
 3月18日， `https://focusinbox-eight.wangdadi.xyz` 
 3月18日， `https://saaskiller.wangdadi.xyz` 
 3月19日， `https://noaimd.wangdadi.xyz` 
 3月19日， `https://crosspostfast.wangdadi.xyz` 
 3月19日， `https://killswitchapi.wangdadi.xyz` 
 3月20日， `https://pingthemio.wangdadi.xyz` 
 3月20日， `https://neveruploadio.wangdadi.xyz/` 
 3月20日， `https://cleancsvai.wangdadi.xyz` 
 3月21日， `https://saasstripper.wangdadi.xyz` 
 3月21日， `https://noadobe.wangdadi.xyz` 
 3月21日， `https://navslayer.wangdadi.xyz` 
 3月22日， `https://killsaas.wangdadi.xyz` 
 3月22日， `https://slimsnd.wangdadi.xyz` 
 3月22日， `https://boothell.wangdadi.xyz` 
 3月26日， `https://linguisticdnaextractor.wangdadi.xyz/` 
 3月26日， `https://humbled.wangdadi.xyz/` 
 3月27日， `https://stopsaas.wangdadi.xyz/` 
 3月28日， `https://oneclickapi.wangdadi.xyz/（脚本提交google`  console）
 3月29日， `https://stopaicost.wangdadi.xyz/` 
 3月29日， `https://smesurvivalai.wangdadi.xyz/` 
 3月30日， `https://onecommand.wangdadi.xyz/` 
 3月30日， `https://killsubscription.wangdadi.xyz/` 
 4月3日， `https://manualslib.wangdadi.xyz/` 
 4月4日-5日， `https://billripper.wangdadi.xyz/` 
 4月5日， `https://deadliner.wangdadi.xyz/` 
 4月5日， `https://zerosub.wangdadi.xyz/` 
 4月5日， `https://mockupnuke.wangdadi.xyz/` 
 4月5日， `https://scriptkill.wangdadi.xyz/` 
 4月5日， `https://viralhook.wangdadi.xyz/` 
 4月5日， `https://onepagesaas.wangdadi.xyz/` 
 4月6日， `https://cineskin.wangdadi.xyz/` 
 4月7日-8日， `https://office-sync.wangdadi.xyz/` 
 4月7日-8日， `https://brainbridge.wangdadi.xyz/` 
 4月7日-8日， `https://personalock.wangdadi.xyz/` 
 4月7日-8日， `https://neverexplain.wangdadi.xyz/` 
 4月8日， `https://capsule-factory-saas.wangdadi.xyz` 
 4月8日， `https://chapterpredictor.wangdadi.xyz/` 
 4月8日， `https://giveawaytracker.wangdadi.xyz/` 
 4月9日， `https://stoptheswitch.wangdadi.xyz` 
 4月9日， `https://mememooncalculator.wangdadi.xyz` 
 4月10日， `https://autotask.wangdadi.xyz` 
 4月10日， `https://songkrangenerator.wangdadi.xyz` 
 4月11日， `https://artemisreentry.wangdadi.xyz` 
 4月11日， `https://coachellaviral.wangdadi.xyz` 
 4月12日， `https://tweetvirality.wangdadi.xyz` 
 4月12日， `https://bbb26dramapredictor.wangdadi.xyz` 
 4月12日， `https://deshaefrost.wangdadi.xyz` 
 4月12日， `https://samirapulse.wangdadi.xyz` 
 4月13日， `https://fanguard.wangdadi.xyz` 
 4月14日-15日， `https://agents.wangdadi.xyz` 
 4月15日， `https://receptionkiller.wangdadi.xyz` 
 4月15日， `https://nichecalccrusher.wangdadi.xyz` 
 4月16日， `https://hooksurgeon.wangdadi.xyz` 
 4月17日， `https://gmailretrybeast.wangdadi.xyz` 
 4月17日， `https://slopkiller.wangdadi.xyz` 
 4月18日， `https://postgresroast.wangdadi.xyz` 
 4月18日， `https://cronguard.wangdadi.xyz` 
 4月18日， `https://postgressurgeon.wangdadi.xyz` 
 4月19日， `https://notiontablecleaner.wangdadi.xyz` 
 4月19日， `https://laravelboilerplateslayer.wangdadi.xyz` 
 4月19日， `https://webhookslayer.wangdadi.xyz` 
 4月19日， `https://toolcallkiller.wangdadi.xyz` 
 4月20日， `https://deployguard.wangdadi.xyz` 
 4月20日， `https://contextlock.wangdadi.xyz` 
 4月20日， `https://noisekiller.wangdadi.xyz` 
 4月23日， `https://dossierpro.wangdadi.xyz` 
 4月23日， `https://apismash.wangdadi.xyz` 
 4月23日， `https://figmarip.wangdadi.xyz` 
 4月24日， `https://webhookreaper.wangdadi.xyz` 
 4月24日， `https://supaleak.wangdadi.xyz` 
 4月24日， `https://www.wangdadi.xyz/promptrescue` 
 4月24日， `https://www.wangdadi.xyz/sanityflow` 
  
  
  
 4月25日， `https://www.wangdadi.xyz/vitedaisyfix` 
 4月25日， `https://www.wangdadi.xyz/supaauthfix` 
 4月25日， `https://www.wangdadi.xyz/hookghostkiller`'''
    
    # 提取 URL
    urls = extract_urls(user_text)
    total_urls = len(urls)
    print(f"已提取 {total_urls} 个 URL")
    
    # 生成 sitemap
    xml_content = generate_sitemap(urls)
    
    # 保存 sitemap
    if save_sitemap(xml_content):
        print(f"sitemap.xml 生成成功！")
        print(f"文件位置: {SITEMAP_FILE}")
        print(f"包含 {total_urls} 个 URL")
    else:
        print("sitemap.xml 生成失败！")

if __name__ == "__main__":
    main()