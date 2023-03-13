from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import pandas as pd
class Trader:
    closes = {'BANANAS': [], 'PEARLS': []}

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        # Initialize the method output dict as an empty dict
        result = {}

        # Iterate over all the keys (the available products) contained in the order depths
        for product in state.order_depths.keys():
            product = 'PEARLS'
            # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
            order_depth: OrderDepth = state.order_depths[product]
            if len(order_depth.sell_orders.keys()) != 0:
              current_buy = (min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys())) / 2
              self.closes[product].append(current_buy)

            acceptable_price = sum(self.closes[product]) / len(self.closes[product])
            orders: list[Order] = []
            if len(order_depth.sell_orders) > 0:
                best_ask = min(order_depth.sell_orders.keys())
                best_ask_volume = order_depth.sell_orders[best_ask]
                if best_ask < acceptable_price:
                    print("BUY", str(-best_ask_volume) + "x", best_ask)
                    orders.append(Order(product, best_ask, -best_ask_volume))
                    
            if len(order_depth.buy_orders) != 0:
                best_bid = max(order_depth.buy_orders.keys())
                best_bid_volume = order_depth.buy_orders[best_bid]
                if best_bid > acceptable_price:
                    print("SELL", str(best_bid_volume) + "x", best_bid)
                    orders.append(Order(product, best_bid, -best_bid_volume))

            # Add all the above orders to the result dict
            result[product] = orders

        return result