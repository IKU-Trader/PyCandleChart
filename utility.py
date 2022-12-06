# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 19:37:00 2022

@author: IKU-Trader
"""

import os
import pytz
from datetime import datetime, timezone
import pandas as pd


def pyTime(year, month, day, hour, minute, second, tzinfo):
    t = datetime(year, month, day, hour, minute, second)
    time = tzinfo.localize(t)
    return time

def parseTime(date, time):
    form = '%d/%m/%Y-%H:%M:%S'
    t = datetime.strptime(date + '-' + time, form)
    time = pyTime(t.year, t.month, t.day, t.hour, t.minute, 0, pytz.timezone('America/Chicago'))
    #time = pytz.timezone('America/Chicago').localize(t)
    utc = time.astimezone(timezone.utc)
    return time, utc

def convert():
    path = './data/ym-1m.csv'
    os.mkdir('./data/DJI')
    
    f = open(path, 'r')
    l = f.readline()
    tohlcv = []
    while l:
        values = l.split(';')
        date_str = values[0]
        time_str = values[1]
        op = float(values[2])
        hi = float(values[3])
        lo = float(values[4])
        cl = float(values[5])
        vo = float(values[6])
        t, utc = parseTime(date_str, time_str)
        tohlcv.append([utc, op, hi, lo, cl, vo])
        l = f.readline()
    f.close()
    
    
    for year in range(2007, 2023):
        d = []
        for value in tohlcv:
            if value[0].year == year:
                d.append(value)
                
        if len(d) > 0:
            print('found ', year, len(d))
            filepath = f'./data/DJI/DJI_Feature_{year}.csv'
            df = pd.DataFrame(data=d, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])                
            df.to_csv(filepath, index=False)



if __name__ == '__main__':
    convert()
    
    

