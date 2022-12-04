# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 19:37:00 2022

@author: IKU-Trader
"""

import os
import pytz
from datetime import datetime, timezone
import pandas as pd

def parseTime(date, time):
    form = '%d/%m/%Y-%H:%M:%S'
    t = datetime.strptime(date + '-' + time, form)
    t = datetime(t.year, t.month, t.day, t.hour, t.minute, tzinfo=pytz.timezone('America/Chicago'))
    utc = t.astimezone(timezone.utc)
    return t, utc

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
        lo = float(values[3])
        cl = float(values[4])
        vo = float(values[5])
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
    
    

