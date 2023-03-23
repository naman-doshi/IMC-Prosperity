from typing import Dict, List
import pandas as pd

import json
from datamodel import *
from typing import Any

class Logger:
    def __init__(self) -> None:
        self.logs = ""

    def print(self, *objects: Any, sep: str = " ", end: str = "\n") -> None:
        self.logs += sep.join(map(str, objects)) + end

    def flush(self, state: TradingState, orders: dict[Symbol, list[Order]]) -> None:
        print(json.dumps({
            "state": state,
            "orders": orders,
            "logs": self.logs,
        }, cls=ProsperityEncoder, separators=(",", ":"), sort_keys=True))

        self.logs = ""

logger = Logger()

class Trader:
    closes = {'BANANAS': [], 'PEARLS': []}
    prevlong = 0
    prevshort = 0
    def run(self, state: TradingState) -> dict[Symbol, list[Order]]:

        # TODO: Add logic
        
         # Initialize the method output dict as an empty dict
        result = {}

        # Iterate over all the keys (the available products) contained in the order depths
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
                logger.print("BUY", str(-best_ask_volume) + "x", best_ask)
                orders.append(Order(product, best_ask, -best_ask_volume))
                
        if len(order_depth.buy_orders) != 0:
            best_bid = max(order_depth.buy_orders.keys())
            best_bid_volume = order_depth.buy_orders[best_bid]
            if best_bid > acceptable_price:
                logger.print("SELL", str(best_bid_volume) + "x", best_bid)
                orders.append(Order(product, best_bid, -best_bid_volume))

        # Add all the above orders to the result dict
        result[product] = orders




        # product = "BANANAS"
        # order_depth: OrderDepth = state.order_depths[product]
        # short = 10
        # long = 30
        # shortwindow = []
        # longwindow = []
        # orders: list[Order] = []
        # if len(self.closes[product]) < long and len(order_depth.sell_orders.keys()) != 0:
        #   self.closes[product].append(min(order_depth.sell_orders.keys()))
        # elif len(order_depth.sell_orders.keys()) != 0:
        #   current_buy = min(order_depth.sell_orders.keys())
        #   self.closes[product].append(current_buy)
        #   shortwindow = self.closes[product][-short:]
        #   longwindow = self.closes[product][-long:]
        

        # shortavg = sum(shortwindow) / short
        # longavg = sum(longwindow) / long

        # if shortavg > longavg and self.prevshort < self.prevlong:
        #     if len(order_depth.sell_orders) > 0:
        #         best_ask = min(order_depth.sell_orders.keys())
        #         best_ask_volume  = order_depth.sell_orders[best_ask]
        #         if best_ask < acceptable_price:
        #             logger.print("BUY", str(-best_ask_volume) + "x", best_ask)
        #             orders.append(Order(product, best_ask, -best_ask_volume))
        # if shortavg < longavg and self.prevshort > self.prevlong:       
        #     if len(order_depth.buy_orders) != 0:
        #         best_bid = max(order_depth.buy_orders.keys())
        #         best_bid_volume = order_depth.buy_orders[best_bid]
        #         if best_bid > acceptable_price:
        #             logger.print("SELL", str(best_bid_volume) + "x", best_bid)
        #             orders.append(Order(product, best_bid, -best_bid_volume))

        # self.prevlong = longavg
        # self.prevshort = shortavg
        # result[product] = orders


        

        logger.flush(state, result)
        return result
