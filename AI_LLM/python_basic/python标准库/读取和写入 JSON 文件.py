# 读取和写入 JSON 文件
import json
from pathlib import Path

# 1. 写入 JSON 文件
data = {
    "name": "张三",
    "age": 25,
    "cities": ["北京", "上海", "广州"],
    "info": {
        "job": "程序员",
        "salary": 15000
    }
}

# 将数据写入 JSON 文件
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# 2. 读取 JSON 文件
with open('data.json', 'r', encoding='utf-8') as f:
    loaded_data = json.load(f)
print("从文件读取的数据:", loaded_data)

# 3. JSON 字符串转换
json_str = json.dumps(data, ensure_ascii=False, indent=4)
print("JSON字符串:", json_str)

# 4. JSON 字符串解析
parsed_data = json.loads(json_str)
print("解析的数据:", parsed_data)

# 5. 处理复杂对象
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# 自定义 JSON 编码器
class PersonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Person):
            return {"name": obj.name, "age": obj.age}
        return super().default(obj)

# 使用自定义编码器
person = Person("李四", 30)
person_json = json.dumps(person, cls=PersonEncoder, ensure_ascii=False)
print("对象转JSON:", person_json)

# 6. 格式化保存
complex_data = {
    "users": [
        {"id": 1, "name": "张三", "active": True},
        {"id": 2, "name": "李四", "active": False}
    ],
    "settings": {
        "theme": "dark",
        "notifications": True
    }
}

# 保存为格式化的 JSON 文件
with open('complex_data.json', 'w', encoding='utf-8') as f:
    json.dump(complex_data, f, ensure_ascii=False, indent=4)

# 7. 读取并更新 JSON 文件
def update_json_file(file_path, key, value):
    # 读取现有数据
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 更新数据
    data[key] = value
    
    # 保存更新后的数据
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 使用更新函数
update_json_file('data.json', 'new_key', '新值')