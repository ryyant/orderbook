from heapq import heappop, heappush


class Order:
    def __init__(self, type, price, qty):
        self.type: str = type
        self.price: float = price
        self.qty: int = qty

    # comparator
    def __lt__(self, other):
        return self.price < other.price

    def printOrder(self):
        if self.type == "buy":
            print(f"Price:{-self.price} / Qty:{self.qty}")
        if self.type == "sell":
            print(f"Price:{self.price} / Qty:{self.qty}")


class OrderBook:
    def __init__(self):
        self.buy = []  # max-heap
        self.sell = []  # min-heap
        self.totalVolume = 0
        # since python heapq implementation is min-heap,
        # need to store as neg values for buy to get max-heap

    def addOrder(self, order):
        orderType = order[0]
        if orderType == "buy":
            newOrder = Order(order[0], -float(order[1]), int(order[2]))
            heappush(self.buy, newOrder)
        elif orderType == "sell":
            newOrder = Order(order[0], float(order[1]), int(order[2]))
            heappush(self.sell, newOrder)
        else:
            print("invalid order")
        self.matchOrders()

    # match orders that can be fufilled
    def matchOrders(self):
        while self.buy and self.sell and -self.buy[0].price >= self.sell[0].price:
            # remove smaller qty from both
            tradeQty = min(self.buy[0].qty, self.sell[0].qty)
            self.buy[0].qty -= tradeQty
            self.sell[0].qty -= tradeQty
            if self.buy[0].qty == 0:
                heappop(self.buy)
            if self.sell[0].qty == 0:
                heappop(self.sell)
            # volume cal
            self.addVolume(tradeQty)

    # assuming vol benefit
    def getTotalVolume(self):
        print(self.totalVolume)

    def addVolume(self, qty):
        self.totalVolume += qty

    def removeOrder(self, order):
        pass

    def printOrders(self):
        print("\nBUY ORDERS:")
        if not self.buy:
            print("No buy orders.")
        else:
            priceSortedBuys = sorted(self.buy)
            for b in priceSortedBuys:
                b.printOrder()
        print("\nSELL ORDERS:")
        if not self.sell:
            print("No sell orders.")
        else:
            priceSortedSell = sorted(self.sell)
            for s in priceSortedSell:
                s.printOrder()

    def numOfbuy(self):
        return len(self.buy)

    def numOfsell(self):
        return len(self.sell)


orderBook = OrderBook()
while True:
    next = input()
    if next == "print":
        orderBook.printOrders()
        continue
    if next == "vol":
        orderBook.getTotalVolume()
        continue
    if next == "q":
        break
    order = next.split(" ")
    orderBook.addOrder(order)

# TC
# buy 5.5 2
# buy 4 2
# buy 2 2
# sell 6 3
# sell 7 2
# sell 5 3
# buy 6.2 2

# expect:
# BUY ORDERS:
# Price:4.0 / Qty:2
# Price:2.0 / Qty:2

# SELL ORDERS:
# Price:6.0 / Qty:2
# Price:7.0 / Qty:2

# volume log:
# buy 2
# sell 1
# sell 1
# total: 4
