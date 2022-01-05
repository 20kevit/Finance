#defined in BASICs folder:
import Candle

def EMA(data, length=10, offset=0, source="c"):
    if(source == "o"):
        array = [candle.o for candle in data]
    if(source == "h"):
        array = [candle.h for candle in data]
    if(source == "l"):
        array = [candle.l for candle in data]
    if(source == "c"):
        array = [candle.c for candle in data]
    else:
        return None

    result = list()
    alpha = 2 / (length + 1)
    for i in range(len(array) + offset):
        if(i + 1 < length + offset):
            result.append(None)
            
        elif(i + 1 == length + offset):
            start = i - length + 1
            end = i + 1
            average = sum(array[start - offset : end - offset]) / length
            result.append(average)
        else:
            last_ema = result[-1]
            ema = (array[i - offset] * alpha) + (last_ema * (1 - alpha))
            result.append(ema)
            
    return result
