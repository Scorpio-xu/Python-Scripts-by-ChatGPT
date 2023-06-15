import os

# 打开文件夹，获取md文件列表
folder_path = './'
md_files = [f for f in os.listdir(folder_path) if f.endswith('.md')]

# 按文件名排序
md_files.sort()

# 合并文件
with open('merged.md', 'w', encoding='utf-8') as f:
    for md_file in md_files:
        with open(os.path.join(folder_path, md_file), 'r', encoding='utf-8') as mf:
            f.write(mf.read())
