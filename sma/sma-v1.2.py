from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import pandas as pd
class Trader:
    short = {'BANANAS': [], 'PEARLS': []}
    long = {'BANANAS': [], 'PEARLS': []}

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        # Initialize the method output dict as an empty dict
        result = {}
        shortwindow = 7
        longwindow = 30

        # Iterate over all the keys (the available products) contained in the order depths
        for product in state.order_depths.keys():
            # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
            order_depth: OrderDepth = state.order_depths[product]
            # Initialize the list of Orders to be sent as an empty list
            orders: list[Order] = []
            if len(self.short[product]) < shortwindow and len(order_depth.sell_orders.keys()) != 0:
              self.short[product].append(min(order_depth.sell_orders.keys()))
            elif len(order_depth.sell_orders.keys()) != 0:
              current_buy = min(order_depth.sell_orders.keys())
              self.short[product].append(current_buy)
              del self.short[product][0]

            if len(self.long[product]) < longwindow and len(order_depth.sell_orders.keys()) != 0:
              self.long[product].append(min(order_depth.sell_orders.keys()))
            elif len(order_depth.sell_orders.keys()) != 0:
              current_buy = min(order_depth.sell_orders.keys())
              self.long[product].append(current_buy)
              del self.long[product][0]

            if len(self.short[product]) == shortwindow and len(self.long[product]) == longwindow:
              short_avg = sum(self.short[product]) / len(self.short[product])
              long_avg = sum(self.long[product]) / len(self.long[product])
              if len(order_depth.sell_orders) > 0:
                  best_ask = min(order_depth.sell_orders.keys())
                  best_ask_volume = order_depth.sell_orders[best_ask]
                  if short_avg > long_avg:
                      print("BUY", str(-best_ask_volume) + "x", best_ask)
                      orders.append(Order(product, best_ask, -best_ask_volume))
                      
              if len(order_depth.buy_orders) > 0:
                  best_bid = max(order_depth.buy_orders.keys())
                  best_bid_volume = order_depth.buy_orders[best_bid]
                  if short_avg < long_avg:
                      print("SELL", str(best_bid_volume) + "x", best_bid)
                      orders.append(Order(product, best_bid, -best_bid_volume))

              # Add all the above orders to the result dict
              result[product] = orders
        print(state.position)

        return result