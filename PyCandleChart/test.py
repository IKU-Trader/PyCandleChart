# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 22:03:12 2022

@author: IKU-Trader
"""
from datetime import datetime
import pandas as pd
import numpy as np
import pytz
from PyCandleChart import PyCandleChart, candleData2arrays, makeFig, gridFig
from time_utility import changeTimezone, TIMEZONE_TOKYO, str2pytimeArray, sliceTime



def midpoint(ohlcv):
    op = ohlcv[0]
    cl = ohlcv[3]
    mid = []
    for o, c in zip(op, cl):
        mid.append( (o + c ) / 2)
    return np.array(mid)
    
def momentum(array, distance):
    n = len(array)
    mom = np.full(n, np.nan)
    for i in range(distance, n):
        d = array[i] - array[i - distance]
        mom[i] = d
    return np.array(mom)

def momentumPercent(array, distance):
    n = len(array)
    mom = np.full(n, np.nan)
    for i in range(distance, n):
        d = array[i] - array[i - distance]
        mom[i] = d / array[i - distance] * 100.0
    return np.array(mom)    

def sma(array, period):
    n = len(array)
    out = []
    for i in range(n):
        if i < period - 1:
            out.append(np.nan)
        else:
            a = array[i - period + 1: i + 1]
            out.append(sum(a) / period)
    return np.array(out)

def polarity(array, threshold=0.0, values=(1.0, -1.0)):
    out = [values[0] if v >= threshold else values[-1] for v in array]
    return np.array(out)


def crossPoint(array, threshold=0.0):
    n = len(array)
    up = []
    down = []
    for i in range(1, n):
        if array[i - 1] <= threshold and array[i] > threshold:
            up.append([i, array[i]])
        if array[i - 1] >= threshold and array[i] < threshold:
            down.append([i, array[i]])
    return up, down
    

def backward(ohlc):
    n = len(ohlc[0])
    out = np.zeros(n)
    op = ohlc[0]
    hi = ohlc[1]
    lo = ohlc[2]
    cl = ohlc[3]
    for i in range(1, n):
        mid = (op[i - 1] + cl[i - 1]) / 2
        if cl[i - 1] >= op[i - 1]:
            #positive
            out[i] = lo[i] - op[i - 1]
        else:
            out[i] = op[i - 1] - hi[i]
    return out
    
    
    


def test():

    df = pd.read_csv('../data/DJI/DJI_Feature_2019_08.csv')
    tohlcv = candleData2arrays(df.values)
    time = str2pytimeArray(tohlcv[0], pytz.utc)
    jst = changeTimezone(time, TIMEZONE_TOKYO) 
    print(jst[0],  '->', jst[-1])
    
    t0 = datetime(2019, 8, 5, 23).astimezone(TIMEZONE_TOKYO)
    t1 = datetime(2019, 8, 6, 5).astimezone(TIMEZONE_TOKYO)
    length, begin, end = sliceTime(jst, t0, t1)
    if length == 0:
        return
    
    jst = jst[begin:end+1]
    op = tohlcv[1][begin:end+1]
    hi = tohlcv[2][begin:end+1]
    lo = tohlcv[3][begin:end+1]
    cl = tohlcv[4][begin:end+1]
    vo = tohlcv[5][begin:end+1]
    ohlcv = [op, hi, lo, cl, vo]
    
    sma5 = sma(tohlcv[4], 5)
    sma20 = sma(tohlcv[4], 20)
    mid = midpoint(tohlcv[1:])
    back = backward(tohlcv[1:])
    
    sma5 = sma5[begin: end + 1]
    sma20 = sma20[begin: end + 1]
    mid = mid[begin: end + 1]
    back = back[begin: end + 1]
    dif = (sma5 - sma20) / cl[0] * 100.0
    
    fig, axes = gridFig([8, 4, 2], (20, 8))
    chart1 = PyCandleChart(fig, axes[0], 'DJI2019/8/6')
    chart1.drawCandle(jst, ohlcv)    
    chart1.drawLine(jst, sma5, color='red')
    chart1.drawLine(jst, sma20, color='blue')
    
    up_points, down_points = crossPoint(dif)
    for i, value in up_points:
        chart1.drawMarker(jst[i], hi[i], '^', 'green')
    for i, _ in down_points:
        chart1.drawMarker(jst[i], hi[i], 'v', 'red')
    
    chart2 = PyCandleChart(fig, axes[2], '')
    chart2.drawLine(jst, dif)
    
    chart3 = PyCandleChart(fig, axes[1], '')
    chart3.drawLine(jst, back, color='orange')

if __name__ == '__main__':
    test()