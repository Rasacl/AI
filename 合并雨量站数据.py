# import pandas as pd
# import json

# # 读取Excel文件
# excel_file = 'd:\\project\\self\\AI\\245雨量站站点信息.xlsx'
# json_file = 'd:\\project\\self\\AI\\originExe.json'

# # 读取Excel数据
# df = pd.read_excel(excel_file)

# # 读取现有的JSON文件
# with open(json_file, 'r', encoding='utf-8') as f:
#     json_data = json.load(f)

# # 遍历Excel数据并转换为所需格式
# for _, row in df.iterrows():
#     new_station = {
#         "id": str(row['stcd']),  # 确保ID是字符串类型
#         "name": row['stnm'],
#         "district": row['addvcdname'],
#         "status": "在线",
#         "height": 0,
#         "elementLevel": None,
#         "lonLat": [float(row['lgtd']), float(row['lttd'])],
#         "time": None,
#         "type": "行业共享站"
#     }
#     json_data['data'].append(new_station)

# # 将更新后的数据写回JSON文件
# with open(json_file, 'w', encoding='utf-8') as f:
#     json.dump(json_data, f, ensure_ascii=False, indent=2)

# print('数据合并完成！')




import pandas as pd
import json

def dms_to_decimal(dms_str):
    """
    将度分秒格式转换为十进制格式
    @description 处理经纬度格式，转换为十进制格式
    @param dms_str: 度分秒格式的字符串或数字
    @return: 十进制格式的浮点数
    """
    try:
        # 将输入转换为字符串
        dms_str = str(dms_str)
        
        # 处理连续数字格式（如1155244表示115度52分44秒）
        if dms_str.isdigit():
            # 从右向左分别取出秒、分、度
            seconds = float(dms_str[-2:]) if len(dms_str) >= 2 else 0
            minutes = float(dms_str[-4:-2]) if len(dms_str) >= 4 else 0
            degrees = float(dms_str[:-4]) if len(dms_str) > 4 else float(dms_str)
            
            decimal = degrees + minutes/60 + seconds/3600
            return decimal
            
        # 处理原有的度分秒格式（度°分'秒"）
        dms_str = dms_str.replace('°', ' ').replace('\'', ' ').replace('"', ' ')
        parts = dms_str.strip().split()
        if len(parts) == 3:
            degrees = float(parts[0])
            minutes = float(parts[1])
            seconds = float(parts[2])
            decimal = degrees + minutes/60 + seconds/3600
            return decimal
        else:
            return float(dms_str)  # 如果已经是十进制格式，直接返回
    except:
        return 0.0  # 转换失败返回0

# 读取Excel文件
excel_file = 'd:\\project\\self\\AI\\规自委580站经纬度高程等台站信息.xlsx'
json_file = 'd:\\project\\self\\AI\\originExe.json'

# 读取Excel数据
df = pd.read_excel(excel_file)

# 读取现有的JSON文件
with open(json_file, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# 遍历Excel数据并转换为所需格式
for _, row in df.iterrows():
    print(row, 1111)
    # 转换经纬度为十进制格式
    longitude = dms_to_decimal(row['经度'])
    latitude = dms_to_decimal(row['纬度'])
    
    new_station = {
        "id": str(row['站点号']),  # 确保ID是字符串类型
        "name": row['监测点'],
        "district": row['区'],
        "status": "在线",
        "height": 0,
        "elementLevel": None,
        "lonLat": [longitude, latitude],
        "time": None,
        "type": "行业共享站"
    }
    json_data['data'].append(new_station)

# 将更新后的数据写回JSON文件
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

print('数据合并完成！')