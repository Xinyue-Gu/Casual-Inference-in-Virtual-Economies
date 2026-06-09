import pandas as pd

# 1. 读取你刚刚通过 Console 黑魔法下载的 CSV
df_players = pd.read_csv('D:/UIUC大学课程相关/课外活动经历记录/论文写作/CS2 DiD相关项目/cs2_players_full_history.csv')

# 2. 将 Unix 毫秒时间戳转换为 datetime 格式
# unit='ms' 告诉 pandas 这是毫秒级别的时间戳
df_players['date_time'] = pd.to_datetime(df_players['timestamp_ms'], unit='ms')

# 3. 提取出具体的日期 (去掉小时和分钟)
df_players['date'] = df_players['date_time'].dt.date

# 4. 按天聚合 (因为原图表有时包含每小时的数据节点)
# 我们取每一天的最高在线人数 (Daily Peak Concurrent Players)
df_daily_players = df_players.groupby('date')['player_count'].max().reset_index()

# 确保 date 列是标准的 datetime64 格式，为了后续和你饰品数据的 Join
df_daily_players['date'] = pd.to_datetime(df_daily_players['date'])

print(df_daily_players.tail(10)) # 检查数据的最后十天，确保包含 2023 和 2024 年的数据！
import pandas as pd

# 1. 读取原始数据 (使用原声字符串 r 防止路径报错)
df_players = pd.read_csv(r'D:\UIUC大学课程相关\课外活动经历记录\论文写作\CS2 DiD相关项目\cs2_players_full_history.csv')

# 2. 转换时间戳为日期
df_players['date_time'] = pd.to_datetime(df_players['timestamp_ms'], unit='ms')
df_players['date'] = df_players['date_time'].dt.date

# 3. 按天提取最高在线人数
df_daily_players = df_players.groupby('date')['player_count'].max().reset_index()

# 4. 确保 date 列是标准格式
df_daily_players['date'] = pd.to_datetime(df_daily_players['date'])

print("清洗成功！前五行如下：")
print(df_daily_players.head())

# 5. 【新增这一行】将清洗好的数据保存为一个新的 CSV 文件
# index=False 表示不保存最左侧的 0,1,2,3 索引号
df_daily_players.to_csv(r'D:\UIUC大学课程相关\课外活动经历记录\论文写作\CS2 DiD相关项目\cs2_players_CLEANED.csv', index=False)

print("\n成功保存为 cs2_players_CLEANED.csv！")