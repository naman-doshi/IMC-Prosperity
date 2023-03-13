from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import pandas as pd


class Trader:
    closes = {'BANANAS': [], 'PEARLS': []}
    opens = {'BANANAS': 0, 'PEARLS': 0}

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        # Initialize the method output dict as an empty dict
        result = {}
        window = 30
        avg = 0

        # Iterate over all the keys (the available products) contained in the order depths
        macds = []
        for product in state.order_depths.keys():
           orders: list[Order] = []
           order_depth: OrderDepth = state.order_depths[product]
           if len(self.closes[product]) < window and len(order_depth.sell_orders.keys()) != 0:
              self.closes[product].append(min(order_depth.sell_orders.keys()))
           elif len(order_depth.sell_orders.keys()) != 0:
              current_buy = min(order_depth.sell_orders.keys())
              current_sell = max(order_depth.buy_orders.keys())
              self.closes[product].append(current_buy)
              del self.closes[product][0]
              avg = sum(self.closes[product]) / window
              if len(order_depth.sell_orders) > 0 and avg > current_buy:
                  best_ask = min(order_depth.sell_orders.keys())
                  best_ask_volume = order_depth.sell_orders[best_ask]
                  print("BUY", str(-best_ask_volume) + "x", best_ask)
                  orders.append(Order(product, best_ask, -best_ask_volume))                       
              elif len(order_depth.buy_orders) > 0 and avg < current_sell:
                  best_bid = max(order_depth.buy_orders.keys())
                  best_bid_volume = order_depth.buy_orders[best_bid]
                  print("SELL", str(best_bid_volume) + "x", best_bid)
                  orders.append(Order(product, best_bid, -best_bid_volume))
           result[product] = orders
           print(state.position)

             

        return result