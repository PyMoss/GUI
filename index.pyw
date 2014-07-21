from tkinter import *
import ttk
import tkFileDialog as FileDialog
from PIL import Image, ImageTk
import tkFont
try:
    # for Python2
    from Tkinter import *
    import ttk as ttk
    import FileDialog as FileDialog
except ImportError:
    # for Python3
    from tkinter import *
    import tkinter.ttk as ttk
    import tkinter.filedialog as FileDialog


root = Tk()
root.wm_iconbitmap("favicon.ico")
root.title("PyMoss")
root.geometry("800x600+10+10")

# Main Container
content = ttk.Frame(root)
bold = tkFont.Font(family='Helvetica', weight='bold')

# ContextMenu
contextMenu = Menu(root, tearoff=0)
contextMenu.add_command(label="Plot") # , command=next) etc...
contextMenu.add_command(label="Cut")
contextMenu.add_command(label="Copy")

# Toolbar Functions -----------------------------------------------------------------------------------------

def include(filename):
    if os.path.exists(filename): 
        execfile(filename)

def openfilename():
   filename = FileDialog.askopenfilename(parent=root)
   f = open(filename)
   text.insert(END, f.read())

def saveimage():
    graph = Figure(figsize=(5,4), dpi=100)
    ax = gca()
    ax.set_xlim(minX, maxX)
    ax.set_ylim(minY, maxY)
#    ax = graph.add_subplot(111)
    plt.plot(x, y)
    plt.savefig("checking.png")
    plt.clf()
    plt.close('all')
    
def close():
    root.destroy()
   
def donothing():
    print "Hello World"

def plotgraph():
    global x
    global y
    x = []
    y = []
    data = text.get("1.0", END)
    sepFile = data.split('\n')
    
    for plotPair in sepFile:
        xAndY = plotPair.split(',')
        if len(xAndY[0]) != 0 and len(xAndY[1]) != 0:
            x.append(float(xAndY[0]))
            y.append(float(xAndY[1]))
#    print x
#    print y
    graph = Figure(figsize=(5,4), dpi=100)
    a = graph.add_subplot(111)
    a.plot(x,y)
#   a.set_title('Tk embedding')
    a.set_xlabel('Velocity')
    a.set_ylabel('Absorbance')
    canvas = FigureCanvasTkAgg(graph, master=RightFrame)
    canvas.show()
    canvas.get_tk_widget().grid(column=2, row=1, rowspan=2, sticky=(N, S, E, W))

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
    
def do_popup(event):
    try:
        contextMenu.tk_popup(event.x_root, event.y_root, 0)
    finally:
        contextMenu.grab_release()

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
        print x
        print y
        canvas.get_tk_widget().grid(column=2, row=1, rowspan=2, sticky=(N, S, E, W))
        self.aid = graph.canvas.mpl_connect('button_press_event', self.on_press)
        self.bid = graph.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid = graph.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        self.is_pressed = True
        if event.xdata is not None and event.ydata is not None:
            self.x0, self.y0 = event.xdata, event.ydata
            print 'press:', self.x0, self.y0
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
                print 'rect:', self.x0, self.y0, self.x1, self.y1, (self.x1-self.x0), (self.y1-self.y0)

    def on_release(self, event):
        self.is_pressed = False
        print 'release:', event.xdata, event.ydata

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
                print 'x0>x1 & y0>y1'
            else:
                self.minX = self.x1
                self.maxX = self.x0
                self.minY = self.y0
                self.maxY = self.y1
                print 'x0>x1 & y0<y1'
        
        if self.x0 < self.x1:
            if self.y0 < self.y1:
                self.minX = self.x0
                self.maxX = self.x1
                self.minY = self.y0
                self.maxY = self.y1
                print 'x0<x1 & y0<y1'
            else:
                self.minX = self.x0
                self.maxX = self.x1
                self.minY = self.y1
                self.maxY = self.y0
                print 'x0<x1 & y0>y1'
            
        global minX
        global minY
        global maxX
        global maxY
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
a.grid()

save_icon = Image.open("save.png")
save_img = ImageTk.PhotoImage(save_icon)
b = Button(toolbar, image=save_img, relief=FLAT, justify=LEFT, command=saveimage)
b.image = save_img
b.grid()

zoom_in_icon = Image.open("zoom_in.png")
zoom_in_img = ImageTk.PhotoImage(zoom_in_icon)
d = Button(toolbar, image=zoom_in_img, relief=FLAT, justify=LEFT, command=lambda: zoom_init(x, y))
d.image = zoom_in_img
d.grid()

zoom_out_icon = Image.open("zoom_out.png")
zoom_out_img = ImageTk.PhotoImage(zoom_out_icon)
e = Button(toolbar, image=zoom_out_img, relief=FLAT, justify=LEFT, command=donothing)
e.image = zoom_out_img
e.grid()

plot_icon = Image.open("plot_icon.png")
plot_icon_img = ImageTk.PhotoImage(plot_icon)
f = Button(toolbar, image=plot_icon_img, relief=FLAT, justify=LEFT, command=plotgraph)
f.image = plot_icon_img
f.grid()

register(a, "Open")
register(b, "Save Image")
register(d, "Zoom in")
register(e, "Zoom out")
register(f, "PLot")

content.grid(column=0, row=0, sticky=(N, S, E, W))
toolbar.grid(column=0, row=0, columnspan=5, sticky=(N, S, E, W))
a.grid(column=0, row=0, padx=5, sticky=W)
b.grid(column=1, row=0, padx=5, sticky=W)
d.grid(column=3, row=0, padx=5, sticky=W)
e.grid(column=4, row=0, padx=5, sticky=W)
f.grid(column=5, row=0, padx=5, sticky=W)
# LeftFrame
LeftFrame = ttk.Frame(content, borderwidth=5, relief="groove", width=200, height=500)

namelbl = ttk.Label(LeftFrame, text="Recent files", font=bold)
namelbl['font'] = bold

text = Text(LeftFrame, height=40, width=10, padx=5, pady=5)
text.bind("<Button-3>", do_popup)
scroll = Scrollbar(LeftFrame, command=text.yview)
text.configure(yscrollcommand=scroll.set)

ok = ttk.Button(LeftFrame, text="Okay")
cancel = ttk.Button(LeftFrame, text="Cancel")
name = ttk.Entry(LeftFrame)


# RightFrame -----------------------------------------------------------------------------------------------
RightFrame = ttk.Frame(content, borderwidth=5, relief="groove", width=750)

#Graph --------------------------------------------------------------------------------------------------
graph = Figure(figsize=(5,4), dpi=100)
a = graph.add_subplot(111)
a.plot([0],[0])
#   a.set_title('Tk embedding')
a.set_xlabel('Velocity')
a.set_ylabel('Absorbance')
canvas = FigureCanvasTkAgg(graph, master=RightFrame)
canvas.show()
canvas.get_tk_widget().grid(column=2, row=1, rowspan=2, sticky=(N, S, E, W))

# Geometry
LeftFrame.grid(column=0, row=1, rowspan=2, sticky=(N, S, E, W))
RightFrame.grid(column=2, row=1, rowspan=2, sticky=(N, S, E, W))
namelbl.grid(column=0, row=1, sticky=(N, S, E, W), padx=5)
text.grid(column=0, row=2, sticky=(N, S, E, W))
scroll.grid(column=1, row=2, sticky=(N, S, E, W))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=1)
LeftFrame.columnconfigure(0, weight=1)
LeftFrame.columnconfigure(1, weight=0)
RightFrame.grid_columnconfigure(2, weight=3)
RightFrame.grid_rowconfigure(2, weight=1)
content.columnconfigure(2, weight=3)
content.rowconfigure(1, weight=1)

root.state("zoomed")

root.mainloop()
