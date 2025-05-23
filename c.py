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

# 读取JSON文件
with open('c.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 设置日期范围
start_date = datetime(2015, 1, 1)
end_date = datetime(2024, 12, 30)

# 修改每个数据项的time字段
for item in data['data']:
    item['time'] = random_date(start_date, end_date)

# 将修改后的数据写回文件
with open('c.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("时间范围修改完成！")