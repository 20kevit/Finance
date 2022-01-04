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
                       lagging_span_periods=52,
                       displacement=26
                       ):
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

    return result

def plot_ichimoku(data,
                  conversion_color = '#2962FF',
                  base_color = '#B71C1C',
                  lead1_color = '#A5D6A7',
                  lead2_color = '#EF9A9A',
                  lagging_span_color = '#43A047',
                  ):
    
    conversion_line = [i.conversion for i in data]
    plt.plot(conversion_line, color=conversion_color)

    base_line = [i.base for i in data]
    plt.plot(base_line, color = base_color)

    lead_line1 = [i.lead1 for i in data]
    plt.plot(lead_line1, color = lead1_color)

    lead_line2 = [i.lead2 for i in data]
    plt.plot(lead_line2, color = lead2_color)

    lagging_span = [i.lagging_span for i in data]
    plt.plot(lagging_span, color = lagging_span_color)

    
    x = range(len(data))
    red_where, green_where = list(), list()
    for i in data:
        if(not i.lead1 or not i.lead2):
            i.lead1 = 0
            i.lead2 = 0
            red_where.append(False)
            green_where.append(False)
        else:
            green_where.append(i.lead1 > i.lead2)
            red_where.append(i.lead1 < i.lead2)

    plt.fill_between(x, [i.lead1 for i in data], [i.lead2 for i in data], color='#EF9A9A50', where=red_where)
    plt.fill_between(x, [i.lead1 for i in data], [i.lead2 for i in data], color='#A5D6A750', where=green_where)
    
    plt.show()
