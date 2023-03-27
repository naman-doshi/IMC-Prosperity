from typing import Dict, List
import pandas as pd
import math

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
    closes = {'PEARLS':[]}
    limits = {"COCONUTS": 600, "PINA_COLADAS": 300, "BERRIES": 250, "DIVING_GEAR": 50, 'BAGUETTE':150, 'DIP':300, 'UKULELE':70, 'PICNIC_BASKET':70}
    ticker = 0
    building = []
    dropping = []
    shorting = []
    bbacking = []
    prevSighting = 0
    ratio = 8/15
    buildingBasket = ''
    droppingBasket = ''
    shortingBasket = ''
    bbackingBasket = ''
    def run(self, state: TradingState) -> dict[Symbol, list[Order]]:
        result = {}
        order_depth: OrderDepth = state.order_depths['BAGUETTE']
        s1 = (min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys())) / 2
        order_depth: OrderDepth = state.order_depths['DIP']
        s2 = (min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys())) / 2
        order_depth: OrderDepth = state.order_depths['UKULELE']
        s3 = (min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys())) / 2
        order_depth: OrderDepth = state.order_depths['PICNIC_BASKET']
        s4 = (min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys())) / 2

        compositePrice = 2 * s1 + 4 * s2 + s3
        basketSpread = compositePrice / s4
        plusMinus = 0.00185
        logger.print(basketSpread)
        if compositePrice < s4:
            vols = {"BAGUETTE": 140, "DIP": 280, "UKULELE": 70, "PICNIC_BASKET": math.floor((compositePrice/s4)*70)}
        else:
            vols = {"BAGUETTE": math.floor((s4/compositePrice)*140), "DIP": math.floor((s4/compositePrice)*280), "UKULELE": math.floor((s4/compositePrice)*70), "PICNIC_BASKET": 70}

        if basketSpread > 0.9944 + plusMinus:
            self.shortingBasket = 'COMPOSITE'
            self.buildingBasket = 'PICNIC_BASKET' 
        elif basketSpread < 0.9944 - plusMinus:
            self.shortingBasket = 'PICNIC_BASKET'
            self.buildingBasket = 'COMPOSITE'
        else:
            self.droppingBasket = self.buildingBasket
            self.bbackingBasket = self.shortingBasket
            self.buildingBasket = ''
            self.shortingBasket = ''
        
        if self.shortingBasket == self.bbackingBasket:
            self.bbackingBasket = ''
        if self.buildingBasket == self.droppingBasket:
            self.droppingBasket = ''


        if self.buildingBasket != '':
            if self.buildingBasket == "PICNIC_BASKET":
                amt = state.position.get(self.buildingBasket, 0) 
                order_depth: OrderDepth = state.order_depths[self.buildingBasket]
                best_ask = min(order_depth.sell_orders.keys())
                vol = vols[self.buildingBasket]

                if amt < vol:
                    orders: list[Order] = []
                    orders.append(Order(self.buildingBasket, best_ask, vol-amt))
                    result[self.buildingBasket] = orders
                else:
                    self.buildingBasket = ''
            else:
                totalFulfilled = 0
                for i in ['BAGUETTE', 'DIP', 'UKULELE']:
                    amt = state.position.get(i, 0) 
                    order_depth: OrderDepth = state.order_depths[i]
                    best_ask = min(order_depth.sell_orders.keys())
                    vol = vols[i]

                    if amt < vol:
                        orders: list[Order] = []
                        orders.append(Order(i, best_ask, vol-amt))
                        result[i] = orders
                    else:
                        totalFulfilled += 1
                if totalFulfilled == 3:
                    self.buildingBasket = ''
                
        
        if self.bbackingBasket != '':
            if self.bbackingBasket == "PICNIC_BASKET":
                amt = state.position.get(self.bbackingBasket, 0) 

                if amt < 0:
                    order_depth: OrderDepth = state.order_depths[self.bbackingBasket]
                    best_ask = min(order_depth.sell_orders.keys())
                    orders: list[Order] = []
                    orders.append(Order(self.bbackingBasket, best_ask, -amt))
                    result[self.bbackingBasket] = orders
                else:
                    self.bbackingBasket = ''
            else:
                totalFulfilled = 0
                for i in ['BAGUETTE', 'DIP', 'UKULELE']:
                    amt = state.position.get(i, 0) 
                    order_depth: OrderDepth = state.order_depths[i]
                    best_ask = min(order_depth.sell_orders.keys())

                    if amt < 0:
                        orders: list[Order] = []
                        orders.append(Order(i, best_ask, -amt))
                        result[i] = orders
                    else:
                        totalFulfilled += 1
                if totalFulfilled == 3:
                    self.bbackingBasket = ''


        if self.shortingBasket != '':
            if self.shortingBasket == "PICNIC_BASKET":
                amt = state.position.get(self.shortingBasket, 0) 
                order_depth: OrderDepth = state.order_depths[self.shortingBasket]
                best_ask = max(order_depth.buy_orders.keys())
                vol = vols[self.shortingBasket]

                if amt > -vol:
                    orders: list[Order] = []
                    orders.append(Order(self.shortingBasket, best_ask, -vol-amt))
                    result[self.shortingBasket] = orders
                else:
                    self.shortingBasket = ''
            else:
                totalFulfilled = 0
                for i in ['BAGUETTE', 'DIP', 'UKULELE']:
                    amt = state.position.get(i, 0) 
                    order_depth: OrderDepth = state.order_depths[i]
                    best_ask = max(order_depth.buy_orders.keys())
                    vol = vols[i]

                    if amt > -vol:
                        orders: list[Order] = []
                        orders.append(Order(i, best_ask, -vol-amt))
                        result[i] = orders
                    else:
                        totalFulfilled += 1
                if totalFulfilled == 3:
                    self.shortingBasket = ''

        if self.droppingBasket != '':
            if self.droppingBasket == "PICNIC_BASKET":
                amt = state.position.get(self.droppingBasket, 0) 
                if amt > 0:
                    order_depth: OrderDepth = state.order_depths[self.droppingBasket]
                    best_ask = max(order_depth.buy_orders.keys())
                    orders: list[Order] = []
                    orders.append(Order(self.droppingBasket, best_ask, -amt))
                    result[self.droppingBasket] = orders
                else:
                    self.droppingBasket = ''
            else:
                totalFulfilled = 0
                for i in ['BAGUETTE', 'DIP', 'UKULELE']:
                    amt = state.position.get(i, 0) 
                    order_depth: OrderDepth = state.order_depths[i]
                    best_ask = max(order_depth.buy_orders.keys())

                    if amt > 0:
                        orders: list[Order] = []
                        orders.append(Order(i, best_ask, -amt))
                        result[i] = orders
                    else:
                        totalFulfilled += 1
                if totalFulfilled == 3:
                    self.droppingBasket = ''

        logger.flush(state, result)
        return result
