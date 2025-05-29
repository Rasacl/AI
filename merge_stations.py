import json
import random
import string

# 生成随机ID和code
def generate_random_id():
    return random.randint(10000, 99999)

def generate_random_code():
    # 生成类似'130126003'的随机code
    return ''.join(random.choices(string.digits, k=9))

# 读取两个JSON文件
with open('北京作业点.json', 'r', encoding='utf-8') as f:
    beijing_data = json.load(f)

with open('人影站点.json', 'r', encoding='utf-8') as f:
    weather_data = json.load(f)

# 转换北京作业点数据
for row in beijing_data['rows']:
    print(row)
    new_station = {
        "id": generate_random_id(),
        "code": generate_random_code(),
        "name": row['belongsTownName'] if row['belongsTownName'] else row['name'],
        "longitude": float(row['lon']),
        "latitude": float(row['lat']),
        "altitude": None,
        "provinceid": "110000",  # 北京市行政区划代码
        "cityid": "",
        "countyid": "",
        "town": None,
        "tool": "火箭",
        "rocketype": None,
        "cannontype": None,
        "planetype": None,
        "burnertype": None,
        "direction": None,
        "elevation": None,
        "radius": None,
        "height": None,
        "airzone": None,
        "radioid": None,
        "note": None,
        "phoneNumber": None,
        "provinceName": row['belongsCountyName'],
        "cityName": None,
        "countyName": None,
        "images": None,
        "rocketNum": "0",
        "cannonNum": "1",
        "moveStatus": 0
    }
    weather_data['data']['rows'].append(new_station)

# 保存合并后的数据
with open('人影站点_merged.json', 'w', encoding='utf-8') as f:
    json.dump(weather_data, f, ensure_ascii=False, indent=4)