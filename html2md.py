import os
import html2text

# 遍历当前目录下的所有文件
for filename in os.listdir("."):
    # 如果是HTML文件，进行转换
    if filename.endswith(".html"):
        # 将HTML文件读入
        with open(filename, 'r', encoding='utf-8') as f:
            html = f.read()

        # 调用html2text将HTML转换为Markdown
        markdown = html2text.html2text(html)

        # 生成Markdown文件名
        markdown_filename = os.path.splitext(filename)[0] + '.md'

        # 将Markdown写入文件
        with open(markdown_filename, 'w', encoding='utf-8') as f:
            f.write(markdown)

        print(f"Converted {filename} to {markdown_filename}")
