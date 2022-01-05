import MA as ma
import matplotlib.pyplot as plt

data = yf.download('BTC-USD', '2021-1-4', '2022-1-4').to_dict()

OPENS = [data['Open'][o] for o in data['Open']]
CLOSES = [data['Close'][i] for i in data['Close']]
HIGHS = [data['High'][o] for o in data['High']]
LOWS = [data['Low'][o] for o in data['Low']]


candles = [Candle(OPENS[i], HIGHS[i], LOWS[i], CLOSES[i]) for i in range(len(LOWS))]

MA5 = ma.MA(candles, period=5, offset=5)
MA10 = ma.MA(candles, period=10, offset=10)
MA20 = ma.MA(candles, period=20, offset=20)

closes = [candle.c for candle in candles]

plt.plot(MA5, color='#ffba08')
plt.plot(MA10, color='#e85d04')
plt.plot(MA20, color='#9d0208')

plt.plot(closes, color='#3772FF')

plt.show()
