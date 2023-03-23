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
    increasingB = True
    increasingP = True
    lastB = 0
    lastP = 0
    def run(self, state: TradingState) -> dict[Symbol, list[Order]]:

        result = {}

        # Iterate over all the keys (the available products) contained in the order depths
        for product in state.order_depths.keys():
            if product == 'BANANAS':
                order_depthB: OrderDepth = state.order_depths[product]
                best_askB = min(order_depthB.sell_orders.keys())
                best_bidB = max(order_depthB.buy_orders.keys())
            if product == 'PEARLS':
                order_depthP: OrderDepth = state.order_depths[product]
                best_askP = min(order_depthP.sell_orders.keys())
                best_bidP = max(order_depthP.buy_orders.keys())
        
        orders: list[Order] = []
        

        threshold = 12
        if 'BANANAS' not in state.position or 'PEARLS' not in state.position:
          if 'BANANAS' not in state.position:
            orders: list[Order] = []
            orders.append(Order("BANANAS", best_bidB, 20))
            self.lastB = best_bidB
            result["BANANAS"] = orders
          if 'PEARLS' not in state.position:
            orders: list[Order] = []
            orders.append(Order("PEARLS", best_bidP, 20))
            self.lastB = best_bidP
            result["PEARLS"] = orders
        else:
          if self.increasingB == False:
            orders: list[Order] = []
            if best_askB >= self.lastB:
              orders.append(Order("BANANAS", best_askB, -(int(state.position['BANANAS'])-threshold)))
              result["BANANAS"] = orders
          elif int(state.position['BANANAS']) == 20:
             self.increasingB = False
             orders: list[Order] = []
             if best_askB >= self.lastB:
                orders.append(Order("BANANAS", best_askB, -(int(state.position['BANANAS'])-threshold)))
                result["BANANAS"] = orders
          if self.increasingB == True or int(state.position['BANANAS']) <= threshold:
            orders: list[Order] = []
            orders.append(Order("BANANAS", best_bidB, 20-int(state.position['BANANAS'])))
            self.lastB = max(self.lastB, best_bidB)
            result["BANANAS"] = orders
            self.increasingB = True
          if self.increasingP == False:
            orders: list[Order] = []
            if best_askP >= self.lastP:
              orders.append(Order("PEARLS", best_askP, -(int(state.position['PEARLS'])-threshold)))
              result["PEARLS"] = orders
          elif int(state.position['PEARLS']) == 20:
             self.increasingP = False
             orders: list[Order] = []
             if best_askP >= self.lastP:
                orders.append(Order("PEARLS", best_askP, -(int(state.position['PEARLS'])-threshold)))
                result["PEARLS"] = orders
          if self.increasingP == True or int(state.position['PEARLS']) <= threshold:
            orders: list[Order] = []
            orders.append(Order("PEARLS", best_bidP, 20-int(state.position['PEARLS'])))
            self.lastP = max(self.lastP, best_bidP)
            result["PEARLS"] = orders
            self.increasingP = True
        logger.print(result)
        logger.print(state.position)
        logger.flush(state, result)
        return result
