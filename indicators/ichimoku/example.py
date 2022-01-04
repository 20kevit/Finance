import matplotlib.pyplot as plt
import yfinance as yf
import ichimoku as im

data = yf.download('BTC-USD', '2017-1-4', '2022-1-4').to_dict()

OPEN = [data['Open'][o] for o in data['Open']]
CLOSE = [data['Close'][c] for c in data['Close']]
HIGH = [data['High'][h] for h in data['High']]
LOW = [data['Low'][l] for l in data['Low']]

candles = [im.Candle(OPEN[i], HIGH[i], LOW[i], CLOSE[i]) for i in range(len(LOWS))]

ichi = calculate_ichimoku(candles)

plot_ichimoku(ichi)
