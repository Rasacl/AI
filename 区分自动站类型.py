import json

# 定义国家级自动站ID列表
NATIONAL_STATION_IDS = ['54594', '54596', '54597']

# 读取原始JSON文件
with open('d:\\project\\self\\AI\\originExe.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 为每个站点添加type字段
for item in data['data']:
    if item['id'] in NATIONAL_STATION_IDS:
        item['type'] = '国家级自动站'
    else:
        item['type'] = '区域级自动站'

# 将更新后的数据写回文件
with open('d:\\project\\self\\AI\\originExe.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('处理完成！')