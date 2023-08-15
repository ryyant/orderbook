class Order:
    def __init__(self, is_buy, qty, price):
        self.is_buy = is_buy
        self.qty = qty
        self.price = price

    def __repr__(self):
        return "{} {}@${:.1f}".format(
            "buy" if self.is_buy else "sell", self.qty, self.price
        )

    def __gt__(self, other):
        return self.price > other.price


class OrderBook:
    def __init__(self):
        self._orders = []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        """
        formats and prints the order book as the test cases expect
        """
        buys, sells = self._split_into_buy_and_sell_orders()
        buys = sorted(buys)
        sells = sorted(sells)
        for o in [*buys, *sells]:
            print(o)

    def _split_into_buy_and_sell_orders(self):
        """
        splits orders into buy and sell orders.
        returns a pair of iterables:
        first iterable points to the first buy order.
        second points to the first sell order.
        """
        from itertools import tee, filterfalse

        is_buy = lambda o: o.is_buy
        buys, sells = tee(self._orders)
        return filter(is_buy, buys), filterfalse(is_buy, sells)

    def add(self, order):
        """
        checks the opposing side's available orders.
        for a buy order, look at existing sell orders, and vice versa.
        if a trade is possible, update the order book accordingly.
        otherwise, insert the order into the book.
        """
        exists = self.check_exist(order)
        if exists:
            return

        other = self._find_trade(order)
        if other:
            self._orders.remove(other)
            qty_left = order.qty - other.qty
            # order qty greater
            if qty_left > 0:
                order_book.add(Order(order.is_buy, qty_left, order.price))
            # other qty greater
            if qty_left < 0:
                order_book.add(Order(other.is_buy, -qty_left, other.price))
        else:
            self._orders.append(order)
            self._orders.sort(key=lambda x: x.price, reverse=True) # Descending

    def check_exist(self, order):
        buys, sells = self._split_into_buy_and_sell_orders()
        sells = sorted(sells)

        if order.is_buy:
            for buy in buys:
                if order.price == buy.price:
                    buy.qty += order.qty
                    return True

        if not order.is_buy:
            for sell in sells:
                if order.price == sell.price:
                    sell.qty += order.qty
                    return True

        return False

        # i = 0
        # while i < len(self._orders):
        #     # check if already exists then overwrite
        #     if (order.is_buy == self._orders[i].is_buy) and (order.price == self._orders[i].price):
        #         new_qty = order.qty + self._orders[i].qty
        #         self._orders[i] = Order(order.is_buy, new_qty, order.price)
        #         return True
        #     i += 1
        # return False

    def _find_trade(self, order):
        """
        returns an order for the best "match" for a give order.
        for buy orders, this would be the lowest sell price.
        for sell orders,the highest buy price.
        if no orders meet the criteria, return None.
        """
        buys, sells = self._split_into_buy_and_sell_orders()
        sells = sorted(sells) # sells need to be ascending

        if order.is_buy:
            for sell in sells:
                if order.price >= sell.price:
                    return sell

        if not order.is_buy:
            for buy in buys:
                if order.price <= buy.price:
                    return buy

        return None

        # ret = None
        # i = 0
        # while i < len(self._orders):
        #     # different sides
        #     if order.is_buy != self._orders[i].is_buy:
        #         if (order.is_buy and (order.price >= self._orders[i].price)) or (not order.is_buy and (order.price <= self._orders[i].price)):
        #             ret = self._orders[i]
        #             break
        #     i += 1
        # return ret


def parse(order_book=OrderBook()):
    while True:
        line = input().strip().split()
        if line[0] == "end":
            break

        is_buy = line[0] == "buy"
        qty, price = line[1:]
        order_book.add(Order(is_buy, int(qty), float(price)))


with OrderBook() as order_book:
    parse(order_book)
    order_book.add(Order(True, 10, 11.0))


"""
Inputs will be parsed before final BUY 10@$11
Test Case:

Input:
buy 5 10.0
buy 2 12.0
sell 3 13.0
buy 1 14.0
sell 4 9.0
end

Output:
buy 3@$10.0
buy 10@$11.0
sell 2@$13.0
"""
