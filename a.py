import json
import random

# 读取JSON文件
with open('a.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 为每个对象添加elementLevel字段
for item in data['data']:
    item['elementLevel'] = random.choice([2,4, 6,7])

# 将修改后的数据写回文件
with open('a.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)