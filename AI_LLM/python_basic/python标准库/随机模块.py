# 随机模块
from random import randint, choice
"""
randint(a, b) 函数说明：

- 生成一个 [a, b] 范围内的随机整数
- 包含边界值 a 和 b
- a 必须小于等于 b
- 返回值是一个整数
这是最常用的随机整数生成函数，适用于需要在指定范围内生成随机整数的场景。
"""

# 生成1到10之间的随机整数
random_number = randint(1, 10)
print(f"随机数: {random_number}")

# 生成骰子点数
dice = randint(1, 6)
print(f"骰子点数: {dice}")

# 生成随机年份
year = randint(2000, 2024)
print(f"随机年份: {year}")

# 生成随机温度
temperature = randint(-10, 40)
print(f"随机温度: {temperature}°C")

# 生成随机分数
score = randint(0, 100)
print(f"随机分数: {score}")

""""
choice(seq) 函数说明：

- 从给定的序列（如列表、元组或字符串）中随机选择一个元素
"""

# 从列表中随机选择
fruits = ['苹果', '香蕉', '橙子', '葡萄']
random_fruit = choice(fruits)
print(f"随机水果: {random_fruit}")

# 从字符串中随机选择
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
random_letter = choice(letters)
print(f"随机字母: {random_letter}")

# 从元组中随机选择
colors = ('红', '黄', '蓝', '绿', '紫')
random_color = choice(colors)
print(f"随机颜色: {random_color}")

# 生成随机验证码
digits = '0123456789'
verification_code = ''.join(choice(digits) for _ in range(6))
print(f"随机验证码: {verification_code}")

# 随机选择星期
weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
random_day = choice(weekdays)
print(f"随机星期: {random_day}")

