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
    limits = {"COCONUTS": 600, "PINA_COLADAS": 300, "BERRIES": 250, "DIVING_GEAR": 50}
    ticker = 0
    building = []
    dropping = []
    shorting = []
    bbacking = []
    prevSighting = 0
    ratio = 8/15
    buildingg = ''
    droppingg = ''
    shortingg = ''
    bbackingg = ''
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

        desiredDistance = 0.0012
        logger.print(spread, self.building, self.shorting, self.bbacking, self.dropping)

        if spread > 1 + desiredDistance:
            self.shortingg = 'PINA_COLADAS'
            self.buildingg = 'COCONUTS' 
        elif spread < 1 - desiredDistance:
            self.shortingg = 'COCONUTS'
            self.buildingg = 'PINA_COLADAS'
        else:
            self.droppingg = self.buildingg
            self.bbackingg = self.shortingg
            self.buildingg = ''
            self.shortingg = ''

        
        self.ticker += 100
        if (self.ticker - 140000) % 1000000 == 0:
            self.building.append("BERRIES")
        elif (self.ticker - 490000) % 1000000 == 0:
            self.shorting.append("BERRIES")
        
        sightings = int(state.observations['DOLPHIN_SIGHTINGS'])
        delta = sightings - self.prevSighting

        if self.prevSighting != 0:
            if delta >= 3:
                self.building.append("DIVING_GEAR")
                if "DIVING_GEAR" in self.shorting:
                    self.shorting.remove("DIVING_GEAR")
            elif delta <= -3:
                self.shorting.append("DIVING_GEAR")
                if "DIVING_GEAR" in self.building:
                    self.building.remove("DIVING_GEAR")
            else:
                if "DIVING GEAR" in self.building:
                    self.building.remove("DIVING_GEAR")
                    self.dropping.append("DIVING_GEAR")
                if "DIVING GEAR" in self.shorting:
                    self.shorting.remove("DIVING_GEAR")
                    self.bbacking.append("DIVING_GEAR")

        self.prevSighting = sightings
            
            
        
        
        for i in self.shorting:
            if i in self.bbacking:
                self.bbacking.remove(i) 
        for i in self.building:
            if i in self.bbacking:
                self.dropping.remove(i)

        if self.building != []:
            
            for i in self.building:
              amt = state.position.get(i, 0) 
              order_depth: OrderDepth = state.order_depths[i]
              best_ask = min(order_depth.sell_orders.keys())
              vol = self.limits[i]

              if amt < vol:
                  orders: list[Order] = []
                  orders.append(Order(i, best_ask, vol-amt))
                  result[i] = orders
              else:
                  self.building.remove(i)
        
        if self.bbacking != []:
            for i in self.bbacking:
              amt = state.position.get(i, 0) 
              if amt < 0:
                  order_depth: OrderDepth = state.order_depths[i]
                  best_ask = min(order_depth.sell_orders.keys())
                  vol = self.limits[i]
                  orders: list[Order] = []
                  orders.append(Order(i, best_ask, -amt))
                  result[i] = orders
              else:
                  self.bbacking.remove(i)


        if self.shorting != []:
            for i in self.shorting:
              amt = state.position.get(i, 0) 
              order_depth: OrderDepth = state.order_depths[i]
              best_ask = max(order_depth.buy_orders.keys())
              vol = self.limits[i]

              if amt > -vol:
                  orders: list[Order] = []
                  orders.append(Order(i, best_ask, -vol-amt))
                  result[i] = orders
              else:
                  self.shorting.remove(i)

        if self.dropping != []:
            for i in self.dropping:
              amt = state.position.get(i, 0) 

              if amt > 0:
                  order_depth: OrderDepth = state.order_depths[i]
                  best_ask = max(order_depth.buy_orders.keys())
                  orders: list[Order] = []
                  orders.append(Order(i, best_ask, -amt))
                  result[i] = orders
              else:
                  self.dropping.remove(i)
            

        if self.shortingg == self.bbackingg:
            self.bbackingg = ''
        if self.buildingg == self.droppingg:
            self.droppingg = ''

        if self.buildingg != '':
            amt = state.position.get(self.buildingg, 0) 
            order_depth: OrderDepth = state.order_depths[self.buildingg]
            best_ask = min(order_depth.sell_orders.keys())
            vol = int(sharedamt // best_ask)

            if amt < vol:
                orders: list[Order] = []
                orders.append(Order(self.buildingg, best_ask, vol-amt))
                result[self.buildingg] = orders
            else:
                self.buildingg = ''
        
        if self.bbackingg != '':
            amt = state.position.get(self.bbackingg, 0) 

            if amt < 0:
                order_depth: OrderDepth = state.order_depths[self.bbackingg]
                best_ask = min(order_depth.sell_orders.keys())
                vol = sharedamt / best_ask
                orders: list[Order] = []
                orders.append(Order(self.bbackingg, best_ask, -amt))
                result[self.bbackingg] = orders
            else:
                self.bbackingg = ''


        if self.shortingg != '':
            amt = state.position.get(self.shortingg, 0) 
            order_depth: OrderDepth = state.order_depths[self.shortingg]
            best_ask = max(order_depth.buy_orders.keys())
            vol = int(sharedamt // best_ask)

            if amt > -vol:
                orders: list[Order] = []
                orders.append(Order(self.shortingg, best_ask, -vol-amt))
                result[self.shortingg] = orders
            else:
                self.shortingg = ''

        if self.droppingg != '':
            amt = state.position.get(self.droppingg, 0) 

            if amt > 0:
                order_depth: OrderDepth = state.order_depths[self.droppingg]
                best_ask = max(order_depth.buy_orders.keys())
                orders: list[Order] = []
                orders.append(Order(self.droppingg, best_ask, -amt))
                result[self.droppingg] = orders
            else:
                self.droppingg = ''

        logger.flush(state, result)
        return result
