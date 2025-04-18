from pathlib import Path


# 获取当前工作目录
p = Path('.')
print(p.cwd())
print(p.absolute())

path = Path('examples.txt')
# 读取文件内容，指定编码为utf-8
content = path.read_text(encoding='utf-8')
print(content)

path = Path('./AI_LLM/python_basic/python标准库/examples.txt')


st = path.stem # 获取文件名
print(st)

su = path.suffix # 获取文件后缀
print(su)

name = path.name # 获取文件名和后缀
print(name)

if path.exists():
    print("文件存在")
    # 读取文件内容，指定编码为utf-8
    content = path.read_text(encoding='utf-8')
    print(content)
    # 写入文件内容，指定编码为utf-8
    path.write_text("Hello, world!", encoding='utf-8')
    
else:
    print("文件不存在")
    
with path.open(mode='w', encoding='utf-8') as file:
    content = file.write("Hello, world! python")
    print(content)