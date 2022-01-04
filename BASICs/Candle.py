#each candle has open(o), high(h), low(l), close(c):
class Candle:
    def __init__(self, o:float, h:float, l:float, c:float):
        self.o = o
        self.h = h
        self.l = l
        self.c = c

        self.body = abs(o - c)
        self.up_shadow = h - max(o, c)
        self.down_shadow = min(o, c) - l

        self.is_bearish = c > o 
        self.is_bullish = c < o
