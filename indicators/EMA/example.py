import Candle
from EMA import EMA

data = yf.download('BTC-USD', '2021-1-4', '2022-1-4').to_dict()

OPENs = [data['Open'][o] for o in data['Open']]
CLOSEs = [data['Close'][c] for c in data['Close']]
HIGHs = [data['High'][h] for h in data['High']]
LOWs = [data['Low'][l] for l in data['Low']]

candles = [Candle(OPENs[i], HIGHs[i], LOWs[i], CLOSEs[i]) for i in range(len(LOWs))]
ema20 = EMA(candles, length=20)
plt.plot(ema20, color='#ffba08')

closes = [candle.c for candle in candles]
plt.plot(closes, color='#3772FF')

plt.show()
