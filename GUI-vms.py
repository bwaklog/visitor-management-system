from tkinter import simpledialog, messagebox
from tkinter import *
import tkinter as tk
from unicodedata import name
from PIL import Image, ImageTk

import database as db

root = tk.Tk()


def vwhis():
    for i in root.winfo_children():
        i.destroy()

def home():
    tkinter.messagebox.showinfo("Rec", "Rec added")
    for i in root.winfo_children():
        i.destroy()
    homeScr()

def rem():
    pass



def vw_his():
    pass


def newVis():
    root.deiconify()
    vwhis()
    app_title = Label(root, text='VMS', font=('JetBrains Mono',40))
    # app_title.config(background='white')
    app_title.grid(row=0, column=1, pady=20, padx=0)

    name = tk.Label(root, text='Name :').grid(row=1, column=1, padx=20)
    vname = tk.Entry(root).grid(row=1, column=2, padx=20)
    house = tk.Label(root, text='House :').grid(row=2, column=1, padx=20)
    vhouse = tk.Entry(root).grid(row=2, column=2, padx=20)
    reason = tk.Label(root, text='Reason :').grid(row=3, column=1, padx=20)
    vreason = tk.Entry(root).grid(row=3, column=2, padx=20)

    def activator():
        if enter['state'] == tk.DISABLED:
            enter['state'] = tk.NORMAL
        else:
            enter['state'] = tk.DISABLED

    chk = Label(root, text='Confirm Entry?').grid(row=4, column=1, padx=20)
    chk_btn = Checkbutton(root, command=activator).grid(row=4, column=2)
    
    def new_vis():
        db.add_visi(name=vname.get(), house_no=vhouse.get(), reason=vreason.get(), chk_ins=1, accreg=1 ,aptname=aptselect)
        home()

    enter = tk.Button(root, text='Confirm', command=new_vis, state=DISABLED)
    enter.grid(row=5, ipady=5, columnspan=3, sticky='NSWE', padx=5, pady=5)

    qut = tk.Button(root, text='Quit', command=root.destroy)
    qut.grid(row=6, ipady=5, columnspan=3, sticky='NSWE', padx=5, pady=5)


def remVis():
    root.deiconify()
    vwhis()
    for i in root.winfo_children():
        i.destroy()
    app_title = Label(root, text='VMS', font=('JetBrains Mono', 40))
    # app_title.config(background='white')
    app_title.grid(row=0, column=0, pady=20, padx=0)

    image = Image.open('gate.png')
    photo = ImageTk.PhotoImage(image)
    label = Label(root, image=photo)
    label.image = photo
    label.grid(row=0, column=1)


    name = Label(root, text='Name :').grid(row=1, column=0, padx=20)
    vname = Entry(root).grid(row=1, column=1, padx=20)
    house = Label(root, text='House :').grid(row=2, column=0, padx=20)
    vhouse = Entry(root).grid(row=2, column=1, padx=20)

    def activator():
        if rem['state'] == tk.DISABLED:
            rem['state'] = tk.NORMAL
        else:
            rem['state'] = tk.DISABLED

    chk = Label(root, text='Confirm Entry?').grid(row=3, column=0, padx=20)
    chk_btn = Checkbutton(root, command=activator).grid(row=3, column=1)


    rem = tk.Button(root, text='Confirm', command=home, state=tk.DISABLED)
    rem.grid(row=4, ipady=5, columnspan=3, sticky='NSWE', padx=5, pady=5)
    qut = Button(root, text='Quit', command=root.destroy)
    qut.grid(row=5, ipady=5, columnspan=3, sticky='NSWE', padx=5, pady=5)





def homeScr():
    for i in root.winfo_children():
        i.destroy()

    image = Image.open('gate.png')
    photo = ImageTk.PhotoImage(image)
    label = Label(root, image=photo)
    label.image = photo
    label.grid(row=0, column=1)

    app_title = Label(root, text='VMS', font=('JetBrains Mono',40))
    app_title.grid(row=0, column=0, pady=20)

    vw_history = Button(root, text='Add Visitor', width=26, command=newVis)
    vw_history.grid(row=1, columnspan=2, padx=20, pady=5, ipady=5)

    ad_visitor = Button(root, text='Remove Visitor', width=26, command=remVis)
    ad_visitor.grid(row=2, columnspan=2,padx=20, ipady=5)

    rem_visitor = Button(root, text='View History', width=26)
    rem_visitor.grid(row=3, columnspan=2, padx=20, pady=5, ipady=5)

    qt = Button(root, text='Quit', width=26, command=root.destroy)
    qt.grid(row=4, columnspan=2, padx=20, pady=0, ipady=5)

aptselect = simpledialog.askstring("Apartment", "Enter the name of the apartment :")
aptselect = aptselect.replace(" ", "")
db.chk_tbl(aptname=aptselect)

homeScr()
root.mainloop()