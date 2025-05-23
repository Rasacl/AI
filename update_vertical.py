import pandas as pd
import json
import random

def dms_to_decimal(dms_str):
    """
    @description 将度分秒格式（以小数点分隔）转换为十进制格式
    @param {str} dms_str 度分秒格式的字符串，如"116.1726"表示116度17分26秒
    @returns {float} 十进制格式的浮点数
    """
    dms_str = str(dms_str).replace(',', '')
    if '.' not in dms_str:
        # 对于没有小数点的数字，在倒数第4位插入小数点
        dms_str = dms_str[:-4] + '.' + dms_str[-4:]
    
    parts = dms_str.split('.')
    degrees = float(parts[0])
    if len(parts) > 1:
        minutes = float(parts[1][:2])
        seconds = float(parts[1][2:] if len(parts[1]) > 2 else 0)
        decimal = degrees + minutes/60 + seconds/3600
        return round(decimal, 6)
    return degrees

def format_coordinate(coord_str):
    """
    @description 处理经纬度格式，转换为十进制格式
    @param {str} coord_str 经纬度字符串
    @returns {float} 十进制格式的浮点数
    """
    return dms_to_decimal(coord_str)

# 读取Excel文件中的所有工作表
excel_file = pd.ExcelFile('垂直设备.xlsx')
sheet_names = excel_file.sheet_names

# 创建一个字典来存储所有工作表的数据
all_sheets_data = {}

# 读取每个工作表的数据
for sheet_name in sheet_names:
    df = pd.read_excel('垂直设备.xlsx', sheet_name=sheet_name)
    sheet_data = df.to_dict('records')
    all_sheets_data[sheet_name] = sheet_data

# 读取现有的JSON文件
with open('垂直设备.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# 遍历Excel中的每个工作表数据
for sheet_name, sheet_data in all_sheets_data.items():
    for row in sheet_data:
        # 获取高度值（处理不同的列名）
        height_value = row.get('高度') if '高度' in row else row.get('海拔高度')
        
        # 创建新的设备对象
        device = {
            "lonLat": [
                format_coordinate(row['经度E']),
                format_coordinate(row['纬度N'])
            ],
            "height": float(str(height_value).replace(',', '')),
            "radarType": [sheet_name],
            "id": str(row['区站号']),
            "district": row['区县'],
            "name": row['站名'],
            "status": random.choice(['可用', '告警']),
        }
        
        # 检查是否已存在相同区站号的设备
        existing_device = None
        for d in json_data['data']:
            if d.get('id') == device['id']:
                existing_device = d
                break
        
        if existing_device:
            # 如果设备已存在，将当前sheet_name添加到radarType列表中
            if sheet_name not in existing_device['radarType']:
                existing_device['radarType'].append(sheet_name)
        else:
            # 如果设备不存在，添加新的设备对象
            json_data['data'].append(device)

# 将更新后的数据写回JSON文件
with open('垂直设备.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

print("数据更新完成！")