from app.view_models.book import BookViewModel


class TradeInfo:
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)

    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(element) for element in goods]

    def __map_to_trade(self, element):
        if element.format_create_time:
            time = element.format_create_time.strftime("%Y-%m-%d")
        else:
            time = "未知"
        return dict(user_name=element.user.nickname, time=time, id=element.id)


class MyTrade:
    def __init__(self, trades_of_mine, trades_count_list):
        self.trades = []
        self.__trades_of_mine = trades_of_mine
        self.__trades_count_list = trades_count_list

        self.trades = self.__parse()

    def __parse(self):
        temp_trades = []
        for trade in self.__trades_of_mine:
            my_trade = self.__matching(trade)
            temp_trades.append(my_trade)
        return temp_trades

    def __matching(self, trade):
        count = 0
        for trade_count in self.__trades_count_list:
            if trade.isbn == trade_count["isbn"]:
                count = trade_count["count"]
        r = {"wishes_count": count, "book": BookViewModel(trade.book), "id": trade.id}
        return r
