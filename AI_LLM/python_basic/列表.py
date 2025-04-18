# 创建列表
fruit = ['apple', 'banana', 'orange']
print(fruit)

fruit[0] = 'pear' # 修改列表元素
print(fruit)

fruit.append('grape') # 添加元素
print(fruit)

fruit.insert(1, 'peach') # 在指定位置插入元素
print(fruit)

fruit.remove('orange') # 删除指定元素
print(fruit)

fruit.pop(2) # 删除指定位置的元素
print(fruit)

fruit.sort() # 排序
print(fruit)

fruit.reverse() # 反转
print(fruit)

print(len(fruit)) # 获取列表长度
print(fruit.index('pear')) # 获取元素在列表中的位置
print(fruit.count('pear')) # 统计元素在列表中出现的次数
print(fruit[1:3]) # 切片，获取指定范围内的元素

# while循环
i = 0
while i < len(fruit):
    print(fruit[i])
    i += 1

# for循环
for f in fruit:
    print(f)
    
nums = [1, 2, 3, 4, 5]

max_num = max(nums)
min_num = min(nums)
sum_nums = sum(nums)

print("最大值：", max_num)
print("最小值：", min_num)
print("总和：", sum_nums)

even_nums = list(range(0,100, 2))

print("偶数列表：", even_nums)


# 列表推导式
squares = [x**2 for x in range(1, 11)]
print(squares)


