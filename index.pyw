from tkinter import *
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

#from Tkinter import FileDialog

root = Tk()
root.wm_iconbitmap("favicon.ico")
root.title("PyMoss")
root.geometry("800x600+10+10")

content = ttk.Frame(root)
toolbar = ttk.Frame(content, borderwidth=5, relief="groove")
LeftFrame = ttk.Frame(content, borderwidth=5, relief="groove", width=50, height=500)
RightFrame = ttk.Frame(content, borderwidth=5, relief="groove", width=400, height=100)
namelbl = ttk.Label(LeftFrame, text="Name") #Textbox_label
menubar = Menu(root) #Menubar
name = ttk.Entry(LeftFrame) #Textbox

def openfilename():
    filename = FileDialog.askopenfilename(filetypes=[("ASCII Files","*.csv"),("All Files", "*")])
    print filename
    f = open(filename)
    #print f.read()
    Label(RightFrame, text=filename).pack()

def saveasfilename():
    FileDialog.asksaveasfilename()
    
def close():
   root.destroy()
   
def donothing():
    print "Hello World"

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

open = Image.open("open.png")
open_img = ImageTk.PhotoImage(open)
a = Button(toolbar, image=open_img, relief=FLAT, justify=LEFT, command=donothing)
a.image = open_img
a.grid()

save = Image.open("save.png")
save_img = ImageTk.PhotoImage(save)
b = Button(toolbar, image=save_img, relief=FLAT, justify=LEFT, command=donothing)
b.image = save_img
b.grid()

save_as = Image.open("save_as.png")
save_as_img = ImageTk.PhotoImage(save_as)
c = Button(toolbar, image=save_as_img, relief=FLAT, justify=LEFT, command=donothing)
c.image = save_as_img
c.grid()

zoom_in = Image.open("zoom_in.png")
zoom_in_img = ImageTk.PhotoImage(zoom_in)
d = Button(toolbar, image=zoom_in_img, relief=FLAT, justify=LEFT, command=donothing)
d.image = zoom_in_img
d.grid()

zoom_out = Image.open("zoom_out.png")
zoom_out_img = ImageTk.PhotoImage(zoom_out)
e = Button(toolbar, image=zoom_out_img, relief=FLAT, justify=LEFT, command=donothing)
e.image = zoom_out_img
e.grid()

onevar = BooleanVar()
twovar = BooleanVar()
threevar = BooleanVar()

onevar.set(True)
twovar.set(False)
threevar.set(True)

one = ttk.Checkbutton(content, text="One", variable=onevar, onvalue=True)
two = ttk.Checkbutton(content, text="Two", variable=twovar, onvalue=True)
three = ttk.Checkbutton(content, text="Three", variable=threevar, onvalue=True)
ok = ttk.Button(LeftFrame, text="Okay")
cancel = ttk.Button(LeftFrame, text="Cancel")

content.grid(column=0, row=0, sticky=(N, S, E, W))
toolbar.grid(column=0, row=0, columnspan=5, sticky=(N, S, E, W))
a.grid(column=0, row=0, padx=5, sticky=W)
b.grid(column=1, row=0, padx=5, sticky=W)
c.grid(column=2, row=0, padx=5, sticky=W)
d.grid(column=3, row=0, padx=5, sticky=W)
e.grid(column=4, row=0, padx=5, sticky=W)

# Tooltip
tipwindow = None

# Creates a tooptip box for a widget.
def createToolTip( widget, text ):
    def enter( event ):
        global tipwindow
        x = y = 0
        if tipwindow or not text:
            return
        x, y, cx, cy = widget.bbox( "insert" )
        x += widget.winfo_rootx() + 27
        y += widget.winfo_rooty() + 27
        # Creates a toplevel window
        tipwindow = tw = Toplevel( widget )
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

createToolTip(a, "Open file")    
createToolTip(b, "Save file")
createToolTip(c, "Save As..")
createToolTip(d, "Zoom In")
createToolTip(e, "Zoom Out")


LeftFrame.grid(column=0, row=1, columnspan=2, rowspan=2, sticky=(N, S, E, W))
RightFrame.grid(column=2, row=1, columnspan=3, rowspan=2, sticky=(N, S, E, W))
namelbl.grid(column=0, row=1, sticky=(N, W), padx=5)
name.grid(column=1, row=1, sticky=(N, E, W), pady=5, padx=5)
one.grid(column=2, row=3)
two.grid(column=3, row=3)
three.grid(column=4, row=3)
ok.grid(column=0, row=3)
cancel.grid(column=1, row=3)

#frame.Label(root, text=openfilename(filecontent))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=1)
content.columnconfigure(1, weight=1)
content.columnconfigure(2, weight=4)
content.columnconfigure(3, weight=4)
content.columnconfigure(4, weight=4)
content.rowconfigure(1, weight=1)

root.state("zoomed")

root.mainloop()

