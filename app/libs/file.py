import io
import requests
from PIL import Image  

def urldownload(url, filepath=None, headers=None):
    """
    下载文件到指定目录
    :param url: 文件下载的url, e.g: "https://img3.doubanio.com/lpic/s1326052.jpg"
    :param filepath: 要存放的目录及文件名, e.g: app/static/images/book/s1326052.jpg
    """
    if not filepath:
        raise ValueError

    current_number = 1
    response = requests.get(url,  headers=headers)
    # print(response.status_code)
    # print(response.headers['Content-Length'])
    while current_number <= 5:
        if response.status_code!=200:
            response = requests.get(url,  headers=headers,stream=True)
        else:
            break
        current_number += 1
    
    with open(filepath, "wb") as f:
        f.write(response.content)
