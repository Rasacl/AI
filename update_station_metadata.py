import pandas as pd
import json

def convert_longitude(lon_str):
    # 处理经度，如1163847E -> 116°38'47"E -> 116.646389
    if isinstance(lon_str, str) and lon_str.endswith('E'):
        lon = lon_str[:-1]  # 去掉E
        degrees = int(lon[:3])  # 度
        minutes = int(lon[3:5])  # 分
        seconds = int(lon[5:])  # 秒
        decimal = degrees + minutes/60 + seconds/3600
        return decimal
    return None

def convert_latitude(lat_str):
    # 处理纬度，如400329N -> 40°03'29"N -> 40.058056
    if isinstance(lat_str, str) and lat_str.endswith('N'):
        lat = lat_str[:-1]  # 去掉N
        degrees = int(lat[:2])  # 度
        minutes = int(lat[2:4])  # 分
        seconds = int(lat[4:])  # 秒
        decimal = degrees + minutes/60 + seconds/3600
        return decimal
    return None

def convert_time(time_str):
    # 处理时间，如20250213.0 -> 2025-02-13
    if isinstance(time_str, str):
        # 移除小数点及其后面的数字
        time_str = time_str.split('.')[0]
        if len(time_str) == 8:
            return f"{time_str[:4]}-{time_str[4:6]}-{time_str[6:]}"
    return None

# 读取Excel文件
df = pd.read_excel('台站元数据.xlsx')

# 读取JSON文件
with open('自动站.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# 更新JSON数据
    
    
    # 遍历JSON数据
    for station in json_data['data']:
        # 确保类型一致的比较
        matched_row = df[df['区站号'].astype(str).str.strip() == str(station['id']).strip()]
        if not matched_row.empty:
            row = matched_row.iloc[0]
            # 转换经纬度
            lon = convert_longitude(str(row['经度']))
            lat = convert_latitude(str(row['纬度']))
            if lon is not None and lat is not None:
                station['lonLat'] = [lon, lat]
            
            # 转换时间
            time = convert_time(str(row['建站时间']))
            if time is not None:
                station['time'] = time
    
    # 删除没有lonLat的记录
    json_data['data'] = [station for station in json_data['data'] if 'lonLat' in station]



# 保存更新后的JSON文件
with open('自动站.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)