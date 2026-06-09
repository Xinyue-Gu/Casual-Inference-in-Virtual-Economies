import cloudscraper
import re
import pandas as pd
import json

# 1. 使用 cloudscraper 替代 requests，自动处理基本的 Cloudflare 质询
scraper = cloudscraper.create_scraper()
url = "https://steamcharts.com/app/730"

print("正在尝试突破反爬获取数据...")
response = scraper.get(url)

if response.status_code == 200:
    html_content = response.text
    
    # 2. 正则捕获数据
    pattern = r"data:\s*(\[\[.*?\]\])"
    match = re.search(pattern, html_content, re.DOTALL)
    
    if match:
        data_string = match.group(1)
        raw_data = json.loads(data_string)
        
        # 3. 数据清洗
        df_players = pd.DataFrame(raw_data, columns=['timestamp_ms', 'concurrent_players'])
        df_players['date'] = pd.to_datetime(df_players['timestamp_ms'], unit='ms').dt.date
        df_daily_players = df_players.groupby('date')['concurrent_players'].max().reset_index()
        
        print("抓取成功！前五行数据：")
        print(df_daily_players.head())
        # df_daily_players.to_csv('cs2_daily_players.csv', index=False)
    else:
        print("未找到数据，可能是正则表达式未匹配到目标结构。")
else:
    print(f"请求失败，状态码: {response.status_code}")