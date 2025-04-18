# datetime
from datetime import datetime, timedelta

# 1. 获取当前日期和时间
now = datetime.now()
print(f"当前时间：{now}")

# 2. 创建指定的日期和时间
specific_date = datetime(2024, 1, 1, 12, 30, 0)
print(f"指定时间：{specific_date}")

# 3. 日期格式化
formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
print(f"格式化时间：{formatted_date}")

# 4. 字符串转日期
date_string = "2024-01-01 12:30:00"
parsed_date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
print(f"解析的时间：{parsed_date}")

# 5. 日期计算
tomorrow = now + timedelta(days=1)
print(f"明天：{tomorrow}")

next_week = now + timedelta(weeks=1)
print(f"下周：{next_week}")

two_hours_later = now + timedelta(hours=2)
print(f"两小时后：{two_hours_later}")

# 6. 获取日期的具体部分
print(f"年：{now.year}")
print(f"月：{now.month}")
print(f"日：{now.day}")
print(f"时：{now.hour}")
print(f"分：{now.minute}")
print(f"秒：{now.second}")

# 7. 日期比较
date1 = datetime(2024, 1, 1)
date2 = datetime(2024, 2, 1)
print(f"日期比较：{date1 < date2}")

# 8. 计算日期差
time_diff = date2 - date1
print(f"相差天数：{time_diff.days}")

# 9. 时间戳转换
timestamp = datetime.timestamp(now)
print(f"时间戳：{timestamp}")

from_timestamp = datetime.fromtimestamp(timestamp)
print(f"从时间戳转回：{from_timestamp}")

# 10. 获取星期
weekday = now.strftime("%A")
print(f"星期：{weekday}")