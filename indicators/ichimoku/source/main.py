import matplotlib.pyplot as plt

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

#
class Ichimoku:
    def __init__(self, conversion, base, lead1, lead2, lagging_span):
        self.conversion = conversion
        self.base = base
        self.lead1 = lead1
        self.lead2 = lead2
        self.lagging_span = lagging_span

#calculate average of highest and lowest price in a period:
def donchian(high_list, low_list):
    result = max(high_list) + min(low_list)
    result /= 2
    return result

#returns a list of Ichimoku objects:
def calculate_ichimoku(data, #is a list of Candle objects
                       conversion_periods=9,
                       base_periods=26,
                       lagging_span_periods=52
                       ):
    open_prices = [candle.o for candle in data]
    high_prices = [candle.h for candle in data]
    low_prices = [candle.l for candle in data]
    close_prices = [candle.c for candle in data]

    result = []

    for i in range(len(data)):
        #conversion:
        if(i >= conversion_periods):
            high_list = high_prices[i - conversion_periods + 1: i + 1]
            low_list = low_prices[i - conversion_periods + 1 : i + 1]
            conversion = donchian(high_list, low_list)
        else:
            conversion = None
        
        #base:
        if(i >= base_periods):
            high_list = high_prices[i + 1 - base_periods : i + 1]
            low_list = low_prices[i + 1 - base_periods : i + 1]
            base = donchian(high_list, low_list)
        else:
            base = None
            
        #lead1:
        if(conversion and base):
            lead1 = conversion + base
            lead1 /= 2
        else:
            lead1 = None

        #lead2:
        if(i >= lagging_span_periods):
            high_list = high_prices[i + 1 - lagging_span_periods : i + 1]
            low_list = low_prices[i + 1 - lagging_span_periods : i + 1]
            lead2 = donchian(high_list, low_list)
        else:
            lead2 = None

        #lagging_span:
        lagging_span = close_prices[i]

        new_item = Ichimoku(conversion, base, lead1, lead2, lagging_span)
        result.append(new_item)

    return result


def plot_ichimoku(data,
                  displacement = 26,
                  conversion_color = '#2962FF',
                  base_color = '#B71C1C',
                  lead1_color = '#A5D6A7',
                  lead2_color = '#EF9A9A',
                  lagging_span_color = '#43A047',
                  ):
    displacement -= 1
    D = [None for i in range(displacement)]
    
    conversion_line = array(D + [i.conversion for i in data] + D)
    plt.plot(conversion_line, color=conversion_color)

    base_line = array(D + [i.base for i in data] + D)
    plt.plot(base_line, color = base_color)

    lead_line1 = array(D + D + [i.lead1 for i in data])
    plt.plot(lead_line1, color = lead1_color)

    lead_line2 = array(D + D + [i.lead2 for i in data])
    plt.plot(lead_line2, color = lead2_color)

    lagging_span = array([i.lagging_span for i in data] + D + D)
    plt.plot(lagging_span, color = lagging_span_color)

    
    x = range(2 * displacement + len(data))
    
    for i in data:
        if(not i.lead1 or not i.lead2):
            i.lead1 = 0
            i.lead2 = 0
            
    D = [0 for i in range(displacement)]
    lead1 = array(D + D + [i.lead1 for i in data])
    lead2 = array(D + D + [i.lead2 for i in data])

    W = [False for i in range(displacement)]
    plt.fill_between(x, lead1, lead2, color=lead1_color+'50', where= W + W + [i.lead1 > i.lead2 for i in data])
    plt.fill_between(x, lead1, lead2, color=lead2_color+'50', where= W + W + [i.lead1 < i.lead2 for i in data])
    
    plt.show()
