# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 22:03:12 2022

@author: IKU-Trader
"""
from datetime import datetime
import pandas as pd
import pytz
from PyCandleChart import PyCandleChart, candleData2arrays, makeFig
from time_utility import changeTimezone, TIMEZONE_TOKYO, str2pytimeArray, sliceTime

def test():

    df = pd.read_csv('../data/DJI/DJI_Feature_2019.csv')
    tohlcv = candleData2arrays(df.values)
    time = str2pytimeArray(tohlcv[0], pytz.utc)
    jst = changeTimezone(time, TIMEZONE_TOKYO) 
    print(jst[0],  '->', jst[-1])
    
    t0 = datetime(2019, 8, 6, 1).astimezone(TIMEZONE_TOKYO)
    t1 = datetime(2019, 8, 6, 6).astimezone(TIMEZONE_TOKYO)
    length, begin, end = sliceTime(jst, t0, t1)
    
    jst = jst[begin:end+1]
    op = tohlcv[1][begin:end+1]
    hi = tohlcv[2][begin:end+1]
    lo = tohlcv[3][begin:end+1]
    cl = tohlcv[4][begin:end+1]
    vo = tohlcv[5][begin:end+1]
    ohlcv = [op, hi, lo, cl, vo]
    
    fig, ax = makeFig(1, 1, (40, 8))
    chart = PyCandleChart(fig, ax, 'DJI2019/8/6')
    chart.drawCandle(jst, ohlcv)
    
    
    
    

if __name__ == '__main__':
    test()