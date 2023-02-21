# Versions

## MarketMaker

### v1

Trades pearls and bananas up to 20 units each, then attempts to trade down to a predefined threshold value. Once here, it attempts to trade back to 20 units although orders are almost never fully executed, so position sizes usually hover around the threshold value. However, its limitations are that it has an inherent bullish bias and isn't a true market making algorithm. Also, trades do not have a guaranteed profit. Next steps would be to save data between tradingstates and ensure that every trade is profitable.

### v1.1

Trades both instruments up and down using variables, making to sure to go in a predefined direction. Currently optimised for a threshold of 12 units, giving a ~$1.7k end profit in the tutorial. The next step is to ensure that every trade is profitable.
