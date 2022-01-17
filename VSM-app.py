from tkinter import *
import os
import mysql.connector as mysql
import pandas as pd
import time

clear_console = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
clear_console()

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
        name, house, reason, entry, ext, accreg, status = record[1], record[2], record[3], record[4], record[5], \
                                                           record[6], record[7]
        print(record)
        if str(status) == "None":
            print("Not inside")
        df.loc[len(df.index)] = [name, house, reason, entry, ext, accreg, status]
    print(df)


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
    query_i = "SELECT * FROM %s.%s WHERE `status`=1;"%(l[3], aptname)
    cursor.execute(query_i)
    records = cursor.fetchall()
    for record in records:
        print(record)
        name, house, reason, entry = record[1], record[2], record[3], record[4]
        df.loc[len(df.index)] = [name, house, reason, entry]
    print(df)



app = Tk()
app.title('VSM')
from PIL import Image, ImageTk

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
        HOMESCRC(apt=aptinfo)


    l1 = Label(app, text='Apartment Name :')
    l1.grid(row=1, column=0, padx=5)

    apartment = StringVar()

    apt = Entry(app, textvariable=apartment)
    apt.grid(row=1, column=1, padx=5)

    apt_sel = Button(app, text='Select Apartment!', width=26, command=selected)
    apt_sel.grid(row=2, columnspan=2, pady=5)


    pass
def HOMESCRC(apt=str):
    for i in app.winfo_children():
        i.destroy()

    app.title(apt)
    constnt()

    def vis():
        ADDVIS(apt=apt)
    def rem():
        pass
    def his():
        pass
    def insd():
        pass
    def change():
        STARTSRC(apt=apt)

    add_vis = Button(app, text='Add Visitor', width=26, command=vis)
    add_vis.grid(row=2, columnspan=2, pady=1, padx=5)
    rem_vis = Button(app, text='Remove Visitor', width=26, command=rem)
    rem_vis.grid(row=3, columnspan=2, pady=1, padx=5)
    hist = Button(app, text='View history', width=26, command=his)
    hist.grid(row=4, columnspan=2, pady=1, padx=5)
    ins = Button(app, text='Currently Inside', width=26, command=insd)
    ins.grid(row=5, columnspan=2, pady=1, padx=5)
    chng = Button(app, text='Change Apartment', width=26, command=change)
    chng.grid(row=5, columnspan=2, pady=1, padx=5)
    qut = Button(app, text='Quit Application', width=26, command=app.destroy)
    qut.grid(row=5, columnspan=2, pady=1, padx=5)


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
        HOMESCRC()
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

    bck = Button(app, text='Add Visitor', width=26, command=addition)
    bck.grid(row=5, columnspan=2, pady=1, padx=5)
    bck = Button(app, text='Back', width=26, command=HOMESCRC)
    bck.grid(row=6, columnspan=2, pady=1, padx=5)



STARTSRC()

app.mainloop()
