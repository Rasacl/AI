import os

# 目标文件夹
folder_path = r"D:\project\uino\mobile-group-3d\public\images\ai-data\load"

# 获取所有 png 文件，按文件名排序
files = sorted([f for f in os.listdir(folder_path) if f.endswith(".png")])

# 遍历并重命名
for index, filename in enumerate(files, start=1):
    old_path = os.path.join(folder_path, filename)
    new_name = f"frame_{index}.png"
    new_path = os.path.join(folder_path, new_name)
    
    os.rename(old_path, new_path)
    print(f"重命名: {filename} -> {new_name}")

print("✅ 所有文件重命名完成！")
