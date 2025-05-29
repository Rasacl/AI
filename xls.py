import pandas as pd
import json
import random
from datetime import datetime, timedelta

def random_date(start_date, end_date):
    """
    @description 在给定的起始日期和结束日期之间随机生成一个日期
    @param {datetime} start_date 开始日期
    @param {datetime} end_date 结束日期
    @returns {str} 返回格式化的日期字符串
    """
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date.strftime("%Y-%m-%d")

# 读取Excel文件
df = pd.read_excel('花粉.xlsx')

# 创建结果数据结构
result = {
    "code": 200,
    "success": True,
    "data": [],
    "msg": "操作成功"
}

# 设置日期范围
start_date = datetime(2015, 1, 1)
end_date = datetime(2025, 12, 31)

# 遍历Excel数据
for _, row in df.iterrows():
    # 检查必要的列是否存在
    if '站点号' in row and '名称' in row and '经度' in row and '纬度' in row:
        station_data = {
            "id": str(row['站点号']),
            "name": str(row['名称']),
            "lonLat": [
                str(row['经度']),
                str(row['纬度'])
            ],
            "district": str(row['区县']),
            "height": str(random.randint(10, 800)),  # 随机生成10-800之间的高度
            "status": "在线",  # 随机选择状态
            "time": random_date(start_date, end_date)  # 随机生成2015-2025之间的日期
        }
        result['data'].append(station_data)

# 将结果写入新的JSON文件
with open('stations.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

print("JSON文件生成完成！")