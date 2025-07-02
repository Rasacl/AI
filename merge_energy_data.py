import pandas as pd
import json

# 读取Excel文件
df = pd.read_excel('d:\\project\\self\\AI\\变电站位置.xlsx')

# 读取现有的能源.json文件
with open('d:\\project\\self\\AI\\能源.json', 'r', encoding='utf-8') as f:
    energy_data = json.load(f)

# 转换Excel数据为指定格式
for _, row in df.iterrows():
    # 检查 LONGITUDE 和 LATITUDE 是否有值
    if pd.notna(row['LONGITUDE']) and pd.notna(row['LATITUDE']):
        print(row)
        new_station = {
            "stationId": str(row['ID']),  # 确保ID转为字符串
            "stationType": "变电站",
            "stationName": row['NAME'],
            "lonLat": [float(row['LONGITUDE']), float(row['LATITUDE'])],
            "height": 32000,
            "markerState": False
        }
        energy_data['data'].append(new_station)

# 将更新后的数据写回文件
with open('d:\\project\\self\\AI\\能源.json', 'w', encoding='utf-8') as f:
    json.dump(energy_data, f, ensure_ascii=False, indent=2)

print('数据合并完成！')