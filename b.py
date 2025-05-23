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
with open('b.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 获取当前日期
current_date = datetime.now()

# 处理每个数据项
for item in data['data']:
    project_name = item['projectName']
    item['status'] = random.choice(['可用', '告警'])
    if project_name == "2015-2020：十三五项目":
        start_date = datetime(2015, 1, 1)
        end_date = datetime(2020, 12, 31)
        item['time'] = random_date(start_date, end_date)
    
    elif project_name == "2021-2023：十四五项目":
        start_date = datetime(2021, 1, 1)
        end_date = datetime(2023, 12, 31)
        item['time'] = random_date(start_date, end_date)
    
    elif project_name == "2024：能力提升项目":
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 12, 31)
        item['time'] = random_date(start_date, end_date)
    
    elif project_name == "2025-至今：2025收官（待建）":
        start_date = datetime(2025, 1, 1)
        item['time'] = random_date(start_date, current_date)
    
    # 删除projectName字段
    del item['projectName']

# 将修改后的数据写回文件
with open('b.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)