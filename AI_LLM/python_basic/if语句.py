# 分支 - If 语句和布尔值

# 1. 基本的 if 语句
age = 18
if age >= 18:
    print("已成年")

# 2. if-else 语句
score = 85
if score >= 60:
    print("及格")
else:
    print("不及格")

# 3. if-elif-else 多分支
grade = 75
if grade >= 90:
    print("优秀")
elif grade >= 80:
    print("良好")
elif grade >= 60:
    print("及格")
else:
    print("不及格")

# 4. 嵌套 if 语句
age = 20
has_ticket = True
if age >= 18:
    if has_ticket:
        print("可以进入")
    else:
        print("需要购票")
else:
    print("年龄不够")

# 5. 条件表达式（三元运算符）
age = 20
status = "成年" if age >= 18 else "未成年"

# 6. 使用 and、or、not 运算符
age = 25
has_id = True
if age >= 18 and has_id:
    print("可以办理")

# 7. 使用 in 和 not in
fruits = ["苹果", "香蕉", "橙子"]
if "苹果" in fruits:
    print("有苹果")

# 8. 判断值是否为空
name = ""
if not name:
    print("名字为空")

# 9. 多条件判断
score = 85
attendance = 95
if score >= 60 and attendance >= 80:
    print("合格")

# 10. 使用 is 和 is not
x = None
if x is None:
    print("x 是 None")

# 11. 链式比较
age = 18
if 0 <= age <= 100:
    print("年龄合法")

# 12. 使用 any 和 all
numbers = [1, 2, 3, 4, 5]
if any(num > 3 for num in numbers):
    print("存在大于3的数")
if all(num > 0 for num in numbers):
    print("所有数都大于0")

# 13. 复杂条件组合
age = 20
vip_level = 2
score = 85
if (age >= 18 and vip_level > 1) or score >= 90:
    print("可以享受优惠")

# 14. 使用列表推导式配合if
numbers = [1, 2, 3, 4, 5]
even_numbers = [x for x in numbers if x % 2 == 0]

# 15. 使用 pass 语句
if age < 18:
    pass  # 待实现的代码
else:
    print("成年")