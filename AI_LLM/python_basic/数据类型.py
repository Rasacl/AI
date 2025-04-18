# 字符串



name  = "aaaa"  
age   = 25     # 整数
height = 1.75  # 浮点数
message = '   Hello, ' + name + '!'
mes = f"Hello, {name}! Your age is {age} and your height is {height:.2f} meters." # 字符串拼接
upeer_name = name.upper()

print(upeer_name)
print(type(upeer_name))
print(type(age))
print(type(height))
print(name.title()) # 首字母大写
print(name.lower()) # 全部小写
print(name.upper()) # 全部大写
print(message.strip())  # 去除字符串两端的空格
print(message.rstrip()) # 去除字符串右端的空格
print(message.lstrip()) # 去除字符串左端的空格
print(message.replace('a','b')) # 替换字符串中的字符