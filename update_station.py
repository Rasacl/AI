import pandas as pd
import json

# 读取Excel文件
df = pd.read_excel('自动站观测表20250515.xlsx')

# 读取JSON文件
with open('自动站.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# 清空原有的data数组
json_data['data'] = []

# 处理每一行数据
for _, row in df.iterrows():
    # 检查各个字段的值是否为'-'或'/'
    temp = str(row['气温'])
    humidity = str(row['相对湿度'])
    max_wind_speed = str(row['极大风速'])
    max_wind_direction = str(row['极大风向'])
    rain_1min = str(row['1分钟降水量'])
    pressure = str(row['气压'])
    visibility = str(row['能见度'])
    
    # 根据条件设置elementLevel
    if all(x not in ['-', '/'] for x in [temp, humidity, max_wind_speed, max_wind_direction, rain_1min, pressure, visibility]):
        element_level = 7
    elif all(x not in ['-', '/'] for x in [temp, humidity, max_wind_speed, max_wind_direction, rain_1min, pressure]):
        element_level = 6
    elif all(x not in ['-', '/'] for x in [temp, humidity, max_wind_speed, pressure]):
        element_level = 4
    elif all(x not in ['-', '/'] for x in [temp, rain_1min]):
        element_level = 2
    else:
        element_level = 2  # 默认值
    
    # 创建站点数据
    station_data = {
        "id": str(row['站号']),
        "name": str(row['站名']),
        "district": str(row['区县']),
        "status": "正常" if str(row['黑名单']) == '正常' else "告警",
        "height": str(row['海拔']),
        "elementLevel": element_level
    }
    
    # 添加到data数组
    json_data['data'].append(station_data)

# 将更新后的数据写回JSON文件
with open('自动站.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)

print("数据更新完成！")