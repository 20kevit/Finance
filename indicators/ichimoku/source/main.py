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

class Ichimoku:
    def __init__(self, conversion, base, lead1, lead2, lagging_span):
        self.conversion = conversion
        self.base = base
        self.lead1 = lead1
        self.lead2 = lead2
        self.lagging_span = lagging_span


def donchian(high_list, low_list):
    result = max(high_list) + min(low_list)
    result /= 2
    return result
    
def calculate_ichimoku(data, conversion_periods=9, base_periods=26, lagging_span_periods=52, displacement=26):
    open_prices = [candle.o for candle in data]
    high_prices = [candle.h for candle in data]
    low_prices = [candle.l for candle in data]
    close_prices = [candle.c for candle in data]

    result = []

    for i in range(len(data) + displacement):
        #conversion:
        if(len(data) > i and i >= conversion_periods):
            high_list = high_prices[i - conversion_periods + 1: i + 1]
            low_list = low_prices[i - conversion_periods + 1 : i + 1]
            conversion = donchian(high_list, low_list)
        else:
            conversion = None
        
        #base:
        if(len(data) > i and i >= base_periods):
            high_list = high_prices[i - base_periods + 1 : i + 1]
            low_list = low_prices[i - base_periods + 1 : i + 1]
            base = donchian(high_list, low_list)
        else:
            base = None
            
        #lead1:
        try:
            temp_conversion = result[-displacement].conversion
            temp_base = result[-displacement].base
            lead1 = (temp_conversion + temp_base) / 2
        except:
            lead1 = None

        #lead2:
        if(i >= lagging_span_periods + displacement):
            high_list = high_prices[i - lagging_span_periods - displacement + 1 : i - displacement + 1]
            low_list = low_prices[i - lagging_span_periods - displacement + 1 : i - displacement + 1]
            lead2 = donchian(high_list, low_list)
        else:
            lead2 = None

        #lagging_span:
        if(i + displacement <= len(data)):
            lagging_span = close_prices[i + displacement - 1]
        else:
            lagging_span = None

        new_item = Ichimoku(conversion, base, lead1, lead2, lagging_span)
        result.append(new_item)
        print(new_item.base, ' - ', new_item.conversion)

    return result
