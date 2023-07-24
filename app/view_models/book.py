"""
    下行返回的数据模型
"""


class BookViewModel:

    def __init__(self, data):
        self.title = data['title']
        self.author = data['author']
        self.binding = data['binding']
        self.publisher = data['publisher']
        self.image = data['image']
        self.price = data['price']
        self.isbn = data['isbn']
        self.pubdate = data['pubdate']
        self.summary = data['summary']
        self.pages = data['pages']


class BookViewCollection:

    def __init__(self):
        self.keyword = ''
        self.total = 0
        self.books = []  # 存放 BookViewModel

    def fill(self, bookCollection, keyword):
        self.keyword = keyword
        self.total = bookCollection.total
        self.books = [BookViewModel(book) for book in bookCollection.books]
