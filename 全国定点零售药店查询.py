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
        return re.sub(r"[\x00-\x08\x0b-\x0c\x0e-\x1f]", "", s)
    return s


# 递归提取所有层级的编码和名称
def extract_code_name(items):
    result = []
    for item in items:
        # 处理直辖市（admdvsLv为1）
        if item["admdvsLv"] == "1" and item["code"] in [
            "110000",
            "120000",
            "310000",
            "500000",
        ]:
            result.append(
                {
                    "province_name": item["name"],
                    "province_code": item["code"],
                    "city_name": item["name"],
                    "city_code": item["code"],
                }
            )
        # 处理普通省份
        elif item["admdvsLv"] == "1":
            province_name = item["name"]
            province_code = item["code"]
            # 遍历该省份下的所有城市
            for city in item.get("list", []):
                result.append(
                    {
                        "province_name": province_name,
                        "province_code": province_code,
                        "city_name": city["name"],
                        "city_code": city["code"],
                    }
                )
    return result


def create_session(max_retries=3, backoff_factor=1):
    """创建带有重试机制的请求会话"""
    session = requests.Session()
    retry_strategy = Retry(
        total=max_retries,
        backoff_factor=backoff_factor,
        status_forcelist=[500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    return session


def fetch_data(regnCode):
    url = (
        f"https://fuwu.nhsa.gov.cn/ebus/fuwu/api/nthl/api/CommQuery/queryRtalPhacBInfo"
    )
    payload_template = {
        "data": {
            "encData": "3DFBCA4667B978F639BB23B95DCE4CC74CE34C33DC32F1068E9E23CA546C9EA8CCD20943B4DAE96380B41164D761DE97BBBD5DB53EA5E7154071E74EF0BE481E2BADC2FDCC843E425B4CA14CEDBC102CA979CA4202C06C9F2CD837D90C6DA45E64DE712DF3683DE81C358841664CBE17561D0390069F11B0D412FE38BE15BA5C",
            "regnCode": regnCode["city_code"],
            "addr": "",
            "businessLvOutMedOtp": "",
            "medinsName": "",
            "pageNum": 1,
            "pageSize": 100,
            "queryDataSource": "es",
        },
        "appCodo": "T98HPCGN5ZVVQBS8LZQNOAEXVI9GYHKQ",
        "encType": "SM4",
        "signData": "qtybVSdrcTtBKvbkU6yjseERgq7PzzPHpds6rKTvoAYjvlSHlvDQ9uZ65w911wTX24qbGPyg0SpBF",
        "signType": "SM2",
        "timestamp": int(time.time()),
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
            current_data = data["data"]["list"]
            print(
                f"返回数据{len(current_data)}条，正在抓取第{page_num}页数据, 地区编码: {regnCode}"
            )

            for item in current_data:
                item["province_name"] = regnCode["province_name"]
                item["province_code"] = regnCode["province_code"]
                item["city_name"] = regnCode["city_name"]
                item["city_code"] = regnCode["city_code"]

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


def clean_text(text):
    """清理文本中的非法字符"""
    if not isinstance(text, str):
        return text
    # 移除控制字符
    text = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", text)
    # 移除特殊空格
    text = text.replace("\u00A0", " ")
    return text.strip()


def get_business_status(code):
    """转换业务状态码为对应的状态说明"""
    # 如果是浮点数，转换为整数
    if isinstance(code, float):
        code = int(code)
    # 如果是字符串，清理并转换
    elif isinstance(code, str):
        # 移除空格
        code = code.strip()
        # 如果包含小数点，转换为整数
        if "." in code:
            code = str(int(float(code)))
    status_map = {
        "1": "业务正常",
        "2": "业务开通，但近7天未产生业务数据",
        "3": "业务未开通",
        "0": "业务未开通",
    }
    result = status_map.get(str(code), "未知状态")
    if result == "未知状态":
        print(
            f"发现未知业务状态码: {code}, 类型: {type(code)}, 值: {str(code)}, 状态: {type(str(code))}"
        )
    return result


def get_outmed_status(code):
    """转换异地就医服务状态码"""
    # 如果是浮点数，转换为整数
    if isinstance(code, float):
        code = int(code)
    # 如果是字符串，清理并转换
    elif isinstance(code, str):
        # 移除空格
        code = code.strip()
        # 如果包含小数点，转换为整数
        if "." in code:
            code = str(int(float(code)))
    status_map = {"1": "已开通", "2": "未开通", "3": "未开通"}
    result = status_map.get(str(code), "未知状态")
    if result == "未知状态":
        print(f"发现未知异地就医状态码: {code}, 类型: {type(code)}")
    return result


def jsontoexecl():
    df = pd.read_json("全国定点零售药店数据.json", encoding="utf-8")

    # 重命名列
    df = df.rename(
        columns={
            "province_name": "省",
            "province_code": "省编码",
            "city_name": "市",
            "city_code": "市编码",
            "uscc": "统一社会信用代码",
            "medinsName": "药店名称",
            "rtalPhacCode": "机构编码",
            "drugBizScp": "经营范围",
            "addr": "详细地址",
            "tel": "联系电话",
        }
    )

    # 使用apply方法批量处理状态转换
    df["移动支付"] = df["businessLvMpc"].fillna("3").apply(get_business_status)
    df["电子凭证"] = df["businessLvCfc"].fillna("3").apply(get_business_status)
    df["电子处方"] = df["businessLvEpc"].fillna("3").apply(get_business_status)
    df["电子票据"] = df["businessLvEbc"].fillna("3").apply(get_business_status)
    df["医保钱包"] = df["businessLvWlt"].fillna("3").apply(get_business_status)
    df["异地就医服务"] = df["businessLvOutMedOtp"].fillna("2").apply(get_outmed_status)

    # 选择需要的列
    final_columns = [
        "省",
        "省编码",
        "市",
        "市编码",
        "统一社会信用代码",
        "药店名称",
        "机构编码",
        "经营范围",
        "详细地址",
        "联系电话",
        "移动支付",
        "电子凭证",
        "电子处方",
        "电子票据",
        "医保钱包",
        "异地就医服务",
    ]
    df = df[final_columns]

    # 清理所有文本字段中的非法字符
    text_columns = [
        "省",
        "省编码",
        "市",
        "市编码",
        "统一社会信用代码",
        "药店名称",
        "机构编码",
        "经营范围",
        "详细地址",
        "联系电话",
    ]

    for column in text_columns:
        df[column] = df[column].apply(clean_text)

    # 保存到Excel
    df.to_excel("全国定点零售药店数据.xlsx", index=False)
    print(f"数据已保存到Excel文件，共处理{len(df)}条记录")


def main():
    # 读取行政区划代码表
    with open("arr_code.json", "r", encoding="utf-8") as f:
        arr_code_data = json.load(f)

    # 创建编码到名称的映射字典
    code_to_name = extract_code_name(arr_code_data)

    all_data = []
    # 顺序遍历regnCode
    for i, regnCode in enumerate(code_to_name, 1):
        print(regnCode)
        print(
            f"\n===== 开始处理地区 {i}/{len(code_to_name)}: 省份 {regnCode['province_name']}-省份代码 {regnCode['province_code']}- 城市 {regnCode['city_name']}-城市代码 {regnCode['city_code']} ====="
        )
        data = fetch_data(regnCode)
        all_data.extend(data)
        # 添加地区间延迟，进一步减轻服务器负担
        time.sleep(1)
    # 将数据保存为JSON文件
    with open("全国定点零售药店数据.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print(f"数据已保存到JSON文件，共计{len(all_data)}条记录")

    jsontoexecl()


if __name__ == "__main__":
    main()
