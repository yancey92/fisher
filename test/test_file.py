import os
import sys

if __package__ == "" or __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.libs.file import urldownload

file_dir = "./app/static/images/book/"
dir_list = os.listdir(file_dir)
headers = {
    "referer": "http://127.0.0.1:5000/",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.175",
}
for cur_file in dir_list:
    # 获取文件的绝对路径
    path = os.path.join(file_dir, cur_file)
    abspath=os.path.abspath(path)
    if os.path.isfile(abspath):
        print(abspath)
        file_name = str.split(path, "/")[-1]
        urldownload("https://img3.doubanio.com/lpic/" + file_name, abspath, headers)

