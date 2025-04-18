# 1. 基本创建和访问
basic_tuple = ("张三", "李四", "王五")
print(basic_tuple[0])  # 访问单个元素
print(basic_tuple[-1])  # 访问最后一个元素

# 2. 元组解包
name, age, city = ("张三", 25, "北京")
print(f"姓名: {name}, 年龄: {age}, 城市: {city}")

# 3. 返回多个值
def get_person_info():
    return "张三", 25, "北京"
name, age, city = get_person_info()

# 4. 元组作为字典键
person_dict = {
    ("张三", "001"): "销售部",
    ("李四", "002"): "技术部"
}
print(person_dict[("张三", "001")])

# 5. 元组切片
numbers = (0, 1, 2, 3, 4, 5)
print(numbers[1:4])  # 切片操作
print(numbers[::2])  # 步长切片

# 6. 元组方法
repeat_tuple = (1, 2, 2, 3, 2)
print(repeat_tuple.count(2))  # 计数
print(repeat_tuple.index(3))  # 查找索引

# 7. 元组嵌套
nested_tuple = ((1, 2), (3, 4), (5, 6))
print(nested_tuple[0][1])  # 访问嵌套元素

# 8. 元组与列表转换
tuple_to_list = list(("张三", "李四", "王五"))
list_to_tuple = tuple(["张三", "李四", "王五"])

# 9. 元组拼接
tuple1 = (1, 2, 3)
tuple2 = (4, 5, 6)
combined_tuple = tuple1 + tuple2

# 10. 元组重复
repeated_tuple = (1, 2) * 3
print(repeated_tuple)  # 输出: (1, 2, 1, 2, 1, 2)

# 11. 元组比较
tuple1 = (1, 2, 3)
tuple2 = (1, 2, 4)
print(tuple1 < tuple2)  # True

# 12. 元组推导式（生成器表达式）
generator = tuple(x for x in range(5))
print(generator)

# 13. 使用enumerate
for index, value in enumerate(("张三", "李四", "王五")):
    print(f"索引: {index}, 值: {value}")

# 14. 元组作为函数参数
def print_info(name, age, city):
    print(f"姓名: {name}, 年龄: {age}, 城市: {city}")

info = ("张三", 25, "北京")
print_info(*info)  # 解包作为参数传递

# 15. 命名元组
from collections import namedtuple
Person = namedtuple('Person', ['name', 'age', 'city'])
person = Person("张三", 25, "北京")
print(person.name, person.age, person.city)