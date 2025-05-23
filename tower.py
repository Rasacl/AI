import json
import random

# 读取JSON文件
with open('tower.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 为每个对象添加elementLevel字段
for item in data['data']:
    item['type'] = random.choice(['铁塔站', '铁塔智慧站', '铁塔交通站','铁塔梯度站'])

# 将修改后的数据写回文件
with open('tower.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)