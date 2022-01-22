'''
VISITOR MANAGEMENT SYSTEM
version 4.3.2
===================================================================================================================
Author     : Aditya Hegde
Github     : xadityahx
Repository : visitor-management-system
Created on : 19th October 2021
'''

# Modules necessary for the project
from PIL import Image, ImageTk
from tkinter import *
import os
import mysql.connector as mysql
import pandas as pd

# Function to clear the terminal


def clear_console(): return os.system(
    'cls' if os.name in ('nt', 'dos') else 'clear')


# Clearing the terminal
clear_console()


# Defining the windown using tkinter
app = Tk()
app.title('VSM')

# Getting the details of the configuration for using MySQL(hostname, username, password and database being used)
with open('config.txt', 'r') as f:
    l = f.readline()
    l.strip('')
    l = l.split('/')

# Connecting to the databse that is going to be referred to in the application
db = mysql.connect(
    host=l[0],
    user=l[1],
    passwd=l[2],
    database=l[3]
)

# Defining the cursor to perform SQL commands in MySQL
cursor = db.cursor()


# Function to create a new table for an apartment in the database
def crt_apt(aptname=str):
    """Function To create an apartment

    Args:
        aptname (str, optional): [description]. Defaults to str.
    """
    query = "CREATE TABLE " + aptname + " (vsid INT NOT NULL AUTO_INCREMENT\
     PRIMARY KEY, name VARCHAR(255), house VARCHAR(255),reason VARCHAR(255),\
      idate DATETIME, fdate DATETIME, accreg BOOLEAN, status BOOLEAN)"

    cursor.execute(query)
    db.commit()
    print(aptname, "table successfully created")


# Function to check whether the table for an apartment exists inside a table
def chk_tbl(aptname=str):
    """Function to check whether the table for an apartment exists insisde the database being used

    Args:
        aptname (str, optional): [description]. Defaults to str.
    """
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


# Shows the records of a table - people inside and outside(Terminal output)
# This function also creates an interface to show the graphical output in the app window in the form of a table
def show_rec(aptname=str):
    """ Outputs the history of entries in the table {aptname}

    Args:
        aptname (str, optional): [description]. Defaults to str.
    """
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

    btn = Button(app, text='Exit Home', command=ext_home, width=26).grid(
        row=i, pady=5, columnspan=len(records[0]))


# Add a visitor to a table
def add_rec(aptname=str, name=str, house=str, reason=str, accreg=bool, status=bool):
    """Function to create and execute an sql query to enter in a visitor

    Args:
        aptname (str, optional): Apartment name. Defaults to str.
        name (str, optional): Name of visitor. Defaults to str.
        house (str, optional): House the visitor is visiting. Defaults to str.
        reason (str, optional): Reason for visit. Defaults to str.
        accreg (bool, optional): Accepted or rejected entry. Defaults to bool.
        status (bool, optional): Status - if visitor is inside. Defaults to bool. Default to 1 if entry if {accreg} is 1
    """
    query = "INSERT INTO `%s`.`%s` (`name`, `house`, `reason`, `idate`, `fdate`, `accreg`, `status`) VALUES ('%s',\
     '%s', '%s', NOW(), NULL, %d, %d)" % (
        l[3], aptname, name, house, reason, accreg, status)
    cursor.execute(query)
    db.commit()


# Add the time of exit of a visitor - removing a visitor from the apartment
def remove(aptname=str, name=str, house=str):
    """Function to add the time the visitor exits the aparment and change {status} value to 0

    Args:
        aptname (str, optional): Apartment name. Defaults to str.
        name (str, optional): Visitor's name. Defaults to str.
        house (str, optional): House which was visitied -  house number. Defaults to str.
    """
    query_s = "SELECT * FROM %s.%s WHERE name='%s' AND house='%s'" % (
        l[3], aptname, name, house)
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

    def get_data(self):  # sourcery skip: remove-unnecessary-else
        """Creating a visitor object to be used, incase a particular visitor's record is to be retrive"

        Returns:
            str: Returns "No data available" if there exists no record with the given name and house combination

            if the arguements for name and house combination exists, in that case we can retrieve the other details:
                > of the visitor such as the time of entry
                > time of exit(if visitor has left the apartment)
                > if the visitor is still inside the complex
                > if the visitor entry has been rejected
        """
        query_s = "SELECT * FROM %s.%s WHERE name='%s' AND house='%s'" % (
            l[3], self.aptname, self.name, self.house)
        cursor.execute(query_s)
        record = cursor.fetchall()
        if record == []:
            return print("No data available")
        else:
            record = record[0]
            vname, vhouse, reason, entry, ext, accreg, status = record[1:]
            # print(vname, vhouse, reason, entry, ext, accreg, status)


# Function to check who all are inside
# This function also creates an interface to show the graphical output in the app window in the form of a table
def status_in(aptname=str):
    """Return the records in a tabulated manner of only those who are still inside

    Args:
        aptname (str, optional): Apartment name. Defaults to str.
    """
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

    btn = Button(app, text='Exit Home', command=ext_home, width=26).grid(
        row=i, pady=5, columnspan=len(records[0]))


# Logo + App Title which is used in all screens
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


# Interface for start screen
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


# Interface for the homescreen of the selected apartment - same for all
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

    def insd():
        clear_console()  # can comment out
        VWINSD(apt=apt)

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


# Interface to add a visitor
def ADDVIS(apt=str):
    for i in app.winfo_children():
        i.destroy()
    constnt()

    def addition():
        name_info = name.get()
        house_info = house.get()
        reason_info = reason.get()
        print(name_info, house_info, reason_info)
        add_rec(aptname=apt, name=name_info, house=house_info,
                reason=reason_info, accreg=1, status=1)
        print("Record has been added")
        print("Exiting to Home screen")
        HOMESCR(apt=apt)

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


# Interface for when you want to record someone leaving the apartment
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


# Calling the interface for showing the tabulated form of the visiting history
def HISTORY(apt):
    show_rec(aptname=apt)


# Filters out the visiting history and returns a tabulated result of the people still inside the association
def VWINSD(apt):
    status_in(aptname=apt)


# Initiate app from Start Screen - to enter apartment name
STARTSRC()

app.mainloop()
