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
    closes = {'PEARLS':[]}
    limits = {"COCONUTS": 600, "PINA_COLADAS": 300}
    building = ''
    dropping = ''
    shorting = ''
    bbacking = ''
    ratio = 8/15
    def run(self, state: TradingState) -> dict[Symbol, list[Order]]:

        result = {}

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
                orders.append(Order(product, best_ask, -best_ask_volume))
                
        if len(order_depth.buy_orders) != 0:
            best_bid = max(order_depth.buy_orders.keys())
            best_bid_volume = order_depth.buy_orders[best_bid]
            if best_bid > acceptable_price:
                orders.append(Order(product, best_bid, -best_bid_volume))

        # Add all the above orders to the result dict
        result[product] = orders

        # Iterate over all the keys (the available products) contained in the order depths
        # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
        order_depth: OrderDepth = state.order_depths['COCONUTS']
        midCoconut = (min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys())) / 2
        order_depth: OrderDepth = state.order_depths['PINA_COLADAS']
        midPinacolada = (min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys())) / 2
        cocounutamount = state.position.get('COCONUTS', 0) 
        pinacoladaamount = state.position.get('PINA_COLADAS', 0) 

        maxCoconut = 600 * midCoconut
        maxPinacolada = 300 * midPinacolada
        sharedamt = min(maxCoconut, maxPinacolada)


        spread = (midPinacolada / midCoconut) * self.ratio

        desiredDistance = 0.00072

        if spread > 1 + desiredDistance:
            self.shorting = 'PINA_COLADAS'
            self.building = 'COCONUTS' 
        elif spread < 1 - desiredDistance:
            self.shorting = 'COCONUTS'
            self.building = 'PINA_COLADAS'
        else:
            self.dropping = self.building
            self.bbacking = self.shorting
            self.building = ''
            self.shorting = ''
        


        if self.shorting == self.bbacking:
            self.bbacking = ''
        if self.building == self.dropping:
            self.dropping = ''

        if self.building != '':
            amt = state.position.get(self.building, 0) 
            order_depth: OrderDepth = state.order_depths[self.building]
            best_ask = min(order_depth.sell_orders.keys())
            vol = int(sharedamt // best_ask)

            if amt < vol:
                orders: list[Order] = []
                orders.append(Order(self.building, best_ask, vol-amt))
                result[self.building] = orders
            else:
                self.building = ''
        
        if self.bbacking != '':
            amt = state.position.get(self.bbacking, 0) 

            if amt < 0:
                order_depth: OrderDepth = state.order_depths[self.bbacking]
                best_ask = min(order_depth.sell_orders.keys())
                vol = sharedamt / best_ask
                orders: list[Order] = []
                orders.append(Order(self.bbacking, best_ask, -amt))
                result[self.bbacking] = orders
            else:
                self.bbacking = ''


        if self.shorting != '':
            amt = state.position.get(self.shorting, 0) 
            order_depth: OrderDepth = state.order_depths[self.shorting]
            best_ask = max(order_depth.buy_orders.keys())
            vol = int(sharedamt // best_ask)

            if amt > -vol:
                orders: list[Order] = []
                orders.append(Order(self.shorting, best_ask, -vol-amt))
                result[self.shorting] = orders
            else:
                self.shorting = ''

        if self.dropping != '':
            amt = state.position.get(self.dropping, 0) 

            if amt > 0:
                order_depth: OrderDepth = state.order_depths[self.dropping]
                best_ask = max(order_depth.buy_orders.keys())
                orders: list[Order] = []
                orders.append(Order(self.dropping, best_ask, -amt))
                result[self.dropping] = orders
            else:
                self.dropping = ''
        
        

        logger.flush(state, result)
        return result
