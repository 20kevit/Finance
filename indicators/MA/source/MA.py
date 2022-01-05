#located in Finance/BASICs/Candle.py:
import Candle

#returns a list contains MA values:
def MA(data, period=9, offset=0, source="c"): #data -> a list of Candle object
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
    for i in range(len(array) + offset):
        if(i >= period + offset - 1 ):
            start = i - period  + 1
            end = i + 1
            average = sum(array[start-offset : end-offset]) / period
            result.append(average)
        else:
            result.append(None)
    return(result)
