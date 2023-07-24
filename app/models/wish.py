from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc, func
from sqlalchemy.orm import relationship
from app.models.base import Base, db
from app.models.book import Book
# from app.spider.yushu_book import YuShuBook


# 想要的书籍清单
class Wish(Base):
    # __tablename__ = "wish"  # 指定数据库表名，如果不设置，默认是类名的小写
    id = Column(Integer, primary_key=True)
    launched = Column(Boolean, default=False)  # 是否送出去了
    user = relationship("User")  # 要关联的哪张表
    uid = Column(Integer, ForeignKey("user.id"), nullable=False)  # 书籍索要者
    isbn = Column(String(13), nullable=False)  # 要赠送的书籍编号

    @classmethod
    def get_wish_counts(cls, isbn_list):
        # 根据传入的一组isbn编号，到Wish表中计算出某个礼物的Wish心愿数量
        # select count(id),isbn from wish where launched = false and isbn in ('','') and enable_status =1 group by isbn
        count_list = (
            db.session.query(func.count(Wish.id), Wish.isbn)
            .filter(
                Wish.launched == False,
                Wish.isbn.in_(isbn_list),
                Wish.enable_status == 1,
            )
            .group_by(Wish.isbn)
            .all()
        )
        # 不要将tuple返回到外部，应该返回有意义的字典或者对象
        count_list = [{"count": w[0], "isbn": w[1]} for w in count_list]
        return count_list

    @property
    def book(self):
        bookCollection=Book.search_by_isbn(self.isbn)
        return bookCollection.first_element

    @classmethod
    def get_user_wishs(cls, uid):
        gifts = (
            Wish.query.filter_by(uid=uid, launched=False, enable_status=1)
            .order_by(desc(Wish.create_time))
            .all()
        )
        return gifts
