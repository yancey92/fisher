from sqlalchemy import Column, Integer, String
from app.models.base import Base
from app import app


class Book(Base):
    """
    继承 Base class, 而 Base class 又继承了 db.Model, 所以 Book 类就间接继承了 db.Model
    也可以使用多继承: class Book(Base, db.Model)
    """

    __tablename__ = "book"  # 指定数据库表名，如果不设置，默认是类名的小写

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    title = Column("title", String(50), nullable=False)  # 书名
    # 作者, e.g: ["Noah Gift", "Jeremy Jones"]
    author = Column("author", String(100), default="未名")
    binding = Column("binding", String(20))  # 装订 (精装、平装)
    publisher = Column(String(50))  # 出版社
    price = Column(String(20))  # 价格
    pages = Column(String(10))  # 页数
    pubdate = Column(String(20))  # 出版日期
    isbn = Column(String(15), nullable=False, unique=True)  # 图书的isbn
    summary = Column(String(2000))  # 书籍的简介
    image = Column(String(150))  # 图书的图片

    @classmethod
    def search_by_isbn(cls, isbn):
        book = cls.query.filter_by(isbn=isbn, enable_status=1).first()
        return BookCollection(1, [book.to_dict()])

    @classmethod
    def search_by_keyword(cls, keyword, page=1):
        # 分页: https://blog.csdn.net/qq_41843228/article/details/104890820
        per_page = app.config["PER_PAGE"]
        pagination = cls.query.filter(
            cls.title.like("%" + keyword + "%"), cls.enable_status == 1
        ).paginate(page=page, per_page=per_page)

        book_list = [book.to_dict() for book in pagination.items]
        return BookCollection(pagination.total, book_list)


class BookCollection:
    def __init__(self, total, books):
        self.total = total
        self.books = books

    @property
    def first_element(self):
        return self.books[0] if self.total > 0 else None
