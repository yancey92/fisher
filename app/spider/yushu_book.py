"""
    从 t.talelin.com 抓取数据, 分别有两种抓取方式: isbn_url, keyword_url
    对不同方式抓取到的数据统一返回
    
    通过这个方法, 将查询到的部分数据转存到 mysql;
    之后将直接使用 mysql 中的数据, 而不再使用这个模块来获取图书信息
   
    
    #-------------- 通过 isbn 获取单个数据 --------------#
    # request:
        curl --location --request GET 'http://t.talelin.com/v2/book/isbn/9787111213826'
    # response:
        {
            "author": [
                "[美]BruceEckel"
            ],
            "binding": "平装",
            "category": "编程",
            "id": 6,
            "image": "https://img3.doubanio.com/lpic/s27243455.jpg",
            "images": {
                "large": "https://img3.doubanio.com/lpic/s27243455.jpg"
            },
            "isbn": "9787111213826",
            "pages": "880",
            "price": "108.00元",
            "pubdate": "2007-6",
            "publisher": "机械工业出版社",
            "subtitle": "",
            "summary": "本书赢得了全球程序员的广泛赞誉，即使是最晦涩的概念，在Bruce Eckel的文字亲和力和小而直接的编程示例面前也会化解于无形。从Java的基础语法到最高级特性（深入的面向对象概念、多线程、自动项目构建、单元测试和调试等），本书都能逐步指导你轻松掌握。\\n从本书获得的各项大奖以及来自世界各地的读者评论中，不难看出这是一本经典之作。本书的作者拥有多年教学经验，对C、C++以及Java语言都有独到、深入的见解，以通俗易懂及小而直接的示例解释了一个个晦涩抽象的概念。本书共22章，包括操作符、控制执行流程、访问权限控制、复用类、多态、接口、通过异常处理错误、字符串、泛型、数组、容器深入研究、Java I/O系统、枚举类型、并发以及图形化用户界面等内容。这些丰富的内容，包含了Java语言基础语法以及高级特性，适合各个层次的Java程序员阅读，同时也是高等院校讲授面向对象程序设计语言以及Java语言的绝佳教材和参考书。\\n第4版特点：\\n适合初学者与专业人员的经典的面向对象叙述方式，为更新的Java SE5/6增加了新的示例和章节。\\n 测验框架显示程序输出。",
            "title": "Java编程思想 （第4版）",
            "translator": [
                "陈昊鹏"
            ]
        }


    #-------------- 通过关键字获取多个数据 --------------#
    # request:
        curl --location 'http://t.talelin.com/v2/book/search?q=python&count=5&start=0'
    # response:
        {
            "books": [
                {
                    ......
                },
                {
                    "author": [
                        "P.J.Deitel",
                        "J.P.Liperi",
                        "B.A.Wiedermann",
                        "H.M.Deitel"
                    ],
                    "binding": "平装(无盘)",
                    "category": "编程",
                    "id": 105,
                    "image": "https://img3.doubanio.com/lpic/s1326052.jpg",
                    "images": {
                        "large": "https://img3.doubanio.com/lpic/s1326052.jpg"
                    },
                    "isbn": "9787302066422",
                    "pages": "596",
                    "price": "88.00元",
                    "pubdate": "2003-6",
                    "publisher": "清华大学出版社",
                    "subtitle": "",
                    "summary": "本书由全球著名的程序语言培训专家精心编著，解释了如何将Python用作常规用途，编写多层、客户机/服务器结构、数据库密集型、基于Internet和Web的应用程序。书中采用作者独创的“活代码”教学方式，层层揭示了Python这一程序设计语言的强大功能，并通过穿插在全书各处的屏幕输出和编程技巧与提示，帮助读者搭建良好的知识结构、养成良好的编程习惯、避免常见的编程错误以及写出高效、可靠的应用程序。",
                    "title": "Python 编程金典",
                    "translator": []
                },
                {
                    ......
                },
                {
                    ......
                },
                {
                    ......
                }
            ],
            "count": 5,
            "start": 0,
            "total": 58
        }
"""

from flask import current_app
from app.libs.file import urldownload
from app.models import auto_commit
from app.models.book import Book
from app.libs.httper import HTTP
import json


class YuShuBook:
    isbn_url = "http://t.talelin.com/v2/book/isbn/{}"  # 通过isbn查询单个记录
    keyword_url = (
        "http://t.talelin.com/v2/book/search?q={}&count={}&start={}"  # 通过关键字模糊查询多条
    )

    def __int__(self):
        self.total = 0
        self.books = []

    # 只有一个数据返回时
    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books = [data]

    # 有多条数据被找到
    def __fill_multiple(self, data):
        self.total = data["total"]
        self.books = data["books"]

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        result = HTTP.get(url)
        self.__fill_single(result)
        # self.save_book_todb(self.books) # 如果要将数据保存到db, 则打开该注释

    def search_by_keyword(self, keyword, page=1):
        url = self.keyword_url.format(
            keyword, current_app.config["PER_PAGE"], self.calculate_start(page)
        )
        result = HTTP.get(url)
        self.__fill_multiple(result)
        # self.save_book_todb(self.books) # 如果要将数据保存到db, 则打开该注释

    # @property 是个装饰器，用于定义一个属性的 getter 方法。它允许你在访问属性时执行一些逻辑，而不仅仅是简单地返回属性的值。
    @property
    def first_element(self):
        return self.books[0] if self.total > 0 else None

    @classmethod
    def calculate_start(cls, page):
        return (page - 1) * current_app.config["PER_PAGE"]

    @classmethod
    def save_book_todb(cls, books_list):
        """
        传入http请求获得的book列表, 然后将其格式化保存到数据库
        图书的图片则保存到 static/images/book/ 目录下面
        """
        with auto_commit() as db:
            for element in books_list:
                # 如果数据库中存在, 则跳过
                if Book.search_by_isbn(element.get("isbn")):
                    continue

                image_name = str.split(element.get("image"), "/")[-1]
                book = Book()
                book.author = json.dumps(element.get("author"), ensure_ascii=False)
                book.title = element.get("title")
                book.binding = element.get("binding")
                book.image = f'http://{current_app.config["HOST"]}:{current_app.config["PORT"]}{current_app.static_url_path}/images/book/{image_name}'
                book.isbn = element.get("isbn")
                book.pages = int(element.get("pages"))
                book.price = element.get("price")
                book.pubdate = element.get("pubdate")
                book.publisher = element.get("publisher")
                book.summary = element.get("summary")
                db.session.add(book)

                # 保存图片
                file_path = current_app.static_folder + "/images/book/" + image_name
                urldownload(
                    element.get("image"),
                    file_path,
                    headers={
                        "referer": f'http://{current_app.config["HOST"]}:{current_app.config["PORT"]}',
                        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.175",
                    },
                )
