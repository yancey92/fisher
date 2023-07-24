from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc, func
from sqlalchemy.orm import relationship
from app.models.base import Base, db
from app.models.book import Book
# from app.spider.yushu_book import YuShuBook


# 书籍赠送模型
class Gift(Base):
    # __tablename__ = "gift"  # 指定数据库表名，如果不设置，默认是类名的小写
    id = Column(Integer, primary_key=True)
    launched = Column(Boolean, default=False)  # 是否送出去了
    user = relationship("User")  # Gift 要关联的哪张表
    uid = Column(Integer, ForeignKey("user.id"), nullable=False)  # 赠送者
    isbn = Column(String(13), nullable=False)  # 要赠送的书籍编号

    @classmethod
    def recent(cls):
        # select distinct * from gift group by isbn order by create_time limit 30
        recent_gifts = (
            Gift.query.filter_by(launched=False, enable_status=1)
            # .group_by(Gift.isbn)  # 加上这个会报错
            .order_by(desc(Gift.create_time))
            .limit(30)
            .distinct()
            .all()
        )
        return recent_gifts

    @property
    def book(self):
        bookCollection=Book.search_by_isbn(self.isbn)
        return bookCollection.first_element

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = (
            Gift.query.filter_by(uid=uid, launched=False, enable_status=1)
            .order_by(desc(Gift.create_time))
            .all()
        )
        return gifts

    @classmethod
    def get_gift_counts(cls, isbn_list):
        # 根据传入的一组isbn编号，到Wish表中计算出某个礼物的Wish心愿数量
        # select count(id),isbn from wish where launched = false and isbn in ('','') and enable_status =1 group by isbn
        count_list = (
            db.session.query(func.count(Gift.id), Gift.isbn)
            .filter(
                Gift.launched == False,
                Gift.isbn.in_(isbn_list),
                Gift.enable_status == 1,
            )
            .group_by(Gift.isbn)
            .all()
        )
        # 不要将tuple返回到外部，应该返回有意义的字典或者对象
        count_list = [{"count": w[0], "isbn": w[1]} for w in count_list]
        return count_list
