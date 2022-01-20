from tkinter import *
import os
import mysql.connector as mysql
import pandas as pd
import time
import sys

clear_console = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
clear_console()

app = Tk()
app.title('VSM')
from PIL import Image, ImageTk

with open('config.txt', 'r') as f:
    l = f.readline()
    l.strip('')
    l = l.split('/')

db = mysql.connect(
    host=l[0],
    user=l[1],
    passwd=l[2],
    database=l[3]
)

cursor = db.cursor()


# Function to create a new table for an apartment in the database
def crt_apt(aptname=str):
    query = "CREATE TABLE " + aptname + " (vsid INT NOT NULL AUTO_INCREMENT\
     PRIMARY KEY, name VARCHAR(255), house VARCHAR(255),reason VARCHAR(255),\
      idate DATETIME, fdate DATETIME, accreg BOOLEAN, status BOOLEAN)"

    cursor.execute(query)
    db.commit()
    print(aptname, "table successfully created")


# Function to check whether the table for an apartment exists inside a table
def chk_tbl(aptname=str):
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    tbl_list = [table[0] for table in tables]
    print(tbl_list)
    if aptname in tbl_list:
        print(True)
    else:
        print(aptname)
        choice = input('False\nDo you want to create a new one(y/n) : ')
        if choice.lower() == 'y':
            crt_apt(aptname)


# show records of a specific table
coln = ['Name', 'House No', 'Reason', 'Entry', 'Exit', 'Accreg', 'Status']


# Shows the records of a table - people inside and outside
def show_rec(aptname=str):
    df = pd.DataFrame(columns=coln)
    query = "SELECT * FROM " + l[3] + "." + aptname + ""
    cursor.execute(query)
    records = cursor.fetchall()
    for record in records:
        name, house, reason, entry, ext, accreg, stat = record[1], record[2], record[3], record[4], record[5], \
                                                        record[6], record[7]
        print(record)
        if stat == 1:
            ext = 'Still Inside'
            print("Not inside")
        df.loc[len(df.index)] = [name, house, reason, entry, ext, accreg, stat]

    print(df)

    for wid in app.winfo_children():
        wid.destroy()

    constnt()

    cols = ['Name', 'House', 'Reason', 'Entry Time', 'Exit Time']
    for c in range(len(cols)):
        col = Label(app, text=cols[c])
        col.grid(row=1, column=c)

    i = 2
    records = list(records)
    for record in records:
        record = record[1:6]
        record = list(record)
        for j in range(len(record)):
            e = Entry(app, width=10, fg='blue')
            e.grid(row=i, column=j, ipadx=26)
            if str(record[j]) == 'None':
                record[j] = 'Still Inside'
            e.insert(END, record[j])
        i = i + 1

    def ext_home():
        HOMESCR(apt=aptname)

    btn = Button(app, text='Exit Home', command=ext_home, width=26).grid(row=i, pady=5, columnspan=len(records[0]))


# Add a visitor to a table
def add_rec(aptname=str, name=str, house=str, reason=str, accreg=bool, status=bool):
    query = "INSERT INTO `%s`.`%s` (`name`, `house`, `reason`, `idate`, `fdate`, `accreg`, `status`) VALUES ('%s',\
     '%s', '%s', NOW(), NULL, %d, %d)" % (
        l[3], aptname, name, house, reason, accreg, status)
    cursor.execute(query)
    db.commit()


# Add the time of exit of a visitor - removing a visitor from the apartment
def remove(aptname=str, name=str, house=str):
    query_s = "SELECT * FROM %s.%s WHERE name='%s' AND house='%s'" % (l[3], aptname, name, house)
    print('Stage 1')
    cursor.execute(query_s)
    record = cursor.fetchall()
    record = record[0]
    if record[-1] == 1:
        query_r = "UPDATE `%s`.`%s` SET `fdate` = NOW(), `status` = '0' WHERE name='%s' AND house='%s'" % (
            l[3], aptname, name, house)
        print('Stage 2')
        cursor.execute(query_r)
        db.commit()


# get data of a specific record !!!
class Visitor:
    def __init__(self, aptname, name, house):
        self.aptname = aptname
        self.name = name
        self.house = house

    def get_data(self):
        query_s = "SELECT * FROM %s.%s WHERE name='%s' AND house='%s'" % (l[3], self.aptname, self.name, self.house)
        cursor.execute(query_s)
        record = cursor.fetchall()
        if record == []:
            return print("No data available")
        else:
            record = record[0]
            vname, vhouse, reason, entry, ext, accreg, status = record[1:]
            # print(vname, vhouse, reason, entry, ext, accreg, status)


# Function to check who all are inside
def status_in(aptname=str):
    coln = ['Visitor', 'House', 'Reason', 'Entry']
    df = pd.DataFrame(columns=coln)
    query_i = "SELECT * FROM %s.%s WHERE `status`=1;" % (l[3], aptname)
    cursor.execute(query_i)
    records = cursor.fetchall()
    for record in records:
        print(record)
        name, house, reason, entry = record[1], record[2], record[3], record[4]
        df.loc[len(df.index)] = [name, house, reason, entry]
    print(df)

    for wid in app.winfo_children():
        wid.destroy()

    constnt()

    cols = ['Name', 'House', 'Reason', 'Entry Time']
    for c in range(len(cols)):
        col = Label(app, text=cols[c])
        col.grid(row=1, column=c)

    i = 2
    records = list(records)
    for record in records:
        record = record[1:5]
        record = list(record)
        for j in range(len(record)):
            e = Entry(app, width=10, fg='blue')
            e.grid(row=i, column=j, ipadx=26)
            e.insert(END, record[j])
        i = i + 1

    def ext_home():
        HOMESCR(apt=aptname)

    btn = Button(app, text='Exit Home', command=ext_home, width=26).grid(row=i, pady=5, columnspan=len(records[0]))


def constnt():
    # consistent GUI
    app_title = Label(app, text='VMS', font=('Mono', 40))
    # app_title.config(background='white')
    app_title.grid(row=0, column=0, pady=20, padx=0)
    image = Image.open('gate.png')
    photo = ImageTk.PhotoImage(image)
    label = Label(app, image=photo)
    label.image = photo
    label.grid(row=0, column=1)


def STARTSRC():
    for i in app.winfo_children():
        i.destroy()

    constnt()

    def selected():
        aptinfo = apt.get()
        str(aptinfo).replace(" ", "")
        chk_tbl(aptname=aptinfo)
        print("Fetching table for", aptinfo)
        HOMESCR(apt=aptinfo)

    l1 = Label(app, text='Apartment Name :')
    l1.grid(row=1, column=0, padx=5)

    apartment = StringVar()

    apt = Entry(app, textvariable=apartment)
    apt.grid(row=1, column=1, padx=5)

    apt_sel = Button(app, text='Select Apartment!', width=26, command=selected)
    apt_sel.grid(row=2, columnspan=2, pady=5)

    pass


def HOMESCR(apt=str):
    for i in app.winfo_children():
        i.destroy()

    app.title(apt)
    constnt()

    def vis():
        ADDVIS(apt=apt)

    def rem():
        REMVIS(apt=apt)

    def his():
        clear_console()  # can comment outr
        show_rec(aptname=apt)
        HISTORY(apt=apt)
        pass

    def insd():
        clear_console()  # can comment out
        VWINSD(apt=apt)
        pass

    def change():
        app.title('VMS')
        STARTSRC()

    add_vis = Button(app, text='Add Visitor', width=26, command=vis)
    add_vis.grid(row=2, columnspan=2, pady=1, padx=5)
    rem_vis = Button(app, text='Remove Visitor', width=26, command=rem)
    rem_vis.grid(row=3, columnspan=2, pady=1, padx=5)
    hist = Button(app, text='View history', width=26, command=his)
    hist.grid(row=4, columnspan=2, pady=1, padx=5)
    ins = Button(app, text='Currently Inside', width=26, command=insd)
    ins.grid(row=5, columnspan=2, pady=1, padx=5)
    chng = Button(app, text='Change Apartment', width=26, command=change)
    chng.grid(row=6, columnspan=2, pady=1, padx=5)
    qut = Button(app, text='Quit Application', width=26, command=app.destroy)
    qut.grid(row=7, columnspan=2, pady=1, padx=5)


def ADDVIS(apt=str):
    for i in app.winfo_children():
        i.destroy()
    constnt()

    def addition():
        name_info = name.get()
        house_info = house.get()
        reason_info = reason.get()
        print(name_info, house_info, reason_info)
        add_rec(aptname=apt, name=name_info, house=house_info, reason=reason_info, accreg=1, status=1)
        print("Record has been added")
        print("Exiting to Home screen")
        HOMESCR(apt=apt)
        pass

    nl = Label(app, text='Visitor Name :')
    nl.grid(row=1, column=0, padx=5)
    hl = Label(app, text='House Visiting :')
    hl.grid(row=2, column=0, padx=5)
    rl = Label(app, text='Visiting Reason :')
    rl.grid(row=3, column=0, padx=5)

    name = StringVar()
    house = StringVar()
    reason = StringVar()

    ne = Entry(app, textvariable=name)
    ne.grid(row=1, column=1, padx=5)
    he = Entry(app, textvariable=house)
    he.grid(row=2, column=1, padx=5)
    re = Entry(app, textvariable=reason)
    re.grid(row=3, column=1, padx=5)

    cl = Label(app, text='Confirm Entry :')
    cl.grid(row=4, column=0, padx=5)
    cr = Checkbutton(app)
    cr.grid(row=4, column=1)

    def back():
        HOMESCR(apt=apt)

    addbtn = Button(app, text='Add Visitor', width=26, command=addition)
    addbtn.grid(row=5, columnspan=2, pady=1, padx=5)
    bck = Button(app, text='Back', width=26, command=back)
    bck.grid(row=6, columnspan=2, pady=1, padx=5)


def REMVIS(apt=str):
    for i in app.winfo_children():
        i.destroy()
    constnt()

    nl = Label(app, text='Visitor Name :')
    nl.grid(row=1, column=0, padx=5)
    hl = Label(app, text='House Visiting :')
    hl.grid(row=2, column=0, padx=5)

    name = StringVar()
    house = StringVar()

    ne = Entry(app, textvariable=name)
    ne.grid(row=1, column=1, padx=5)
    he = Entry(app, textvariable=house)
    he.grid(row=2, column=1, padx=5)

    cl = Label(app, text='Confirm Entry :')
    cl.grid(row=4, column=0, padx=5)
    cr = Checkbutton(app)
    cr.grid(row=4, column=1)

    def rem_visi():
        remove(aptname=apt, name=ne.get(), house=he.get())
        print("Executed")
        HOMESCR(apt=apt)

    def back():
        HOMESCR(apt=apt)

    bck = Button(app, text='Add Visitor', width=26, command=rem_visi)
    bck.grid(row=5, columnspan=2, pady=1, padx=5)
    bck = Button(app, text='Back', width=26, command=back)
    bck.grid(row=6, columnspan=2, pady=1, padx=5)


def HISTORY(apt):
    show_rec(aptname=apt)


def VWINSD(apt):
    status_in(aptname=apt)


STARTSRC()

app.mainloop()
