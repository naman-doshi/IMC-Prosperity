# Versions

## MarketMaker

### v1

Trades pearls and bananas up to 20 units each, then attempts to trade down to a predefined threshold value. Once here, it attempts to trade back to 20 units although orders are almost never fully executed, so position sizes usually hover around the threshold value. However, its limitations are that it has an inherent bullish bias and isn't a true market making algorithm. Also, trades do not have a guaranteed profit. Next steps would be to save data between tradingstates and ensure that every trade is profitable.

### v1.1

Trades both instruments up and down using variables, making to sure to go in a predefined direction. Currently optimised for a threshold of 12 units, giving a ~$1.7k end profit in the tutorial. The next step is to ensure that every trade is profitable.

### v1.2

Ensures every trade is profitable, although it may suffer from drawdowns — a PnL counter would be interesting. Currently optimised for a threshold of 12 units, giving a ~$1k end profit in the tutorial.

## RSI

### v1

## SMA

### v1

Primitive algorithm using rolling averages and checking whether the price is above or below, results are dismal even when optimising the window size. Best result is +100 at its peak. Perhaps something is wrong?

### v1.1

Restructured v1, but performance is still the same.

### v1.2

Added a short and long SMA, and buys if short > long and shorts if short < long. Future versions will need to get signals based on crossovers. Interestingly, this model produces 40k in losses.

### v1.3

Gets signals based on crossovers.

### v1.4

Mean reversion for only pearls, best algorithm so far with a 1.48k profit.

### v1.5

Mean reversion for pearls + bananas, best algorithm so far with a 1.48k profit.
