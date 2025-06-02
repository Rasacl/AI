import json
import random

# 读取JSON文件
file_path = '自动和铁塔.json'
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 处理每个数据项
for item in data['data']:
    # 删除status字段
    if 'status' in item:
        del item['status']
    
    # 删除type字段（如果存在）
    if 'type' in item:
        del item['type']
    
    # 添加historyWater和currentWater字段
    # 先确定historyWater的值（不超过500）
    history_water = random.randint(100, 500)
    
    # 确保currentWater小于historyWater的一半
    max_current = history_water // 2 - 1
    current_water = random.randint(10, max(10, max_current))
    
    item['currentWater'] = current_water
    item['historyWater'] = history_water

# 将处理后的数据写回文件
with open('自动和铁塔_change.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print('处理完成！')