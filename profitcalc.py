def init(self):
        self.holdings = 0
        self.last_trade = 0;

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        result = {}
        timestamp = self.last_trade;
        for trades in state.own_trades.values():
            for trade in trades:
                if trade.timestamp != self.last_trade:
                    timestamp = trade.timestamp
                    if trade.buyer == "SUBMISSION":
                        self.holdings += trade.price * trade.quantity
                    else:
                        self.holdings -= trade.price * trade.quantity
        self.last_trade = timestamp;
        profit = 0
        for product in state.position:
            profit += state.position[product] * (max(state.order_depths[product].buy_orders) + min(state.order_depths[product].sell_orders)) / 2
        profit -= self.holdings
        print("," + str(profit))