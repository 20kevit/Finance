import MA as ma
data = yf.download('BTC-USD', '2020-1-4', '2022-1-4').to_dict()

OPENS = [data['Open'][o] for o in data['Open']]
CLOSES = [data['Close'][i] for i in data['Close']]
HIGHS = [data['High'][o] for o in data['High']]
LOWS = [data['Low'][o] for o in data['Low']]


candles = [Candle(OPENS[i], HIGHS[i], LOWS[i], CLOSES[i]) for i in range(len(LOWS))]

MA10 = ma.MA(candles, period=10)
MA50 = ma.MA(candles, period=50)
MA100 = ma.MA(candles, period=100)
MA200 = ma.MA(candles, period=200)

closes = [candle.c for candle in candles]

plt.plot(MA10, color='#ffba08')
plt.plot(MA50, color='#e85d04')
plt.plot(MA100, color='#9d0208')
plt.plot(MA200, color='#03071e')

plt.plot(closes, color='#3772FF')

plt.show()
