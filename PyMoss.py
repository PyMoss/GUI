from tkinter import *
from tkinter import ttk
import tkinter.filedialog as FileDialog
from PIL import Image, ImageTk
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
import pylab as pylab
import scipy.optimize

root = Tk()
root.wm_iconbitmap("favicon.ico")
root.title("PyMoss")

content = ttk.Frame(root)
graph = Figure(figsize=(8,6), dpi=150)
ax = graph.add_subplot(111)
ax.tick_params(axis='both', which='major', labelsize=8)
ax.tick_params(axis='both', which='minor', labelsize=8)
ax.set_xlabel('Channels', fontsize=8)
ax.set_ylabel('Intensity', fontsize=8)

# Zooming function -------------------------------------------------------------------------------------
class Zoom(object):
    def __init__(self):      
        self.is_pressed = False
        self.x0 = 0.0
        self.y0 = 0.0
        self.x1 = 0.0
        self.y1 = 0.0
        
    def zoom_init(self, x, y):
        graph = Figure(figsize=(5,4), dpi=100)
        self.ax = graph.add_subplot(111)
        self.rect = Rectangle((0,0),0,0)
        self.ax.add_patch(self.rect)   
        self.ax.plot(x, y)
        canvas = FigureCanvasTkAgg(graph, master=RightFrame)
        canvas.show()
        print(x)
        print(y)
        canvas.get_tk_widget().grid(column=2, row=1, rowspan=2, sticky=(N, S, E, W))
        self.aid = graph.canvas.mpl_connect('button_press_event', self.on_press)
        self.bid = graph.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid = graph.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        self.is_pressed = True
        if event.xdata is not None and event.ydata is not None:
            self.x0, self.y0 = event.xdata, event.ydata
            #print('press:', self.x0, self.y0)
            # only remove old rectangle
            self.rect.set_width(0)
            self.rect.set_height(0)
            self.rect.set_xy((self.x0, self.y0))
            self.ax.figure.canvas.draw()
            # color and linestyle for future motion 
            self.rect.set_facecolor('red')
            self.rect.set_linestyle('dashed')

    def on_motion(self, event):
        if self.is_pressed:
            if event.xdata is not None and event.ydata is not None:
                self.x1, self.y1 = event.xdata, event.ydata
                self.rect.set_width(self.x1 - self.x0)
                self.rect.set_height(self.y1 - self.y0)
                self.rect.set_xy((self.x0, self.y0))
                self.ax.figure.canvas.draw()
                #print('rect:', self.x0, self.y0, self.x1, self.y1, (self.x1-self.x0), (self.y1-self.y0))

    def on_release(self, event):
        self.is_pressed = False
        #print('release:', event.xdata, event.ydata)

        # change only color and linestyle
        #self.rect.set_width(self.x1 - self.x0)
        #self.rect.set_height(self.y1 - self.y0)
        #self.rect.set_xy((self.x0, self.y0))
        RightFrame.config(cursor="arrow")
        self.rect.set_facecolor('blue')
        self.rect.set_linestyle('solid')
        #self.ax.figure.canvas.draw()
        if self.x0 > self.x1:
            if self.y0 > self.y1:
                self.minX = self.x1
                self.maxX = self.x0
                self.minY = self.y1
                self.maxY = self.y0
                #print('x0>x1 & y0>y1')
            else:
                self.minX = self.x1
                self.maxX = self.x0
                self.minY = self.y0
                self.maxY = self.y1
                #print('x0>x1 & y0<y1')
        
        if self.x0 < self.x1:
            if self.y0 < self.y1:
                self.minX = self.x0
                self.maxX = self.x1
                self.minY = self.y0
                self.maxY = self.y1
                #print('x0<x1 & y0<y1')
            else:
                self.minX = self.x0
                self.maxX = self.x1
                self.minY = self.y1
                self.maxY = self.y0
                #print('x0<x1 & y0>y1')
            
        global minX, minY, maxX, maxY
        minX = self.minX
        minY = self.minY
        maxX = self.maxX
        maxY = self.maxY
        graph = Figure(figsize=(5,4), dpi=100)
        self.ax = graph.add_subplot(111)
        self.ax.set_xlim(self.minX, self.maxX)
        self.ax.set_ylim(self.minY, self.maxY)
        self.ax.plot(x, y)
        canvas = FigureCanvasTkAgg(graph, master=RightFrame)
        canvas.show()
        canvas.get_tk_widget().grid(column=2, row=1, rowspan=2, sticky=(N, S, E, W))

my_object = Zoom()

def zoom_init(x, y):
    RightFrame.config(cursor="crosshair")
    my_object.zoom_init(x, y)
# UI Part------------------------------------------------------------------------------------------------------
class Data(object):
    def __init__(self): 
        self.LF_1 = LabelFrame(frame, text="Curve 1 :", padx=5, pady=5)
        self.LF_1.grid(padx=10, pady=10)
        self.LF_hwhm_1 = ttk.Label(self.LF_1, text="HWHM :")
        self.LF_hwhm_1.grid(column=0, row=0, sticky=(N, S, E, W))
        self.LF_hwhm_entry_1 = ttk.Entry(self.LF_1)
        self.LF_hwhm_entry_1.grid(column=1, pady=5, row=0, sticky=(N, S, E, W))
        self.LF_center_1 = ttk.Label(self.LF_1, text="Center :")
        self.LF_center_1.grid(column=0, row=1, sticky=(N, S, E, W))
        self.LF_center_entry_1 = ttk.Entry(self.LF_1)
        self.LF_center_entry_1.grid(column=1, row=1, pady=5, sticky=(N, S, E, W))
        self.LF_intensity_1 = ttk.Label(self.LF_1, text="Intensity :")
        self.LF_intensity_1.grid(column=0, row=2, sticky=(N, S, E, W))
        self.LF_intensity_entry_1 = ttk.Entry(self.LF_1)
        self.LF_intensity_entry_1.grid(column=1, row=2,pady=5, sticky=(N, S, E, W))
        self.LF_2 = LabelFrame(frame, text="Curve 2 :", padx=5, pady=5)
        self.LF_2.grid(padx=10, pady=10)
        self.LF_hwhm_2 = ttk.Label(self.LF_2, text="HWHM :")
        self.LF_hwhm_2.grid(column=0, row=0, sticky=(N, S, E, W))
        self.LF_hwhm_entry_2 = ttk.Entry(self.LF_2)
        self.LF_hwhm_entry_2.grid(column=1, pady=5, row=0, sticky=(N, S, E, W))
        self.LF_center_2 = ttk.Label(self.LF_2, text="Center :")
        self.LF_center_2.grid(column=0, row=1, sticky=(N, S, E, W))
        self.LF_center_entry_2 = ttk.Entry(self.LF_2)
        self.LF_center_entry_2.grid(column=1, row=1, pady=5, sticky=(N, S, E, W))
        self.LF_intensity_2 = ttk.Label(self.LF_2, text="Intensity :")
        self.LF_intensity_2.grid(column=0, row=2, sticky=(N, S, E, W))
        self.LF_intensity_entry_2 = ttk.Entry(self.LF_2)
        self.LF_intensity_entry_2.grid(column=1, row=2,pady=5, sticky=(N, S, E, W))
        self.LF_3 = LabelFrame(frame, text="Curve 3 :", padx=5, pady=5)
        self.LF_3.grid(padx=10, pady=10)
        self.LF_hwhm_3 = ttk.Label(self.LF_3, text="HWHM :")
        self.LF_hwhm_3.grid(column=0, row=0, sticky=(N, S, E, W))
        self.LF_hwhm_entry_3 = ttk.Entry(self.LF_3)
        self.LF_hwhm_entry_3.grid(column=1, pady=5, row=0, sticky=(N, S, E, W))
        self.LF_center_3 = ttk.Label(self.LF_3, text="Center :")
        self.LF_center_3.grid(column=0, row=1, sticky=(N, S, E, W))
        self.LF_center_entry_3 = ttk.Entry(self.LF_3)
        self.LF_center_entry_3.grid(column=1, row=1, pady=5, sticky=(N, S, E, W))
        self.LF_intensity_3 = ttk.Label(self.LF_3, text="Intensity :")
        self.LF_intensity_3.grid(column=0, row=2, sticky=(N, S, E, W))
        self.LF_intensity_entry_3 = ttk.Entry(self.LF_3)
        self.LF_intensity_entry_3.grid(column=1, row=2,pady=5, sticky=(N, S, E, W))
        self.LF_4 = LabelFrame(frame, text="Curve 4 :", padx=5, pady=5)
        self.LF_4.grid(padx=10, pady=10)
        self.LF_hwhm_4 = ttk.Label(self.LF_4, text="HWHM :")
        self.LF_hwhm_4.grid(column=0, row=0, sticky=(N, S, E, W))
        self.LF_hwhm_entry_4 = ttk.Entry(self.LF_4)
        self.LF_hwhm_entry_4.grid(column=1, pady=5, row=0, sticky=(N, S, E, W))
        self.LF_center_4 = ttk.Label(self.LF_4, text="Center :")
        self.LF_center_4.grid(column=0, row=1, sticky=(N, S, E, W))
        self.LF_center_entry_4 = ttk.Entry(self.LF_4)
        self.LF_center_entry_4.grid(column=1, row=1, pady=5, sticky=(N, S, E, W))
        self.LF_intensity_4 = ttk.Label(self.LF_4, text="Intensity :")
        self.LF_intensity_4.grid(column=0, row=2, sticky=(N, S, E, W))
        self.LF_intensity_entry_4 = ttk.Entry(self.LF_4)
        self.LF_intensity_entry_4.grid(column=1, row=2,pady=5, sticky=(N, S, E, W))
        self.LF_5 = LabelFrame(frame, text="Curve 5 :", padx=5, pady=5)
        self.LF_5.grid(padx=10, pady=10)
        self.LF_hwhm_5 = ttk.Label(self.LF_5, text="HWHM :")
        self.LF_hwhm_5.grid(column=0, row=0, sticky=(N, S, E, W))
        self.LF_hwhm_entry_5 = ttk.Entry(self.LF_5)
        self.LF_hwhm_entry_5.grid(column=1, pady=5, row=0, sticky=(N, S, E, W))
        self.LF_center_5 = ttk.Label(self.LF_5, text="Center :")
        self.LF_center_5.grid(column=0, row=1, sticky=(N, S, E, W))
        self.LF_center_entry_5 = ttk.Entry(self.LF_5)
        self.LF_center_entry_5.grid(column=1, row=1, pady=5, sticky=(N, S, E, W))
        self.LF_intensity_5 = ttk.Label(self.LF_5, text="Intensity :")
        self.LF_intensity_5.grid(column=0, row=2, sticky=(N, S, E, W))
        self.LF_intensity_entry_5 = ttk.Entry(self.LF_5)
        self.LF_intensity_entry_5.grid(column=1, row=2,pady=5, sticky=(N, S, E, W))
        self.LF_6 = LabelFrame(frame, text="Curve 6 :", padx=5, pady=5)
        self.LF_6.grid(padx=10, pady=10)
        self.LF_hwhm_6 = ttk.Label(self.LF_6, text="HWHM :")
        self.LF_hwhm_6.grid(column=0, row=0, sticky=(N, S, E, W))
        self.LF_hwhm_entry_6 = ttk.Entry(self.LF_6)
        self.LF_hwhm_entry_6.grid(column=1, pady=5, row=0, sticky=(N, S, E, W))
        self.LF_center_6 = ttk.Label(self.LF_6, text="Center :")
        self.LF_center_6.grid(column=0, row=1, sticky=(N, S, E, W))
        self.LF_center_entry_6 = ttk.Entry(self.LF_6)
        self.LF_center_entry_6.grid(column=1, row=1, pady=5, sticky=(N, S, E, W))
        self.LF_intensity_6 = ttk.Label(self.LF_6, text="Intensity :")
        self.LF_intensity_6.grid(column=0, row=2, sticky=(N, S, E, W))
        self.LF_intensity_entry_6 = ttk.Entry(self.LF_6)
        self.LF_intensity_entry_6.grid(column=1, row=2,pady=5, sticky=(N, S, E, W))
        self.LF_7 = LabelFrame(frame, text="Curve 7 :", padx=5, pady=5)
        self.LF_7.grid(padx=10, pady=10)
        self.LF_hwhm_7 = ttk.Label(self.LF_7, text="HWHM :")
        self.LF_hwhm_7.grid(column=0, row=0, sticky=(N, S, E, W))
        self.LF_hwhm_entry_7 = ttk.Entry(self.LF_7)
        self.LF_hwhm_entry_7.grid(column=1, pady=5, row=0, sticky=(N, S, E, W))
        self.LF_center_7 = ttk.Label(self.LF_7, text="Center :")
        self.LF_center_7.grid(column=0, row=1, sticky=(N, S, E, W))
        self.LF_center_entry_7 = ttk.Entry(self.LF_7)
        self.LF_center_entry_7.grid(column=1, row=1, pady=5, sticky=(N, S, E, W))
        self.LF_intensity_7 = ttk.Label(self.LF_7, text="Intensity :")
        self.LF_intensity_7.grid(column=0, row=2, sticky=(N, S, E, W))
        self.LF_intensity_entry_7 = ttk.Entry(self.LF_7)
        self.LF_intensity_entry_7.grid(column=1, row=2,pady=5, sticky=(N, S, E, W))
        self.LF_8 = LabelFrame(frame, text="Curve 8 :", padx=5, pady=5)
        self.LF_8.grid(padx=10, pady=10)
        self.LF_hwhm_8 = ttk.Label(self.LF_8, text="HWHM :")
        self.LF_hwhm_8.grid(column=0, row=0, sticky=(N, S, E, W))
        self.LF_hwhm_entry_8 = ttk.Entry(self.LF_8)
        self.LF_hwhm_entry_8.grid(column=1, pady=5, row=0, sticky=(N, S, E, W))
        self.LF_center_8 = ttk.Label(self.LF_8, text="Center :")
        self.LF_center_8.grid(column=0, row=1, sticky=(N, S, E, W))
        self.LF_center_entry_8 = ttk.Entry(self.LF_8)
        self.LF_center_entry_8.grid(column=1, row=1, pady=5, sticky=(N, S, E, W))
        self.LF_intensity_8 = ttk.Label(self.LF_8, text="Intensity :")
        self.LF_intensity_8.grid(column=0, row=2, sticky=(N, S, E, W))
        self.LF_intensity_entry_8 = ttk.Entry(self.LF_8)
        self.LF_intensity_entry_8.grid(column=1, row=2,pady=5, sticky=(N, S, E, W))
        self.LF_9 = LabelFrame(frame, text="Curve 9 :", padx=5, pady=5)
        self.LF_9.grid(padx=10, pady=10)
        self.LF_hwhm_9 = ttk.Label(self.LF_9, text="HWHM :")
        self.LF_hwhm_9.grid(column=0, row=0, sticky=(N, S, E, W))
        self.LF_hwhm_entry_9 = ttk.Entry(self.LF_9)
        self.LF_hwhm_entry_9.grid(column=1, pady=5, row=0, sticky=(N, S, E, W))
        self.LF_center_9 = ttk.Label(self.LF_9, text="Center :")
        self.LF_center_9.grid(column=0, row=1, sticky=(N, S, E, W))
        self.LF_center_entry_9 = ttk.Entry(self.LF_9)
        self.LF_center_entry_9.grid(column=1, row=1, pady=5, sticky=(N, S, E, W))
        self.LF_intensity_9 = ttk.Label(self.LF_9, text="Intensity :")
        self.LF_intensity_9.grid(column=0, row=2, sticky=(N, S, E, W))
        self.LF_intensity_entry_9 = ttk.Entry(self.LF_9)
        self.LF_intensity_entry_9.grid(column=1, row=2,pady=5, sticky=(N, S, E, W))
        self.LF_10 = LabelFrame(frame, text="Curve 10 :", padx=5, pady=5)
        self.LF_10.grid(padx=10, pady=10)
        self.LF_hwhm_10 = ttk.Label(self.LF_10, text="HWHM :")
        self.LF_hwhm_10.grid(column=0, row=0, sticky=(N, S, E, W))
        self.LF_hwhm_entry_10 = ttk.Entry(self.LF_10)
        self.LF_hwhm_entry_10.grid(column=1, pady=5, row=0, sticky=(N, S, E, W))
        self.LF_center_10 = ttk.Label(self.LF_10, text="Center :")
        self.LF_center_10.grid(column=0, row=1, sticky=(N, S, E, W))
        self.LF_center_entry_10 = ttk.Entry(self.LF_10)
        self.LF_center_entry_10.grid(column=1, row=1, pady=5, sticky=(N, S, E, W))
        self.LF_intensity_10 = ttk.Label(self.LF_10, text="Intensity :")
        self.LF_intensity_10.grid(column=0, row=2, sticky=(N, S, E, W))
        self.LF_intensity_entry_10 = ttk.Entry(self.LF_10)
        self.LF_intensity_entry_10.grid(column=1, row=2,pady=5, sticky=(N, S, E, W))
        self.LF_11 = LabelFrame(frame, text="Curve 11 :", padx=5, pady=5)
        self.LF_11.grid(padx=10, pady=10)
        self.LF_hwhm_11 = ttk.Label(self.LF_11, text="HWHM :")
        self.LF_hwhm_11.grid(column=0, row=0, sticky=(N, S, E, W))
        self.LF_hwhm_entry_11 = ttk.Entry(self.LF_11)
        self.LF_hwhm_entry_11.grid(column=1, pady=5, row=0, sticky=(N, S, E, W))
        self.LF_center_11 = ttk.Label(self.LF_11, text="Center :")
        self.LF_center_11.grid(column=0, row=1, sticky=(N, S, E, W))
        self.LF_center_entry_11 = ttk.Entry(self.LF_11)
        self.LF_center_entry_11.grid(column=1, row=1, pady=5, sticky=(N, S, E, W))
        self.LF_intensity_11 = ttk.Label(self.LF_11, text="Intensity :")
        self.LF_intensity_11.grid(column=0, row=2, sticky=(N, S, E, W))
        self.LF_intensity_entry_11 = ttk.Entry(self.LF_11)
        self.LF_intensity_entry_11.grid(column=1, row=2,pady=5, sticky=(N, S, E, W))
        
    def fetchdata(self):
        self.curve = []
        self.hwhm_1 = self.LF_hwhm_entry_1.get()
        self.center_1 = self.LF_center_entry_1.get()
        self.intensity_1 = self.LF_intensity_entry_1.get()
        if self.hwhm_1.strip() != '' and self.center_1.strip() != '' and self.intensity_1.strip() != '':
            self.curve.append(float(self.hwhm_1))
            self.curve.append(float(self.center_1))
            self.curve.append(float(self.intensity_1))
        
        self.hwhm_2 = self.LF_hwhm_entry_2.get()
        self.center_2 = self.LF_center_entry_2.get()
        self.intensity_2 = self.LF_intensity_entry_2.get()
        if self.hwhm_2.strip() != '' and self.center_2.strip() != '' and self.intensity_2.strip() != '':
            self.curve.append(float(self.hwhm_2)) 
            self.curve.append(float(self.center_2)) 
            self.curve.append(float(self.intensity_2))

        self.hwhm_3 = self.LF_hwhm_entry_3.get()
        self.center_3 = self.LF_center_entry_3.get()
        self.intensity_3 = self.LF_intensity_entry_3.get()
        if self.hwhm_3.strip() != '' and self.center_3.strip() != '' and self.intensity_3.strip() != '':
            self.curve.append(float(self.hwhm_3))
            self.curve.append(float(self.center_3))
            self.curve.append(float(self.intensity_3))
        
        self.hwhm_4 = self.LF_hwhm_entry_4.get()
        self.center_4 = self.LF_center_entry_4.get()
        self.intensity_4 = self.LF_intensity_entry_4.get()
        if self.hwhm_4.strip() != '' and self.center_4.strip() != '' and self.intensity_4.strip() != '':
            self.curve.append(float(self.hwhm_4))
            self.curve.append(float(self.center_4))
            self.curve.append(float(self.intensity_4))
        
        self.hwhm_5 = self.LF_hwhm_entry_5.get()
        self.center_5 = self.LF_center_entry_5.get()
        self.intensity_5 = self.LF_intensity_entry_5.get()
        if self.hwhm_5.strip() != '' and self.center_5.strip() != '' and self.intensity_5.strip() != '':
            self.curve.append(float(self.hwhm_5))
            self.curve.append(float(self.center_5))
            self.curve.append(float(self.intensity_5))
        
        self.hwhm_6 = self.LF_hwhm_entry_6.get()
        self.center_6 = self.LF_center_entry_6.get()
        self.intensity_6 = self.LF_intensity_entry_6.get()
        if self.hwhm_6.strip() != '' and self.center_6.strip() != '' and self.intensity_6.strip() != '':
            self.curve.append(float(self.hwhm_6))
            self.curve.append(float(self.center_6))
            self.curve.append(float(self.intensity_6))
        
        self.hwhm_7 = self.LF_hwhm_entry_7.get()
        self.center_7 = self.LF_center_entry_7.get()
        self.intensity_7 = self.LF_intensity_entry_7.get()
        if self.hwhm_7.strip() != '' and self.center_7.strip() != '' and self.intensity_7.strip() != '':
            self.curve.append(float(self.hwhm_7))
            self.curve.append(float(self.center_7))
            self.curve.append(float(self.intensity_7))

        self.hwhm_8 = self.LF_hwhm_entry_8.get()
        self.center_8 = self.LF_center_entry_8.get()
        self.intensity_8 = self.LF_intensity_entry_8.get()
        if self.hwhm_8.strip() != '' and self.center_8.strip() != '' and self.intensity_8.strip() != '':
            self.curve.append(float(self.hwhm_8))
            self.curve.append(float(self.center_8))
            self.curve.append(float(self.intensity_8))

        self.hwhm_9 = self.LF_hwhm_entry_9.get()
        self.center_9 = self.LF_center_entry_9.get()
        self.intensity_9 = self.LF_intensity_entry_9.get()
        if self.hwhm_9.strip() != '' and self.center_9.strip() != '' and self.intensity_9.strip() != '':
            self.curve.append(float(self.hwhm_9))
            self.curve.append(float(self.center_9))
            self.curve.append(float(self.intensity_9))

        self.hwhm_10 = self.LF_hwhm_entry_10.get()
        self.center_10 = self.LF_center_entry_10.get()
        self.intensity_10 = self.LF_intensity_entry_10.get()
        if self.hwhm_10.strip() != '' and self.center_10.strip() != '' and self.intensity_10.strip() != '':
            self.curve.append(float(self.hwhm_10))
            self.curve.append(float(self.center_10))
            self.curve.append(float(self.intensity_10)) 

        self.hwhm_11 = self.LF_hwhm_entry_11.get()
        self.center_11 = self.LF_center_entry_11.get()
        self.intensity_11 = self.LF_intensity_entry_11.get()
        if self.hwhm_11.strip() != '' and self.center_11.strip() != '' and self.intensity_11.strip() != '':
            self.curve.append(float(self.hwhm_11))
            self.curve.append(float(self.center_11))
            self.curve.append(float(self.intensity_11))
        fit_curve(self.curve)
        
        
def myfunction(event):
    LF_canvas.configure(scrollregion=LF_canvas.bbox("all"),width=220,height=600)

LeftFrame = ttk.Frame(content, borderwidth=5, relief="groove", width=220, height=600)
nb = ttk.Notebook(LeftFrame)
nb.grid(sticky=(N, S, E, W))

# create a child frame for each page
f1 = Frame(height=600, width=220)
f2 = Frame(height=600, width=220)

# create the pages
nb.add(f1, text='  Curve Fitting  ')
nb.add(f2, text='  Data Plotting  ')

myframe=Frame(f1,relief=GROOVE,height=600,width=220,bd=1)
myframe.grid(column=0,row=0, columnspan=2, sticky=(N, S, E, W))

text = Text(f2, height=40, width=30, padx=5, pady=5)
scroll = Scrollbar(f2, command=text.yview)
text.configure(yscrollcommand=scroll.set)

LF_canvas=Canvas(myframe)
frame=Frame(LF_canvas)
myscrollbar=Scrollbar(myframe,orient="vertical",command=LF_canvas.yview)
LF_canvas.configure(yscrollcommand=myscrollbar.set)

myscrollbar.grid(column=1,row=0,sticky=(N, S, E, W))
LF_canvas.grid(column=0, row=0)
LF_canvas.create_window((0,0),window=frame,anchor='nw')
frame.bind("<Configure>",myfunction)
    
mish = Data()

# Backend------------------------------------------------------------------------
RightFrame = ttk.Frame(content, borderwidth=5, relief="groove", width=750)
def dataReducer(data, reductionlevel):
    #Checks to see if amount of data is divisible by the reducion level. If not then this method will not work
    if len(data) % reductionlevel != 0:
        print("This won't work. The reduction level doesn't match the amount of points.")
        return
    p = 0
    q = reductionlevel
    new = []
    for i in range(0,len(data)//reductionlevel):
        new.append(np.sum(data[p:q]))
        p+=reductionlevel
        q+=reductionlevel
    out=np.array(new)
    return out
#This function takes the data and performs folding to remove a parabolic baseline.
def dataFolder(data, foldingpoint):
    newfold = []
    for i in range(0,len(data)//2):
        newfold.append(data[i]+data[len(data)-i-1])
    return newfold
#This function coverts the X axis to velocity and returns the new values.
def dataVelocity(data,zeroPoint,rate):
    pos = []
    neg = []
    for i in range(zeroPoint,len(data)):
        pos.append((i-zeroPoint)*rate)
    for i in range(-zeroPoint,0):
        neg.append((i)*rate)
    newVelocitycityMatrix = np.append(neg,pos)
    return newVelocitycityMatrix
#This function is wrapper for plotting.  
def mossplot(datain,xval,title="Mossbauer Spectrum",xaxis="Velocity (mm/s)",yaxis="Counts"):
    fig = ax.plot(xval,datain)
    ax.grid(True)
    ax.legend()
    ax.title(title)
    ax.xlabel(xaxis)
    ax.ylabel(yaxis)
    ax.xlim(min(xval),max(xval))
    return
#This function calculates Doppler effect from velocity as an input and resonance energy
def dopplerEffect (velocity,resonanceEnergy):
    c=2.997924588E8
    eDoppler= (1+velocity)*resonanceEnergy/c
    return eDoppler
#This function calculates effective mossbauer thickness -- not to be implemented for a long time
def effectiveThickness (LMfactor,cross,abundance,density,thickness,molarmass):
    N=6.022E23
    result= LMfactor*N*abundance*density*thickness/molarmass
#The parameters for Lorentzian fits.
def lorentzian(x,hwhm,cent,intense,back=0):
    numerator =  (hwhm**2 )
    denominator = ( x - (cent) )**2 + hwhm**2
    y = intense*(numerator/denominator)+back
    return y
#Residual function for fitting.
def residuals(p,y,x):
    err = y - lorentzian(x,p)
    return err
#Residual function for fitting multiple curves.
def multipleResiduals(p,x,yval):
    parin= np.zeros(len(x))
    for i in range(0,len(p),3):
        p0=p[i]
        p1=p[i+1]
        p2=p[i+2]
        if p0>0.5 or p0<0: return 1E8
        if p2>-10: return 1E8
        parin=np.add(parin,lorentzian(x,p0,p1,p2))
    err = yval - parin
    return err
#END SECTION: Functions
#Input parameters ideally not hard coded, but for testing and dev they will be.
filename = "TPNIOF14forwmoss.dat" #Test Data Path - Go Through GUI
data = []
data = pylab.loadtxt(filename)
redNumber=4
channels=1024
midpoint= 512//redNumber
passionbeat="fit"
#End input parameters
data = dataFolder(data,channels)
new = dataReducer(data,redNumber)
newVelocity = dataVelocity(new,midpoint,16/channels*redNumber)
ind_bg_low = (newVelocity > min(newVelocity)) & (newVelocity < -3)
ind_bg_high = (newVelocity > +3) & (newVelocity < max(newVelocity))
x_bg = np.concatenate((newVelocity[ind_bg_low],newVelocity[ind_bg_high]))
y_bg = np.concatenate((new[ind_bg_low],new[ind_bg_high]))
ind_bg_mid=(newVelocity > -8) & (newVelocity < 8)
m, c = np.polyfit(x_bg, y_bg, 1)
background = m*newVelocity + c
y_bg_corr = new - background
#These are the test values for parameters to be fitted.
#It should be able to accept an unlimited number.
#It is set for 12 sets of parameters. It needs to be able to do 1,2,5,6,12
def fit_curve(input_data):
    p = input_data
    global graph, canvas, ax, passionbeat
    passionbeat="fit"
    nb.select(0)
    graph = Figure(figsize=(5,4), dpi=150)
    ax = graph.add_subplot(111)
    #p = [0.34,-0.2,-800,0.34,-0.15,-750,0.34,0.11,-500,0.34,-0.25,-888,0.34,-0.2,-800,0.34,-0.15,-750,0.34,0.11,-500,0.34,-0.25,-888,0.34,-0.2,-800,0.34,-0.15,-750,0.34,0.11,-500,0.34,-0.25,-888]  # [hwhm, peak center, intensity] #
    pBest = scipy.optimize.leastsq(multipleResiduals,p,args=(newVelocity[ind_bg_mid],y_bg_corr[ind_bg_mid]),full_output=1)
    fitsum=np.zeros(len(newVelocity))
    for i in range(0,len(pBest[0][:]),3):
        fit = lorentzian(newVelocity,pBest[0][i],pBest[0][i+1],pBest[0][i+2],background)
        fitsum= np.add(fitsum,lorentzian(newVelocity,pBest[0][i],pBest[0][i+1],pBest[0][i+2]))
        ax.plot(newVelocity,fit,'r-',lw=2, label=i)
        plt.plot(newVelocity,fit,'r-',lw=2, label=i)
    fitsum=np.add(fitsum,background)
    plt.plot(newVelocity,new,'b-')
    plt.plot(newVelocity,fitsum,'g-',lw=5)
    plt.legend()
    ax.plot(newVelocity,new,'b-')
    ax.plot(newVelocity,fitsum,'g-',lw=5)
    ax.set_xlabel('Channels', fontsize=8)
    ax.set_ylabel('Intensity', fontsize=8)
    ax.tick_params(axis='both', which='major', labelsize=8)
    ax.tick_params(axis='both', which='minor', labelsize=8)
    ax.legend(fontsize=8)
    canvas = FigureCanvasTkAgg(graph, master=RightFrame)
    canvas.show()
    canvas.get_tk_widget().grid(column=2, row=0, rowspan=2, sticky=(N, S, E, W))

canvas = FigureCanvasTkAgg(graph, master=RightFrame)
canvas.show()
canvas.get_tk_widget().grid(column=2, row=0, rowspan=2, sticky=(N, S, E, W))

def openfilename():
   filename = FileDialog.askopenfilename(parent=root, defaultextension=".csv", filetypes=(("Comma Separated Values", "*.csv"),("All Files", "*.*") ))
   if filename is None:
       return
   f = open(filename)
   text.delete(0.0, END)
   text.insert(END, f.read())
   nb.select(1)

def saveimage():
    f = FileDialog.asksaveasfile(defaultextension=".png", filetypes=(("Image file", "*.png"),("All Files", "*.*") ))
    if f is None:
        return
    if passionbeat is "fit":
        nb.select(0)
        fig1 = plt.gcf()
        fig1.savefig(f, dpi=100)
        
    elif passionbeat is "plot":
        nb.select(1)
        ax = plt.gca()
        ax.set_xlim(minX, maxX)
        ax.set_ylim(minY, maxY)
        china = ax.legend()
        if china is not None:
            ax.legend().set_visible(False)
        
        plt.plot(x, y)
        plt.savefig(f, dpi=100)
        plt.clf()
        plt.close('all')
    
    f.close()
    
def close():
    root.destroy()
   
def donothing():
    print("Hello World")

def plotgraph():
    global x, y, passionbeat, minX, maxX, minY, maxY
    x = []
    y = []
    passionbeat="plot"
    nb.select(1)
    data = text.get("1.0", END)
    sepFile = data.split('\n')
    
    for plotPair in sepFile:
        xAndY = plotPair.split(',')
        if len(xAndY[0]) != 0 and len(xAndY[1]) != 0:
            x.append(float(xAndY[0]))
            y.append(float(xAndY[1]))

    minX=min(x)
    maxX=max(x)
    minY=min(y)
    maxY=max(y)
    graph = Figure(figsize=(5,4), dpi=100)
    a = graph.add_subplot(111)
    a.plot(x,y)
    a.set_xlabel('Channels')
    a.set_ylabel('Intensity')
    canvas = FigureCanvasTkAgg(graph, master=RightFrame)
    canvas.show()
    canvas.get_tk_widget().grid(column=2, row=1, rowspan=2, sticky=(N, S, E, W))

def zoom_out():
    RightFrame.config(cursor="arrow")
# Tooltip function ------------------------------------------------------------------------------------------
class ToolTipManager:
    label = None
    window = None
    active = 0

    def __init__(self):
        self.tag = None

    def getcontroller(self, widget):
        if self.tag is None:

            self.tag = "ui_tooltip_%d" % id(self)
            widget.bind_class(self.tag, "<Enter>", self.enter)
            widget.bind_class(self.tag, "<Leave>", self.leave)

            # pick suitable colors for tooltips
            try:
                self.bg = "systeminfobackground"
                self.fg = "systeminfotext"
                widget.winfo_rgb(self.fg) # make sure system colors exist
                widget.winfo_rgb(self.bg)
            except:
                self.bg = "#ffffe0"
                self.fg = "black"

        return self.tag

    def register(self, widget, text):
        widget.ui_tooltip_text = text
        tags = list(widget.bindtags())
        tags.append(self.getcontroller(widget))
        widget.bindtags(tuple(tags))

    def unregister(self, widget):
        tags = list(widget.bindtags())
        tags.remove(self.getcontroller(widget))
        widget.bindtags(tuple(tags))

    # event handlers

    def enter(self, event):
        widget = event.widget
        if not self.label:
            # create and hide balloon help window
            self.popup = Toplevel(bg=self.fg, bd=1)
            self.popup.overrideredirect(1)
            self.popup.withdraw()
            self.label = Label(
                self.popup, fg=self.fg, bg=self.bg, bd=0, padx=2
                )
            self.label.pack()
            self.active = 0
        self.xy = event.x_root + 16, event.y_root + 10
        self.event_xy = event.x, event.y
        self.after_id = widget.after(200, self.display, widget)

    def display(self, widget):
        if not self.active:
            # display balloon help window
            text = widget.ui_tooltip_text
            if callable(text):
                text = text(widget, self.event_xy)
            self.label.config(text=text)
            self.popup.deiconify()
            self.popup.lift()
            self.popup.geometry("+%d+%d" % self.xy)
            self.active = 1
            self.after_id = None

    def leave(self, event):
        widget = event.widget
        if self.active:
            self.popup.withdraw()
            self.active = 0
        if self.after_id:
            widget.after_cancel(self.after_id)
            self.after_id = None

_manager = ToolTipManager()

def register(widget, text):
    _manager.register(widget, text)

# Menubar ---------------------------------------------------------------------------------------------------
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=openfilename)
filemenu.add_command(label="Save Image", command=saveimage)
filemenu.add_command(label="Close", command=close)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=close)

menubar.add_cascade(label="File", menu=filemenu)
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", command=donothing)

editmenu.add_separator()

editmenu.add_command(label="Cut", command=donothing)
editmenu.add_command(label="Copy", command=donothing)
editmenu.add_command(label="Paste", command=donothing)
editmenu.add_command(label="Delete", command=donothing)
editmenu.add_command(label="Select All", command=donothing)

menubar.add_cascade(label="Edit", menu=editmenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)
root.config(menu=menubar)

# Toolbar
toolbar = ttk.Frame(content, borderwidth=5, relief="groove")
open_icon = Image.open("open.png")
open_img = ImageTk.PhotoImage(open_icon)
a = Button(toolbar, image=open_img, relief=FLAT, justify=LEFT, command=openfilename)
a.image = open_img

save_icon = Image.open("save.png")
save_img = ImageTk.PhotoImage(save_icon)
b = Button(toolbar, image=save_img, relief=FLAT, justify=LEFT, command=saveimage)
b.image = save_img

zoom_in_icon = Image.open("zoom_in.png")
zoom_in_img = ImageTk.PhotoImage(zoom_in_icon)
c = Button(toolbar, image=zoom_in_img, relief=FLAT, justify=LEFT, command=lambda: zoom_init(x, y))
c.image = zoom_in_img

zoom_out_icon = Image.open("zoom_out.png")
zoom_out_img = ImageTk.PhotoImage(zoom_out_icon)
d = Button(toolbar, image=zoom_out_img, relief=FLAT, justify=LEFT, command=zoom_out)
d.image = zoom_out_img

fit_curve_icon = Image.open("fit_curve.png")
fit_curve_img = ImageTk.PhotoImage(fit_curve_icon)
e = Button(toolbar, image=fit_curve_img, relief=FLAT, justify=LEFT, command=lambda: mish.fetchdata())
e.image = fit_curve_img

plot_icon = Image.open("plot_icon.png")
plot_icon_img = ImageTk.PhotoImage(plot_icon)
f = Button(toolbar, image=plot_icon_img, relief=FLAT, justify=LEFT, command=plotgraph)
f.image = plot_icon_img

register(a, "Open")
register(b, "Save Image")
register(c, "Zoom in (Only available for Data Plotting)")
register(d, "Zoom out (Only available for Data Plotting)")
register(e, "Fit Curve")
register(f, "PLot")
register(text, "Open or Paste a .csv file and click Plot")

content.grid(column=0, row=0, sticky=(N, S, E, W))
toolbar.grid(column=0, row=0, columnspan=5, sticky=(N, S, E, W))
a.grid(column=0, row=0, padx=5, sticky=W)
b.grid(column=1, row=0, padx=5, sticky=W)
c.grid(column=2, row=0, padx=5, sticky=W)
d.grid(column=3, row=0, padx=5, sticky=W)
e.grid(column=4, row=0, padx=5, sticky=W)
f.grid(column=5, row=0, padx=5, sticky=W)
LeftFrame.grid(column=0, row=1, rowspan=2, sticky=(N, S, E, W))
RightFrame.grid(column=2, row=1, rowspan=2, sticky=(N, S, E, W))
text.grid(column=0, row=1, sticky=(N, S, E, W))
scroll.grid(column=1, row=1, sticky=(N, S, E, W))


root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=0)
content.columnconfigure(1, weight=0)
content.columnconfigure(2, weight=3)
content.rowconfigure(0, weight=0)
content.rowconfigure(1, weight=1)
LeftFrame.columnconfigure(0, weight=0)
LeftFrame.columnconfigure(1, weight=0)
LeftFrame.rowconfigure(1, weight=1)
RightFrame.columnconfigure(2, weight=3)
RightFrame.rowconfigure(1, weight=1)
nb.rowconfigure(1, weight=1)
f1.rowconfigure(1, weight=1)
text.columnconfigure(0, weight=1)
scroll.columnconfigure(1, weight=0)

root.state("zoomed")
root.mainloop()
