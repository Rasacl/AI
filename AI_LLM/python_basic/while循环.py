# while循环

# 1. 基本while循环
count = 0
while count < 5:
    print(count)
    count += 1

# 2. while循环配合else语句
number = 0
while number < 3:
    print(number)
    number += 1
else:
    print("循环结束")

# 3. break语句终止循环
i = 1
while True:
    if i > 5:
        break
    print(i)
    i += 1

# 4. continue语句跳过当前迭代
j = 0
while j < 5:
    j += 1
    if j == 3:
        continue
    print(j)

# 5. 无限循环
"""
while True:
    print("无限循环")
"""

# 6. 循环输入直到满足条件
"""
password = ''
while password != '123456':
    password = input('请输入密码：')
"""

# 7. while循环嵌套
x = 1
while x <= 3:
    y = 1
    while y <= 3:
        print(f"x:{x}, y:{y}")
        y += 1
    x += 1

# 8. 使用while处理列表
numbers = [1, 2, 3, 4, 5]
index = 0
while index < len(numbers):
    print(numbers[index])
    index += 1

# 9. 条件表达式结合while
count = 0
while count := count + 1 < 5:
    print(count)

# 10. while循环实现倒计时
import time
countdown = 5
while countdown > 0:
    print(countdown)
    countdown -= 1
    time.sleep(1)

# 11. 使用while循环查找元素
data = [1, 3, 5, 7, 9]
target = 5
i = 0
while i < len(data):
    if data[i] == target:
        print(f"找到目标：{target}")
        break
    i += 1

# 12. while循环实现菜单
"""
while True:
    print("1. 开始游戏")
    print("2. 设置")
    print("3. 退出")
    choice = input("请选择：")
    if choice == '3':
        break
"""

# 13. 使用while循环删除列表元素
numbers = [1, 2, 3, 2, 4, 2, 5]
while 2 in numbers:
    numbers.remove(2)

# 14. while循环实现累加
sum = 0
n = 1
while n <= 100:
    sum += n
    n += 1
print(f"1到100的和：{sum}")

# 15. while循环实现数据验证
"""
while True:
    age = input("请输入年龄：")
    if age.isdigit() and 0 <= int(age) <= 120:
        break
    print("输入无效，请重新输入")
"""