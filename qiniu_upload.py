import os
import re
import requests
import qiniu
from qiniu import Auth, put_data
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 七牛云配置
access_key = os.getenv("QINIU_AK")
secret_key = os.getenv("QINIU_SK")
bucket_name = os.getenv("QINIU_BUCKET")
cdn_domain = os.getenv("QINIU_DOMAIN")
dir_path = os.getenv("QINIU_DIR")

# 初始化Auth
q = Auth(access_key, secret_key)

# 初始化BucketManager
bucket = qiniu.BucketManager(q)

# 获取文件列表
files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.md')]

# 遍历文件
for file in files:
    # 读取文件内容
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 匹配图片链接
    pattern = re.compile(r'!\[.*?\]\((.*?)\)')
    matches = pattern.findall(content)

    # 遍历链接
    for url in matches:
        if url.startswith('http'):
            # 如果是网络链接，则下载图片
            img_data = requests.get(url).content
        else:
            # 如果是本地文件，则读取文件内容
            with open(url, 'rb') as f:
                img_data = f.read()

        # 获取文件名
        filename = os.path.basename(url)
        # 去掉空字符
        filename = filename.replace('\x00', '')

        key = f'{dir_path}/{filename}'
        # 上传图片到七牛云
        ret, info = put_data(q.upload_token(bucket_name), key, img_data)
        print(f'{filename}上传情况：{info}')  
        # 替换链接
        new_url = f'https://{cdn_domain}/{key}'
        content = content.replace(url, new_url)

    # 保存文件
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'{file} 处理完成')
