# 字典的各种应用方式

# 1. 创建和访问字典
person = {
    "name": "张三",
    "age": 25,
    "city": "北京"
}
print(person["name"])  # 访问值
print(person.get("age"))  # 使用get方法安全访问

# 2. 修改和添加元素
person["age"] = 26  # 修改值
person["job"] = "程序员"  # 添加新键值对

# 3. 删除元素
del person["city"]  # 删除指定键值对
job = person.pop("job")  # 删除并返回值
last_item = person.popitem()  # 删除并返回最后一个键值对

# 4. 字典方法
keys = person.keys()  # 获取所有键
values = person.values()  # 获取所有值
items = person.items()  # 获取所有键值对

# 5. 遍历字典
for key in person:
    print(key, person[key])

for key, value in person.items():
    print(f"{key}: {value}")

# 6. 字典推导式
squares = {x: x**2 for x in range(5)}

# 7. 合并字典
dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}
dict1.update(dict2)  # 使用update合并
merged = {**dict1, **dict2}  # 使用解包合并

# 8. 嵌套字典
students = {
    "张三": {"age": 20, "score": 90},
    "李四": {"age": 22, "score": 85}
}
print(students["张三"]["score"])

# 9. 默认值处理
from collections import defaultdict
grades = defaultdict(list)
grades["张三"].append(90)  # 自动创建列表

# 10. 有序字典
from collections import OrderedDict
ordered = OrderedDict([('a', 1), ('b', 2)])

# 11. 字典计数
from collections import Counter
words = ["a", "b", "a", "c", "b", "a"]
word_count = Counter(words)

# 12. 字典排序
sorted_dict = dict(sorted(person.items()))  # 按键排序
sorted_by_value = dict(sorted(person.items(), key=lambda x: x[1]))  # 按值排序

# 13. 字典复制
shallow_copy = person.copy()  # 浅拷贝
import copy
deep_copy = copy.deepcopy(person)  # 深拷贝

# 14. 字典键值对交换
inverted = {v: k for k, v in person.items()}

# 15. 字典作为函数参数
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="张三", age=25)

# 16. 字典解构
info = {"name": "张三", "age": 25}
print_info(**info)

# 17. 字典键值验证
if "name" in person:
    print("存在name键")

# 18. 字典视图对象
keys_view = person.keys()
values_view = person.values()
items_view = person.items()

# 19. 字典清空
person.clear()

# 20. 字典格式化字符串
user = {"name": "张三", "age": 25}
print(f"姓名：{user['name']}, 年龄：{user['age']}")