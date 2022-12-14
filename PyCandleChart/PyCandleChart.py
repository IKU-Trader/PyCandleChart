# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 22:02:43 2022

@author: IKU-Trader
"""

import os
import sys


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import matplotlib.gridspec as gridspec

DATE_FORMAT_TIME = '%H:%M'
DATE_FORMAT_DAY = '%m-%d'
DATE_FORMAT_DAY_TIME = '%m-%d %H:%M'

LIGHT_GREEN = '#22bbbb'
LIGHT_RED = '#ee9999'
RED = '#ff4444'
GREEN = '#44ffcc'


def candleData2arrays(ohlc):
    if len(ohlc) == 0:
        return []
    n = len(ohlc[0])
    arrays = []
    for i in range(n):
        array = []
        for data in ohlc:
            array.append(data[i])
        arrays.append(array)
    return arrays

def array2Candle(ohlc_arrays):
    out = []
    n = len(ohlc_arrays)
    size = len(ohlc_arrays[0])
    for i in range(size):
        v = []
        for j in range(n):
            v.append(ohlc_arrays[j][i])
        out.append(v)
    return out        

def makeFig(rows, cols, size):
    fig, ax = plt.subplots(rows, cols, figsize=(size[0], size[1]))
    return (fig, ax)

def gridFig(row_rate, size):
    rows = sum(row_rate)
    fig = plt.figure(figsize=size)
    gs = gridspec.GridSpec(rows, 1)
    axes = []
    begin = 0
    for rate in row_rate:
        end = begin + rate
        ax = plt.subplot(gs[begin: end, 0])
        axes.append(ax)
        begin = end
    return (fig, axes)

def awarePytime2naive(time):
    naive = datetime(time.year, time.month, time.day, time.hour, time.minute, time.second)
    return naive

def awarePyTime2Float(time):
    naive = awarePytime2naive(time)
    t = mdates.date2num([naive])
    return t[0]

def awarePyTimeList2Float(aware_pytime_list):
    naives = []
    for time in aware_pytime_list:
        naive = awarePytime2naive(time)
        naives.append(naive)
    return mdates.date2num(naives)
    
class CandleGraphic:
    def __init__(self, py_time, ohlc, box_width):
        if len(ohlc) < 4:
            raise Exception('Bad ohlc data')
        

        self.box_width = box_width
        self.line_width = 1.0
        self.alpha = 0.7
        self.box_body_color_positive = LIGHT_GREEN
        self.box_line_color_positive = GREEN
        self.box_body_color_negative = LIGHT_RED
        self.box_line_color_negative = RED
        
        t = awarePyTime2Float(py_time)
        op = ohlc[0]
        hi = ohlc[1]
        lo = ohlc[2]
        cl = ohlc[3]
        if cl >= op:
            body_color = self.box_body_color_positive
            line_color = self.box_line_color_positive
            box_low = op
            box_high = cl
            height = cl - op
        else:
            body_color = self.box_body_color_negative
            line_color = self.box_line_color_negative
            box_low = cl
            box_high = op
            height = op - cl
            
        line_upper = Line2D(xdata=(t, t),
                            ydata=(box_high, hi),
                            color=line_color,
                            linewidth=self.line_width,
                            antialiased=True)
        line_lower = Line2D(xdata=(t, t),
                            ydata=(box_low, lo),
                            color=line_color,
                            linewidth=self.line_width,
                            antialiased=True)

        rect = Rectangle(xy=(t - self.box_width / 2, box_low),
                         width=self.box_width,
                         height=height,
                         facecolor=body_color,
                         edgecolor=body_color)
        rect.set_alpha(self.alpha)

        self.line_upper = line_upper
        self.line_lower = line_lower
        self.rect = rect
        return
    
    def setObject(self, ax):
        ax.add_line(self.line_upper)
        ax.add_line(self.line_lower)
        ax.add_patch(self.rect)
        return
    
class BoxGraphic:
    def __init__(self, py_time, box_width, value, color):
        self.alpha = 0.7
        t = awarePyTime2Float(py_time)
        if value >= 0:
            box_low = 0.0
            box_height = value
        else:
            box_low = value
            box_height = -value
        rect = Rectangle(xy=(t - box_width / 2, box_low),
                         width=box_width,
                         height=box_height,
                         facecolor=color,
                         edgecolor=color)
        rect.set_alpha(self.alpha)
        self.rect = rect
        return
    
    def setObject(self, ax):
        ax.add_patch(self.rect)
        return
    
# -----

class PyCandleChart:
    def __init__(self, fig, ax, title, date_format=DATE_FORMAT_TIME):
        self.fig = fig
        self.ax = ax
        self.title = title
        self.ax.grid(True)
        self.ax.xaxis_date()
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
        pass
        
    def drawCandle(self, time, ohlc_arrays, bar_width=None, timerange=None):    
        if len(ohlc_arrays) == 0:
            raise Exception('ohlc_arrays is bad')
        if len(ohlc_arrays[0]) < 4:
            raise Exception('ohlc_arrays is bad')
            
        op = ohlc_arrays[0]
        hi = ohlc_arrays[1]
        lo = ohlc_arrays[2]
        cl = ohlc_arrays[3]
        
        self.ax.set_title(self.title)
        n = len(time)
        t0 = awarePyTime2Float(time[0])
        t1 = awarePyTime2Float(time[-1])
        if bar_width is None:
            self.box_width = (t1 - t0 ) / n / 2.0
        else:
            self.box_width = bar_width
            
        self.graphic_objects = []
        begin = None
        end = None
        vmin = None
        vmax = None
        for i in range(n):
            t = time[i]
            if timerange is None:
                if vmin is None:
                    vmin = lo[i] 
                    vmax = hi[i]
                else:
                    if vmin > lo[i]:
                        vmin = lo[i]
                    if vmax < hi[i]:
                        vmax = hi[i]
            else:
                if begin is None:
                    if t >= timerange[0]:
                        begin = i
                        vmin = lo[i]
                        vmax = hi[i]
                else:
                    if t <= timerange[1]:
                        if vmin > lo[i]:
                            vmin = lo[i]
                        if vmax < hi[i]:
                            vmax = hi[i]
                    else:
                        end = i - 1
            value = [op[i], hi[i], lo[i], cl[i]]
            obj = CandleGraphic(t, value, self.box_width)
            obj.setObject(self.ax)
            self.graphic_objects.append(obj)
        if vmin is not None and vmax is not None:
            dw = (vmax - vmin) * 0.05
            self.ylimit([vmin - dw, vmax + dw])
        
        if timerange is not None:
            t0 = awarePyTime2Float(timerange[0])
            t1 = awarePyTime2Float(timerange[1])
            tick = self.ticks(timerange[0], timerange[1], 10)   
        else:
            tick = self.ticks(time[0], time[-1], 10)
        
        self.ax.set_xlim(t0, t1)
             
        self.ax.set_xticks(tick)
        
        
        #self.ax.autoscale_view()
        return
    
    def ticks(self, t0, t1, dt_minutes):
        tm = int(t0.minute / dt_minutes) * dt_minutes
        time = datetime(t0.year, t0.month, t0.day, t0.hour, tm, tzinfo=t0.tzinfo)
        ticks = []
        while time < t1:
            ticks.append(awarePyTime2Float(time))
            time += timedelta(minutes=dt_minutes)
        return ticks
        
    
    
    def drawLine(self, time, value, color='red', linestyle='solid', linewidth=1.0, ylim=None, label=''):
        tfloat = awarePyTimeList2Float(time)
        self.ax.plot(tfloat, value, color=color, linestyle=linestyle, linewidth=linewidth, label=label)
        if ylim is not None:
            self.ax.set_ylim(ylim[0], ylim[1])
        self.ax.set_xlim(tfloat[0], tfloat[-1])
        self.ax.grid(True)
        return
    
    def hline(self, y, color='black', linewidth=1.0):
        xmin, xmax = self.ax.get_xlim()
        self.ax.hlines(y=y, color=color, linewidth=linewidth, xmin=xmin, xmax=xmax)
        
    def vline(self, x, color='black', linewidth=1.0):
        ymin, ymax = self.ax.get_ylim()
        self.ax.vlines(x=x, color=color, linewidth=linewidth, ymin=ymin, ymax=ymax)
    
    def drawBar(self, time, value, colors=['green', 'red'], ylim=None, label=''):
        t0 = awarePyTime2Float(time[0])
        t1 = awarePyTime2Float(time[9])
        w = (t1 - t0) * 0.9 / 10.0
        for t, v in zip(time, value):
            if v is not None:
                if v >= 0:
                    color = colors[0]
                else:
                    color = colors[1]
                obj = BoxGraphic(t, w, v, color)
                obj.setObject(self.ax)
        if ylim is not None:
            self.ax.set_ylim(ylim[0], ylim[1])
        self.ax.grid()
        return
    
    def drawBar2(self, time, value, color='red', ylim=None):
        t = []
        v = []
        for tt, vv in zip(time, value):
            t.append(tt)
            if vv is None:
                v.append(0)
            else:
                v.append(vv)
                
        t0 = awarePyTime2Float(t[0])
        t1 = awarePyTime2Float(t[1])
        self.ax.bar(t, v, color=color, width= (t1 - t0) * 0.9)
        if ylim is not None:
            self.ax.set_ylim(ylim[0], ylim[1])
        self.ax.grid()
        return
    
    def drawMarkers(self, time, ref, offset, signal, value, marker, color, markersize=10):
        for t, r, s in zip(time, ref, signal):
            if s == value:
                self.drawMarker(t, r + offset, marker, color, markersize=markersize)
        
    def drawMarker(self, time, value, marker, color, markersize=10):
        t = awarePyTime2Float(time)
        self.ax.plot(t, value, marker=marker, color=color, markersize=markersize)
        return
    
    def drawText(self, time, value, text, size=10):
        t = awarePyTime2Float(time)
        self.ax.text(t, value, text, size=size)
        return
    
    def xlimit(self, x):
        self.ax.set_xlim(x[0], x[1])
        self.ax.grid(True)
        
    def ylimit(self, yrange):
        self.ax.set_ylim(yrange[0], yrange[1])
        
    def getXlimit(self):
        return self.ax.get_xlim()
    
    def getYlimit(self):
        return self.ax.get_ylim()
        
class PyBandPlot:
    def __init__(self, fig, ax, title, date_format=DATE_FORMAT_DAY_TIME):
        self.fig = fig
        self.ax = ax
        self.title = title
        self.ax.grid()
        self.ax.xaxis_date()
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
        self.ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=6))
        self.ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval=6))
        pass
        
    def boxWidth(self, time1, time2):
        t1 = awarePyTime2Float(time1)
        t2 = awarePyTime2Float(time2)
        return t2 - t1
    
    def drawBand(self, time, status, colors=None):
        if colors is None:
            colors = ['black', 'blue', 'red', 'pink', 'green', 'cyan', 'brown']
        self.ax.set_title(self.title)
        n = len(time)
        if n < 2:
            return
        
        box_width = self.boxWidth(time[0], time[1])
        self.graphic_objects = []
        for i in range(n):
            t = time[i]
            s = status[i]
            if s > 0:
                c = colors[s]
                obj = BoxGraphic(t, box_width, c)
                obj.setObject(self.ax)
                self.graphic_objects.append(obj)  
        self.ax.autoscale_view()
        return        
        
    def drawLine(self, time, value, color='red', linestyle='solid', linewidth=1.0, timerange=None):
        if timerange is not None:
            begin = None
            end = None
            for i in range(len(time)):
                t = time[i]
                if begin is None:
                    if t >= timerange[0]:
                        begin = i
                else:
                    if t > timerange[1]:
                        end = i - 1
                        break
            if begin is None:
                begin = 0
            if end is None:
                end = len(time) - 1
            time2 = time[begin: end + 1]
            value2 = value[begin: end + 1]
        else:
            time2 = time
            value2 = value
        
        #(time3, value3) = self.removeNan(time2, value2)
        vmin = np.nanmin(value2)
        vmax = np.nanmax(value2)
        dw = (vmax - vmin) * 0.2
        vmax += dw
        vmin -= dw
        self.ylimit((vmin, vmax))
        self.ax.plot(time2, value2, color=color, linestyle=linestyle, linewidth=linewidth)
        self.ax.grid(True)
        self.fig.show()
        return     
    
    def xlimit(self, trange):
        self.ax.set_xlim(trange[0], trange[1])
        
    def ylimit(self, yrange):
        self.ax.set_ylim(yrange[0], yrange[1])
          



