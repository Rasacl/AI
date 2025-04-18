from pathlib import Path
import csv

import matplotlib.pyplot as plt
from datetime import datetime

path = Path('weather.csv')
lines = path.read_text().splitlines() # 读取文件并按行分割
reader = csv.reader(lines) # 读取csv文件
header = next(reader) # 读取第一行
# rows = [row for row in reader] # 读取剩余行

# for index,colum_header in enumerate(header):
#     print(index, colum_header)

temps, data  = [], []
for row in reader:
    temp = row[10]
    temps.append(int(temp))
    current_date = datetime.strptime(row[1], '%Y-%m-%d')  # 转换日期格式
    data.append(current_date)



flg, ax = plt.subplots()
ax.plot(data, temps, c='red')
ax.set_title("Daily high and low temperatures - 2018", fontsize=20)
ax.set_xlabel('', fontsize=16)

flg.autofmt_xdate() # 绘制斜的日期标签，以免它们彼此重叠

ax.set_ylabel("Temperature (F)", fontsize=16)
ax.tick_params(axis='both', which='major', labelsize=16)
plt.show()




