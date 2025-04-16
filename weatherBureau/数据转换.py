import pandas as pd
import json
import os
from datetime import datetime, timedelta

# 设置文件路径
excel_path = r"d:\project\self\AI\weatherBureau\54499站点分类花粉数据.xlsx"

# 读取Excel文件
df = pd.read_excel(excel_path)

# 将OBSERVERTIME列转换为日期类型
df['OBSERVERTIME'] = pd.to_datetime(df['OBSERVERTIME'])

# 获取时间范围
start_date = df['OBSERVERTIME'].min()
end_date = df['OBSERVERTIME'].max()

# 创建完整的日期序列
date_range = pd.date_range(start=start_date, end=end_date, freq='D')
date_df = pd.DataFrame({'OBSERVERTIME': date_range})

# 将原数据与完整日期序列合并，缺失值填充为0
df = pd.merge(date_df, df, on='OBSERVERTIME', how='left')
df = df.fillna(0)

# 将时间戳转换为字符串格式
time_list = df['OBSERVERTIME'].dt.strftime('%Y-%m-%d').tolist()

# 创建数据结构
data = {
    "data": {
        "legend": [],
        "xAxis": time_list,
        "yAxis": []
    }
}

# 获取所有花粉类型
pollen_types = [col for col in df.columns if col != 'OBSERVERTIME']
data["data"]["legend"] = pollen_types

# 获取每种花粉的数据
for pollen_type in pollen_types:
    daily_data = df[pollen_type].tolist()
    data["data"]["yAxis"].append(daily_data)

# 将数据保存为JSON文件
with open('new_pollen_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("数据转换完成，已保存为 new_pollen_data.json")