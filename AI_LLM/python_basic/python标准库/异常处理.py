# 异常处理

# 1. 基本的try-except结构
try:
    num = int("abc")
except ValueError:
    print("无法将字符串转换为数字")

# 2. 处理多个异常
try:
    result = 10 / 0
    num = int("abc")
except ZeroDivisionError:
    print("除数不能为零")
except ValueError:
    print("无法将字符串转换为数字")

# 3. 使用as捕获异常对象
try:
    file = open("不存在的文件.txt")
except FileNotFoundError as e:
    print(f"文件不存在: {e}")

# 4. 使用else子句
try:
    num = int("123")
except ValueError:
    print("转换失败")
else:
    print(f"转换成功: {num}")

# 5. 使用finally子句
try:
    file = open("test.txt", "w")
    file.write("测试内容")
except IOError:
    print("写入失败")
finally:
    file.close()

# 6. 自定义异常
class MyError(Exception):
    def __init__(self, message):
        self.message = message

# 7. 抛出异常
def check_age(age):
    if age < 0:
        raise ValueError("年龄不能为负数")
    return age

# 8. 异常链
try:
    try:
        raise ValueError("原始错误")
    except ValueError as e:
        raise RuntimeError("新错误") from e
except RuntimeError as e:
    print(f"捕获到异常: {e}")

# 9. 使用assert断言
def divide(a, b):
    assert b != 0, "除数不能为零"
    return a / b

# 10. 上下文管理器处理异常
with open("test.txt", "w") as file:
    file.write("自动关闭文件")

# 11. 捕获所有异常
try:
    result = 1 / 0
except Exception as e:
    print(f"捕获到未知异常: {type(e).__name__}")

# 12. 异常处理嵌套
try:
    try:
        print(undefined_variable)
    except NameError:
        print("变量未定义")
except Exception:
    print("发生其他错误")