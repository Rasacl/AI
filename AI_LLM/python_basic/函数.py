# 函数的各种应用示例

# 1. 基本函数定义和调用
def greet(name):
    return f"你好，{name}！"

print(greet("张三"))

# 2. 默认参数
def greet_with_title(name, title="先生"):
    return f"你好，{name}{title}！"

print(greet_with_title("张三"))
print(greet_with_title("李四", "女士"))

# 3. 可变参数
def sum_numbers(*args):
    return sum(args)

print(sum_numbers(1, 2, 3, 4, 5))

# 4. 关键字参数
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="张三", age=25, city="北京")

# 5. 返回多个值
def get_person_info():
    return "张三", 25, "北京"

name, age, city = get_person_info()

# 6. 函数作为参数
def apply_operation(x, func):
    return func(x)

def square(x):
    return x ** 2

print(apply_operation(5, square))

# 7. Lambda 函数
multiply = lambda x, y: x * y
print(multiply(3, 4))

# 8. 装饰器
def log_function(func):
    def wrapper(*args, **kwargs):
        print(f"调用函数: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_function
def add(a, b):
    return a + b

print(add(3, 4))

# 9. 递归函数
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)

print(factorial(5))

# 10. 生成器函数
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for num in fibonacci(10):
    print(num)

# 11. 闭包
def counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

my_counter = counter()
print(my_counter())

# 12. 类型提示
def calculate_age(birth_year: int) -> int:
    return 2024 - birth_year

print(calculate_age(1990))

# 13. 异常处理
def divide(a: float, b: float) -> float:
    try:
        return a / b
    except ZeroDivisionError:
        return "除数不能为零"

print(divide(10, 2))
print(divide(10, 0))

# 14. 函数文档字符串
def calculate_bmi(weight: float, height: float) -> float:
    """
    计算体质指数(BMI)
    
    参数:
        weight: 体重(kg)
        height: 身高(m)
    返回:
        BMI值
    """
    return weight / (height ** 2)

print(calculate_bmi.__doc__)

# 15. 偏函数
from functools import partial
power_of_2 = partial(pow, exp=2)
print(power_of_2(4))

# ·····················································Lambda函数·············································
# Lambda 函数的语法结构：
# lambda 参数1, 参数2, ...: 表达式

# 1. 基本语法
multiply = lambda x, y: x * y  # 两个参数的lambda函数

# 2. 无参数lambda
no_args = lambda: "Hello"  # 无参数

# 3. 单参数lambda
square = lambda x: x ** 2  # 单个参数

# 4. 多参数lambda
calculate = lambda x, y, z: x + y * z  # 三个参数

# 5. 带默认值的lambda
greet = lambda name="Guest": f"Hello {name}"  # 默认参数

# 6. lambda配合条件表达式
check = lambda x: "正数" if x > 0 else "负数或零"  # 带条件判断

# 7. lambda在排序中的应用
pairs = [(1, 'one'), (2, 'two'), (3, 'three')]
sorted_pairs = sorted(pairs, key=lambda pair: pair[1])  # 按第二个元素排序

# 8. lambda在map中的应用
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x**2, numbers))

# 9. lambda在filter中的应用
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))