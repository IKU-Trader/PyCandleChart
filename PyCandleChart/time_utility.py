# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 22:37:16 2022

@author: IKU-Trader
"""

import datetime
import calendar
import pytz

TIMEZONE_TOKYO = datetime.timezone(datetime.timedelta(hours=+9), 'Asia/Tokyo')

def changeTimezone(pytime_array: [datetime.datetime], tzinfo):
    out =[]
    for i in range(len(pytime_array)):
        t = pytime_array[i].astimezone(tzinfo)
        out.append(t)
    return out

def sliceTime(pytime_array: list, time_from, time_to):
    begin = None
    end = None
    for i in range(len(pytime_array)):
        t = pytime_array[i]
        if begin is None:
            if t >= time_from:
                begin = i
        else:
            if t > time_to:
                end = i
                return (end - begin + 1, begin, end)
    if begin is not None:
        end = len(pytime_array) - 1
        return (end - begin + 1, begin, end)
    else:
        return (0, None, None)
    
def str2pytimeArray(time_str_array: [str], tzinfo, form='%Y-%m-%d %H:%M:%S'):
    out = []
    for s in time_str_array:
        i = s.find('+')
        if i > 0:
            s = s[:i]
        t = datetime.datetime.strptime(s, form)
        t = datetime.datetime(t.year, t.month, t.day, t.hour, t.minute, t.second, tzinfo=tzinfo)
        out.append(t)
    return out