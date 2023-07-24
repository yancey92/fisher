from flask import request, flash, current_app, render_template
from app.forms.verify import SearchForm

# from app.spider.yushu_book import YuShuBook
from flask_login import current_user
from app.models.book import Book
from . import web
from app.view_models.book import BookViewCollection, BookViewModel
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.trade import TradeInfo


@web.route("/book/search/<name>/<page>")
def search_test(name, page):
    pass


@web.route("/book/search")
def search():
    """
    /book/search?q=java&page=1
    q: 书名关键字 or isbn
        isbn: 国际标准书号, 分为 isbn13 和 isbn10
        isbn13 13个数字和一些'-'; isbn10 10个数字和一些'-'
    page: 第几页
    """
    # q=request.args["q"]
    # page=request.args["page"]

    viewmodel = BookViewCollection()
    bookCollection = {}
    # 使用 wtforms 做参数校验(验证层)
    form = SearchForm(request.args)
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        short_q = q.replace("-", "")

        if (len(short_q) == 13 or len(q) == 10) and short_q.isdigit():
            # 如果q是isbn
            bookCollection = Book.search_by_isbn(q)
        else:
            # 如果q是书名关键字
            bookCollection = Book.search_by_keyword(q, page)
        viewmodel.fill(bookCollection, q)
    else:
        flash("搜索的关键字不符合要求，请重新输入关键字")
        current_app.logger.info(form.errors)
        # books = form.errors
    # return json.dumps(books, indent=2, ensure_ascii=False, default=lambda obj: obj.__dict__)
    return render_template("search_result.html", books=viewmodel)


@web.route("/book/<isbn>/detail")
def book_detail(isbn):
    # 取出书的详情
    bookCollection = Book.search_by_isbn(isbn)
    viewmodel = BookViewModel(bookCollection.first_element)

    has_in_wishes = False
    has_in_gifts = False
    # 判断用户是否登录，是否有赠送书籍或索要书籍
    if current_user.is_authenticated:
        if Gift.query.filter_by(
            uid=current_user.id, isbn=isbn, launched=False, enable_status=1
        ).first():
            has_in_gifts = True
        if Wish.query.filter_by(
            uid=current_user.id, isbn=isbn, launched=False, enable_status=1
        ).first():
            has_in_wishes = True

    # 赠书人列表和索要人列表
    trade_gifts = Gift.query.filter_by(isbn=isbn, enable_status=1).all()
    trade_wishs = Wish.query.filter_by(isbn=isbn, enable_status=1).all()

    trade_wishs_model = TradeInfo(trade_wishs)
    trade_gifts_model = TradeInfo(trade_gifts)

    return render_template(
        "book_detail.html",
        book=viewmodel,
        wishes=trade_wishs_model,
        gifts=trade_gifts_model,
        has_in_wishes=has_in_wishes,
        has_in_gifts=has_in_gifts,
    )
