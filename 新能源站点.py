import json
import random

def determine_station_type(station_name):
    """根据站点名称判断站点类型"""
    if any(keyword in station_name for keyword in ['光伏', '太阳能']):
        return '光伏电站'
    elif any(keyword in station_name for keyword in ['风电', '风力']):
        return '风电站'
    else:
        return '变电站'

# 读取JSON文件
with open('新能源站点.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 为每个站点添加类型
for station in data['data']:
    station['stationType'] = random.choice(['光伏电站', '风电站', '变电站'])

# 保存修改后的JSON文件
with open('新能源站点.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print('处理完成！')