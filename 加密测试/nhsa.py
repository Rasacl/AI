# 添加所需的导入
import subprocess
from functools import partial

subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs
import requests
import json
import os
from datetime import datetime


# 在decrypt_response_data函数中添加空值检查
def decrypt_response_data(encrypted_data):
    """解密响应数据"""
    if not encrypted_data or not isinstance(encrypted_data, dict):
        raise ValueError("加密数据格式错误：不是有效的字典")

    if "data" not in encrypted_data:
        raise ValueError("加密数据缺少data字段")

    if not encrypted_data["data"] or not isinstance(encrypted_data["data"], dict):
        raise ValueError("data字段格式错误")

    if "data" not in encrypted_data["data"] or not encrypted_data["data"]["data"]:
        raise ValueError("data.data字段缺失或为空")

    if "encData" not in encrypted_data["data"]["data"]:
        raise ValueError("缺少encData字段")

    decrypted_data = nhsa_js.call("getDecryptedData", encrypted_data)

    # 添加空值检查
    if decrypted_data is None:
        raise ValueError("解密失败：返回值为None")

    # 处理字符串类型的结果
    if isinstance(decrypted_data, str):
        try:
            decrypted_data = json.loads(decrypted_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON解析失败：{str(e)}")

    # 确保结果是字典类型
    if not isinstance(decrypted_data, dict):
        raise ValueError(
            f"解密结果格式错误：预期字典类型，实际是{type(decrypted_data)}"
        )

    return decrypted_data


# 读取并编译 JS 文件
with open("./加密测试/nhsa.js", "r", encoding="utf-8") as f:
    nhsa_js = execjs.compile(f.read())

# API URLs
result_url = (
    "https://fuwu.nhsa.gov.cn/ebus/fuwu/api/nthl/api/CommQuery/queryRtalPhacBInfo"
)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"


def get_headers():
    """获取 header 参数，每次请求改变"""
    headers = nhsa_js.call("getHeaders")
    headers.update(
        {
            "User-Agent": UA,
            "Content-Type": "application/json",
            "Host": "fuwu.nhsa.gov.cn",
            "Origin": "https://fuwu.nhsa.gov.cn",
            "Referer": "https://fuwu.nhsa.gov.cn/nationalHallSt/",
        }
    )
    return headers


def save_to_json(data, filename=None):
    """将数据保存到JSON文件"""
    if filename is None:
        # 使用当前时间创建文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"hospital_data_{timestamp}.json"

    # 确保文件路径存在
    os.makedirs(
        (
            os.path.dirname(os.path.abspath(filename))
            if os.path.dirname(filename)
            else "."
        ),
        exist_ok=True,
    )

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"数据已保存到文件: {filename}")
    return filename


def get_result(output_file=None):
    """获取搜索结果并保存到JSON文件"""
    all_results = []

    for page in range(1, int(1) + 1):
        payload = {
            "addr": "",
            "regnCode": "110000",
            "medinsName": "",
            "businessLvOutMedOtp": "",
            "pageNum": page,
            "pageSize": 10,
            "queryDataSource": "es",
        }

        try:
            # 加密数据
            try:
                encrypted_payload = nhsa_js.call("getEncryptedData", payload)
                if encrypted_payload is None:
                    print("加密数据失败：getEncryptedData 返回 None")
                    continue
            except execjs.RuntimeError as e:
                print(f"JavaScript 运行时错误：{str(e)}")
                continue

            # 发送请求
            response = requests.post(
                url=result_url, json=encrypted_payload, headers=get_headers()
            )
            if not response.ok:
                print(f"请求失败：HTTP {response.status_code}")
                continue

            try:
                encrypted_data = response.json()
            except json.JSONDecodeError as e:
                print(f"响应数据解析失败：{str(e)}")
                continue

            if not encrypted_data:
                print("请求返回数据为空")
                continue

            # 解密数据
            try:
                decrypted_data = decrypt_response_data(encrypted_data)
                print(f"第{page}页数据解密成功")

                # 将解密后的数据添加到结果列表
                if "data" in decrypted_data and "list" in decrypted_data["data"]:
                    all_results.extend(decrypted_data["data"]["list"])
                else:
                    all_results.append(decrypted_data)

            except ValueError as e:
                print(str(e))
                continue
            except execjs.RuntimeError as e:
                print(f"JavaScript 解密错误：{str(e)}")
                continue
            except Exception as e:
                print(f"解密数据时出错：{str(e)}")
                continue

        except requests.exceptions.RequestException as e:
            print(f"网络请求错误：{str(e)}")
        except Exception as e:
            print(f"执行出错：{str(e)}")
            import traceback

            print(traceback.format_exc())

    # 将所有结果保存到JSON文件
    if all_results:
        return save_to_json(all_results, output_file)
    else:
        print("没有获取到任何数据，不创建JSON文件")
        return None


def main():
    # 获取脚本所在的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 指定输出文件名，保存到脚本所在目录
    output_file = os.path.join(script_dir, "hospital_data.json")
    get_result(output_file)


if __name__ == "__main__":
    main()
