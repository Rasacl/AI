import json
import pandas as pd
import re

def clean_text(text):
    """清理文本中的非法字符"""
    if not isinstance(text, str):
        return text
    # 移除控制字符
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    # 移除特殊空格
    text = text.replace('\u00A0', ' ')
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
        if '.' in code:
            code = str(int(float(code)))
    status_map = {
        "1": "业务正常",
        "2": "业务开通，但近7天未产生业务数据",
        "3": "业务未开通",
        "0": "业务未开通"
    }
    result = status_map.get(str(code), "未知状态")
    if result == "未知状态":
        print(f"发现未知业务状态码: {code}, 类型: {type(code)}, 值: {str(code)}, 状态: {type(str(code))}")
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
        if '.' in code:
            code = str(int(float(code)))
    status_map = {
        "1": "已开通",
        "2": "未开通",
        "3": "未开通"
    }
    result = status_map.get(str(code), "未知状态")
    if result == "未知状态":
        print(f"发现未知异地就医状态码: {code}, 类型: {type(code)}")
    return result

# 直接用pandas读取JSON文件
df = pd.read_json('全国定点医院数据.json', encoding='utf-8')

# 重命名列
df = df.rename(columns={
    'uscc': '统一社会信用代码',
    'medinsName': '药店名称',
    'rtalPhacCode': '机构编码',
    'drugBizScp': '经营范围',
    'addr': '详细地址',
    'tel': '联系电话'
})



# 使用apply方法批量处理状态转换
df['移动支付'] = df['businessLvMpc'].fillna('3').apply(get_business_status)
df['电子凭证'] = df['businessLvCfc'].fillna('3').apply(get_business_status)
df['电子处方'] = df['businessLvEpc'].fillna('3').apply(get_business_status)
df['电子票据'] = df['businessLvEbc'].fillna('3').apply(get_business_status)
df['医保钱包'] = df['businessLvWlt'].fillna('3').apply(get_business_status)
df['异地就医服务'] = df['businessLvOutMedOtp'].fillna('2').apply(get_outmed_status)

# 选择需要的列
final_columns = ['统一社会信用代码', '药店名称', '机构编码', '经营范围', '详细地址', '联系电话',
                '移动支付', '电子凭证', '电子处方', '电子票据', '医保钱包', '异地就医服务']
df = df[final_columns]

# 清理所有文本字段中的非法字符
text_columns = ['统一社会信用代码', '药店名称', '机构编码', '经营范围', '详细地址', '联系电话']
for column in text_columns:
    df[column] = df[column].apply(clean_text)

# 保存到Excel
df.to_excel('医院数据统计.xlsx', index=False)
print(f'数据已保存到Excel文件，共处理{len(df)}条记录')