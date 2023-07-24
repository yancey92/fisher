"""
    这是一个完整的单元测试示例：
    
    "sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))" , 
    这句话的意思是获取到当前整个项目的根路径, 将其添加到 PYTHONPATH 中,
    如果不加这句话, 将会报错: ModuleNotFoundError: No module named 'app'
    
    其实, python 启动一个程序时，默认将启动文件所在的目录作为项目的根目录, 
    所以, 程序的入口文件的位置尽量要在整个项目的根路径下面, 
    如果不在项目的根路径下, 还想要直接运行该 py 文件, 则需要 sys.path.append() 将项目的根路径添加到 PYTHONPATH
"""
import os
import sys

if __package__ == "" or __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from app.models.user import User
from app.models.book import Book
import unittest, json



class TestDB(unittest.TestCase):
    """
    定义一个测试类，继承自 unittest.TestCase
    测试命令："pytest test_db.py -s"   或   "python3 test_db.py"
    """

    def setUp(self):
        """该方法会首先执行，方法名为固定写法"""
        self.app = app
        # 激活测试标志
        app.config["TESTING"] = True
        # 在这里,使用flask提供的测试客户端进行测试
        self.client = app.test_client()

    def tearDown(self):
        """该方法会在测试代码执行完后执行，方法名为固定写法"""
        pass


    # 我的测试逻辑: 查询 user
    def test_select_user(self):
        with self.app.app_context():
            user = User.query.filter_by(nickname="yangxin", enable_status=1).first()
            print("\nUser :", user.to_dict())

            assert user

    # 我的测试逻辑: 查询 book
    def test_search_by_keyword(self):
        with self.app.app_context():
            bookCollection = Book.search_by_keyword("java", page=1)
            print(
                "\nBooks :",
                json.dumps(
                    bookCollection, ensure_ascii=False, default=lambda obj: obj.__dict__
                ),
            )

            assert bookCollection

        

if __name__ == "__main__":
    # unittest.main(TestDB) # run tests from module.TestClass
    unittest.main()
