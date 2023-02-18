from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import pandas as pd
class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        # Initialize the method output dict as an empty dict
        result = {}

        # Iterate over all the keys (the available products) contained in the order depths
        for product in state.order_depths.keys():
            if product == 'BANANAS':
                order_depthB: OrderDepth = state.order_depths[product]
                # Initialize the list of Orders to be sent as an empty list
                best_askB = min(order_depthB.sell_orders.keys())
                best_bidB = max(order_depthB.buy_orders.keys())
                # best_ask_volumeB = order_depthB.sell_orders[best_askB]
                # best_bid_volumeB = order_depthB.buy_orders[best_bidB]
                # spreadB = ((best_askB - best_bidB)/best_askB)*100*(best_askB/2)
            if product == 'PEARLS':
                order_depthP: OrderDepth = state.order_depths[product]
                # Initialize the list of Orders to be sent as an empty list
                best_askP = min(order_depthP.sell_orders.keys())
                best_bidP = max(order_depthP.buy_orders.keys())
                # spreadP = ((best_askP - best_bidP)/best_askP)*100*(best_askP/2)
                # best_ask_volumeP = order_depthP.sell_orders[best_askP]
                # best_bid_volumeP = order_depthP.buy_orders[best_bidP]
        
        orders: list[Order] = []
        

        threshold = 5
        if 'BANANAS' not in state.position or 'PEARLS' not in state.position:
          if 'BANANAS' not in state.position:
            orders: list[Order] = []
            orders.append(Order("BANANAS", best_bidB, 20))
            result["BANANAS"] = orders
          if 'PEARLS' not in state.position:
            orders: list[Order] = []
            orders.append(Order("PEARLS", best_bidP, 20))
            result["PEARLS"] = orders
        else:
          if state.position['BANANAS'] > threshold:
            orders: list[Order] = []
            orders.append(Order("BANANAS", best_askB, -(int(state.position['BANANAS'])-threshold)))
            result["BANANAS"] = orders
          else:
            orders: list[Order] = []
            orders.append(Order("BANANAS", best_bidB, 20-int(state.position['BANANAS'])))
            result["BANANAS"] = orders
          if state.position['PEARLS'] > threshold:
            orders: list[Order] = []
            orders.append(Order("PEARLS", best_askP, -(int(state.position['PEARLS'])-threshold)))
            result["PEARLS"] = orders
          else:
            orders: list[Order] = []
            orders.append(Order("PEARLS", best_bidP, 20-int(state.position['PEARLS'])))
            result["PEARLS"] = orders
        print(result)
        print(state.position)

        return result