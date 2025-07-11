import pandas as pd
import re
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time
import json


# 清理非法字符
def clean_string(s):
    if isinstance(s, str):
        return re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f]', '', s)
    return s


# 递归提取所有层级的编码和名称
def extract_code_name(items):
    result = []
    for item in items:
        # 处理直辖市（admdvsLv为1）
        if item['admdvsLv'] == '1' and item['code'] in ['110000', '120000', '310000', '500000']:
            result.append({
                'province_name': item['name'],
                'province_code': item['code'],
                'city_name': item['name'],
                'city_code': item['code']
            })
        # 处理普通省份
        elif item['admdvsLv'] == '1':
            province_name = item['name']
            province_code = item['code']
            # 遍历该省份下的所有城市
            for city in item.get('list', []):
                if city['admdvsLv'] == '2':
                    result.append({
                        'province_name': province_name,
                        'province_code': province_code,
                        'city_name': city['name'],
                        'city_code': city['code']
                    })
    return result

def create_session(max_retries=3, backoff_factor=1):
    """创建带有重试机制的请求会话"""
    session = requests.Session()
    retry_strategy = Retry(
        total=max_retries,
        backoff_factor=backoff_factor,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount('https://', adapter)
    return session


def fetch_data(regnCode):
    url = f'https://fuwu.nhsa.gov.cn/ebus/fuwu/api/nthl/api/CommQuery/queryFixedHospital'
    payload_template = {
        "data": {
            "encData": "3DFBCA4667B978F639BB23B95DCE4CC74CE34C33DC32F1068E9E23CA546C9EA8CCD20943B4DAE96380B41164D761DE9742C84A985FE3BABC31CB352556BB87C9C1495DB24A29AB6BC3A85AB7FCA00F33C56677481A67C67F739EE2C7D589054DC373615B5DDB33C24C5B31E61CB7643E8CCAA19EAE1FD36157CF9869E3A3753E0557E5717A55670E908B6C0313C7B8E5B157AFE906331B82E181D018F516AAA5",
            "addr": "",
            "regnCode": regnCode['city_code'],
            "medinsName": "",
            "medinsLvCode": "",
            "medinsTypeCode": "",
            "openElec": "",
            "pageNum": 1,
            "pageSize": 100,
            "queryDataSource": "es"
        },
        "encType": "SM4",
        "signData": "your_sign_data",
        "signType": "SM2",
        "timestamp": 1712110149,
        "version": "1.0.0",
    }

    all_data = []
    has_more_data = True
    page_num = 1

    # 创建带有重试机制的会话
    session = create_session(max_retries=5, backoff_factor=2)

    while has_more_data:
        payload = payload_template.copy()
        payload["data"]["pageNum"] = page_num

        try:
            response = session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            current_data = data['data']['list']
            print(f"返回数据{len(current_data)}条，正在抓取第{page_num}页数据, 地区编码: {regnCode}")

            for item in current_data:
                item['province_name'] = regnCode['province_name']
                item['province_code'] = regnCode['province_code']
                item['city_name'] = regnCode['city_name']
                item['city_code'] = regnCode['city_code']

            all_data.extend(current_data)

            if len(current_data) < 100:
                has_more_data = False
            else:
                page_num += 1
                # 添加页间延迟，减轻服务器负担
                time.sleep(0.5)

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP错误 (编码: {regnCode}, 页码: {page_num}): {http_err}")
            # 对于5xx错误，等待一段时间后重试该页
            if response.status_code >= 500:
                print(f"服务器错误，等待3秒后重试第{page_num}页...")
                time.sleep(3)
                continue
            else:
                break
        except requests.exceptions.RequestException as req_err:
            print(f"请求异常 (编码: {regnCode}, 页码: {page_num}): {req_err}")
            # 网络异常，等待一段时间后重试该页
            print(f"网络异常，等待5秒后重试第{page_num}页...")
            time.sleep(5)
            continue
        except Exception as e:
            print(f"未知错误 (编码: {regnCode}, 页码: {page_num}): {e}")
            break

    return all_data


def main():
    # 读取行政区划代码表
    with open('./全国定点医疗机构/arr_code.json', 'r', encoding='utf-8') as f:
        arr_code_data = json.load(f)
    print(arr_code_data,111111)
    # 创建编码到名称的映射字典
    code_to_name = extract_code_name(arr_code_data)

    
    print(code_to_name)
    all_data = []
    # 顺序遍历regnCode
    for i, regnCode in enumerate(code_to_name, 1):
        print(f"\n===== 开始处理地区 {i}/{len(code_to_name)}: 省份 {regnCode['province_name']}-省份代码 {regnCode['province_code']}- 城市 {regnCode['city_name']}-城市代码 {regnCode['city_code']} =====")
        data = fetch_data(regnCode)
        all_data.extend(data)
        # 添加地区间延迟，进一步减轻服务器负担
        time.sleep(1)

    df = pd.DataFrame(all_data)

    # 添加地区名称映射

    # 选择需要的列并设置中文列名
    df_filtered = df[['province_code','province_name','city_code','city_name', 'medinsName', 'medinsTypeName', 'medinsLvName', 'addr']]

    df_filtered.columns = ['省份编码','省份名称','城市编码','城市名称', '医疗机构名称', '医疗机构类型', '医疗机构等级',
                           '详细地址']

    # 清理数据
    df_filtered = df_filtered.map(clean_string)

    # 保存到 Excel
    df_filtered.to_excel('全国定点医院机构查询.xlsx', index=False)
    print(f'数据已写入表格，共计{len(df)}条记录')


if __name__ == '__main__':
    main()