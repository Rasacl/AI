import pandas as pd
import json

def convert_longitude_dms(dms_str):
    """将经度的度分秒格式转换为十进制度"""
    if not isinstance(dms_str, str):
        return None
    try:
        # 提取度分秒，经度取前3位作为度
        degrees = int(dms_str[:3])
        minutes = int(dms_str[3:5])
        seconds = int(dms_str[5:])
        # 转换为十进制度
        decimal = degrees + minutes/60 + seconds/3600
        return str(round(decimal, 4))
    except:
        return None

def convert_latitude_dms(dms_str):
    """将纬度的度分秒格式转换为十进制度"""
    if not isinstance(dms_str, str):
        return None
    try:
        # 提取度分秒，纬度取前2位作为度
        degrees = int(dms_str[:2])
        minutes = int(dms_str[2:4])
        seconds = int(dms_str[4:])
        # 转换为十进制度
        decimal = degrees + minutes/60 + seconds/3600
        return str(round(decimal, 4))
    except:
        return None

def get_station_type(type_str):
    """根据类型字符串返回对应的铁塔站类型"""
    type_mapping = {
        '交通站': '铁塔交通站',
        '智慧站': '铁塔智慧站',
        '梯度站': '铁塔梯度站',
        '四要素': '铁塔四要素站',
        '花粉站': '铁塔四要素站'
    }
    return type_mapping.get(type_str, '铁塔站')

def main():
    # 读取Excel文件的铁塔tab页
    df = pd.read_excel('站点要素分类.xlsx', sheet_name='铁塔')
    
    # 准备JSON数据结构
    json_data = {
        "code": 200,
        "success": True,
        "data": [],
        "msg": "操作成功"
    }
    
    # 遍历Excel数据
    for _, row in df.iterrows():
        print(row)
        station = {
            "id": str(row['区站号']).strip(),
            "name": str(row['站名']).strip(),
            "lonLat": [
                convert_longitude_dms(str(row['经度(度分秒)'])),
                convert_latitude_dms(str(row['纬度（度分秒）']))
            ],
            "district": str(row['县区']).strip(),
            "height": str(row['测站海拔高度（m）']),
            "status": "正常",
            "time": str(row['建站时间（数据到中心站）']).split(' ')[0],  # 只保留日期部分
            "type": get_station_type(str(row['类型']))
        }
        json_data['data'].append(station)
    
    # 保存为JSON文件
    with open('铁塔站.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()