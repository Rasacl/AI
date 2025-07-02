import json

# 读取JSON文件
with open('d:/project/self/AI/twoer.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 检查每个站点的状态
offline_stations = []
for station in data['data']:
    if station['status'] != '在线':
        offline_stations.append({
            'id': station['id'],
            'name': station['name'],
            'status': station['status']
        })

# 打印结果
if offline_stations:
    print('以下站点不在线：')
    for station in offline_stations:
        print(f"站点ID: {station['id']}, 名称: {station['name']}, 状态: {station['status']}")
else:
    print('所有站点都在线')