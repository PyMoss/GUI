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

# Functions
def openfilename():
   filename = FileDialog.askopenfilename(parent=root)
   f = open(filename)
   text.insert(END, f.read())

def saveasfilename():
    FileDialog.asksaveasfilename()
    
def close():
   root.destroy()
   
def donothing():
    print "Hello World"

def createToolTip( widget, text ):
    def enter( event ):
        global tipwindow
        x = y = 0
        if tipwindow or not text:
            return
        x, y, cx, cy = widget.bbox("insert")
        x += widget.winfo_rootx() + 27
        y += widget.winfo_rooty() + 27
        # Creates a toplevel window
        tipwindow = tw = Toplevel(widget)
        # Leaves only the label and removes the app window
        tw.wm_overrideredirect( 1 )
        tw.wm_geometry( "+%d+%d" % ( x, y ) )
        label = Label( tw, text = text, justify = LEFT,
                       background = "#ffffe0", relief = SOLID, borderwidth = 1,
                       font = ( "tahoma", "8", "normal" ) )
        label.grid(ipadx=5)
        
    def close( event ):
        global tipwindow
        tw = tipwindow
        tipwindow = None
        if tw:
            tw.destroy()
            
        widget.bind( "<Enter>", enter )
        widget.bind( "<Leave>", close )

def do_popup(event):
    try:
        contextMenu.tk_popup(event.x_root, event.y_root, 0)
    finally:
        contextMenu.grab_release()
    
# Menubar
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=openfilename)
filemenu.add_command(label="Save", command=saveasfilename)
filemenu.add_command(label="Save as...", command=saveasfilename)
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
b = Button(toolbar, image=save_img, relief=FLAT, justify=LEFT, command=donothing)
b.image = save_img
b.grid()

save_as_icon = Image.open("save_as.png")
save_as_img = ImageTk.PhotoImage(save_as_icon)
c = Button(toolbar, image=save_as_img, relief=FLAT, justify=LEFT, command=donothing)
c.image = save_as_img
c.grid()

zoom_in_icon = Image.open("zoom_in.png")
zoom_in_img = ImageTk.PhotoImage(zoom_in_icon)
d = Button(toolbar, image=zoom_in_img, relief=FLAT, justify=LEFT, command=donothing)
d.image = zoom_in_img
d.grid()

zoom_out_icon = Image.open("zoom_out.png")
zoom_out_img = ImageTk.PhotoImage(zoom_out_icon)
e = Button(toolbar, image=zoom_out_img, relief=FLAT, justify=LEFT, command=donothing)
e.image = zoom_out_img
e.grid()

tipwindow = None
createToolTip(a, "Open file")    
createToolTip(b, "Save file")
createToolTip(c, "Save As..")
createToolTip(d, "Zoom In")
createToolTip(e, "Zoom Out")


content.grid(column=0, row=0, sticky=(N, S, E, W))
toolbar.grid(column=0, row=0, columnspan=5, sticky=(N, S, E, W))
a.grid(column=0, row=0, padx=5, sticky=W)
b.grid(column=1, row=0, padx=5, sticky=W)
c.grid(column=2, row=0, padx=5, sticky=W)
d.grid(column=3, row=0, padx=5, sticky=W)
e.grid(column=4, row=0, padx=5, sticky=W)


# LeftFrame
LeftFrame = ttk.Frame(content, borderwidth=5, relief="groove", width=150, height=500)


namelbl = ttk.Label(LeftFrame, text="Recent files", font=bold)
namelbl['font'] = bold

text = Text(LeftFrame, height=40, width=20, padx=5, pady=5)
text.bind("<Button-3>", do_popup)
scroll = Scrollbar(LeftFrame, command=text.yview)
text.configure(yscrollcommand=scroll.set)

ok = ttk.Button(LeftFrame, text="Okay")
cancel = ttk.Button(LeftFrame, text="Cancel")
name = ttk.Entry(LeftFrame)


# RightFrame
RightFrame = ttk.Frame(content, borderwidth=5, relief="groove", width=750)

#Graph
graph = Figure(figsize=(5,4), dpi=100)
graph_subplot = graph.add_subplot(111)
graph_t = arange(0.0,3.0,0.01)
graph_sin = sin(2*pi*graph_t)
graph_subplot.plot(graph_t,graph_sin)

onevar = BooleanVar()
twovar = BooleanVar()
threevar = BooleanVar()

onevar.set(True)
twovar.set(False)
threevar.set(True)

one = ttk.Checkbutton(content, text="One", variable=onevar, onvalue=True)
two = ttk.Checkbutton(content, text="Two", variable=twovar, onvalue=True)
three = ttk.Checkbutton(content, text="Three", variable=threevar, onvalue=True)

# Geometry
LeftFrame.grid(column=0, row=1, rowspan=2, sticky=(N, S, E, W))
RightFrame.grid(column=1, row=1, columnspan=3, rowspan=2, sticky=(N, S, E, W))
namelbl.grid(column=0, row=1, sticky=(N, S, E, W), padx=5)
one.grid(column=1, row=3)
two.grid(column=2, row=3)
three.grid(column=3, row=3)
text.grid(column=0, row=2, sticky=(N, S, E, W))
scroll.grid(column=1, row=2, sticky=(N, S, E, W))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=1)
LeftFrame.columnconfigure(0, weight=1)
LeftFrame.columnconfigure(1, weight=0)
content.columnconfigure(1, weight=1)
content.columnconfigure(2, weight=1)
content.columnconfigure(3, weight=1)
content.rowconfigure(1, weight=1)

root.state("zoomed")

root.mainloop()
