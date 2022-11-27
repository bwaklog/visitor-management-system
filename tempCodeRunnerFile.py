# GUI
from tkinter import *
from tkinter.messagebox import askyesno
import pandas as pd
import functions as fxn

app = Tk()
app.title("ETALY")

fxn.consoleClR()


def constnt():

    def back():
        pass

    backBtn = Button(app, text="Home Page", width="26", command=back)
    backBtn.grid(row=10, columnspan=2, pady=1, padx=5)
    appTitle = Label(app, text="ETALY", font=('Mono', 40))
    appTitle.grid(row=1, columnspan=2, pady=20, padx=0)


def STARTSRC():
    for i in app.winfo_children():
        i.destroy()

    constnt()

    def aptSel():
        aptinfo = apt.get()
        str(aptinfo).replace(" ", "")
        # chk_tbl(aptname=aptinfo)

    l1 = Label(app, text='Apartment Name :')
    l1.grid(row=1, column=0, padx=5)

    apartment = StringVar()

    apt = Entry(app, textvariable=apartment)
    apt.grid(row=1, column=1, padx=5)

    selApt = Button(app, text='Select Apartment!', width=26, command=aptSel)
    selApt.grid(row=2, columnspan=2, pady=5)

    appQut = Button(app, text='Quit Application',
                    width=26, command=app.destroy)
    appQut.grid(row=4, columnspan=2, pady=1, padx=5)


def HOMESCR(apt=str):
    for i in app.winfo_children():
        i.destroy()

    app.title(apt + " | ETALY")
    constnt()

    def addVis():
        pass

    def exitVis():
        pass

    def histVis():
        pass

    def chkStat():
        pass

    def aptSel():
        pass

    def qutApp():
        pass

    visAdd = Button(app, text="Add Visitor", width="26", command=addVis)
    visAdd.grid(row=2, columnspan=2, pady=1, padx=5)
    visExit = Button(app, text="Remove Visitor", width="26", command=exitVis)
    visExit.grid(row=3, columnspan=2, pady=1, padx=5)
    visHist = Button(app, text="Visiting History", width="26", command=histVis)
    visHist.grid(row=3, columnspan=2, pady=1, padx=5)
    statChk = Button(app, text="Add Visitor", width="26", command=chkStat)
    statChk.grid(row=4, columnspan=2, pady=1, padx=5)
    selApt = Button(app, text="Reselect appartment",
                    width="26", command=aptSel)
    selApt.grid(row=5, columnspan=2, pady=1, padx=5)
    appQut = Button(app, text="Add Visitor", width="26", command=qutApp)
    appQut.grid(row=6, columnspan=2, pady=1, padx=5)


def STARTSRC():
    for i in app.winfo_children():
        i.destroy()

    constnt()

    def selected():
        aptinfo = apt.get()
        str(aptinfo).replace(" ", "")
        chk_tbl(aptname=aptinfo)
        # print("Fetching table for", aptinfo)
        # HOMESCR(apt=aptinfo)

    l1 = Label(app, text='Apartment Name :')
    l1.grid(row=1, column=0, padx=5)

    apartment = StringVar()

    apt = Entry(app, textvariable=apartment)
    apt.grid(row=1, column=1, padx=5)

    apt_sel = Button(app, text='Select Apartment!', width=26, command=selected)
    apt_sel.grid(row=2, columnspan=2, pady=5)

    qut = Button(app, text='Quit Application', width=26, command=app.destroy)
    qut.grid(row=4, columnspan=2, pady=1, padx=5)


# HOMESCR(apt='apt1')
STARTSRC()

app.mainloop()
