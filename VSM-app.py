'''
VISITOR MANAGEMENT SYSTEM
version 5.0
===================================================================================================================
Author     : Aditya Hegde
Github     : bwaklog
Repository : visitor-management-system
Created on : 19th October 2021
'''

import os
import smtplib
import ssl
import tkinter
from tkinter import *
from tkinter.messagebox import askyesno
import mysql.connector as mysql
import pandas as pd


# Function to clear the terminal
def clear_console(): return os.system(
    'cls' if os.name in ('nt', 'dos') else 'clear')


# Clearing the terminal
clear_console()

# Defining the windown using tkinter
app = Tk()
app.title('ETALY')

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
    # database=l[3]
)

# Defining the cursor to perform SQL commands in MySQL
cursor = db.cursor()

cr = "create database if not exists VSM"
cursor.execute(cr)
cursor.execute("commit")
q = "use VSM"
cursor.execute(q)


# Function to create a new table for an apartment in the database


def crt_apt(aptname=str):

    query = "CREATE TABLE " + aptname + " (vsid INT NOT NULL AUTO_INCREMENT\
     PRIMARY KEY, name VARCHAR(255), house VARCHAR(255),reason VARCHAR(255),\
      idate DATETIME, fdate DATETIME, accreg BOOLEAN, status BOOLEAN)"

    cursor.execute(query)
    db.commit()
    print(aptname, "table successfully created")
    HOMESCR(apt=aptname)


# Function to check whether the table for an apartment exists inside a table
def chk_tbl(aptname=str):

    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    tbl_list = [table[0] for table in tables]
    print(tbl_list)
    if aptname in tbl_list:
        print(True)
        print("In list")
        print("Fetching table for", aptname)
        HOMESCR(apt=aptname)
    else:
        print("Not in list")
        NEWAPT(apt=aptname)


# show records of a specific table
coln = ['Name', 'House No', 'Reason', 'Entry', 'Exit', 'Accreg', 'Status']


# Shows the records of a table - people inside and outside(Terminal output)
# This function also creates an interface to show the graphical output in the app window in the form of a table
def show_rec(aptname=str):

    df = pd.DataFrame(columns=coln)
    query = "SELECT * FROM VSM." + aptname + ""
    cursor.execute(query)
    records = cursor.fetchall()

    if len(records) >= 1:
        for record in records:
            name, house, reason, entry, ext, accreg, stat = record[1], record[2], record[3], record[4], record[5], \
                record[6], record[7]
            print(record)
            if stat == 1:
                ext = 'Still Inside'
                print("Not inside")
            df.loc[len(df.index)] = [name, house,
                                     reason, entry, ext, accreg, stat]

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

    else:
        tkinter.messagebox.showinfo(
            "History Check", "There are no visitors inside the association!")


# Add a visitor to a table
def add_rec(aptname=str, name=str, house=str, reason=str, accreg=bool, status=bool):

    query = "INSERT INTO VSM.`%s` (`name`, `house`, `reason`, `idate`, `fdate`, `accreg`, `status`) VALUES ('%s',\
     '%s', '%s', NOW(), NULL, %d, %d)" % (aptname, name, house, reason, accreg, status)
    cursor.execute(query)
    db.commit()


# Add the time of exit of a visitor - removing a visitor from the apartment
def remove(aptname=str, name=str, house=str):

    query_s = "SELECT * FROM VSM.%s WHERE name='%s' AND house='%s'" % (
        aptname, name, house)
    print('Stage 1')
    cursor.execute(query_s)
    record = cursor.fetchall()
    print(record)
    record = record[-1]
    print(record)
    if record[-1] == 1:
        query_r = "UPDATE VSM.`%s` SET `fdate` = NOW(), `status` = '0' WHERE name='%s' AND house='%s'" % (
            aptname, name, house)
        print('Stage 2')
        cursor.execute(query_r)
        db.commit()


# get data of a specific record !!!
class Visitor:
    def __init__(self, aptname, name, house):
        self.aptname = aptname
        self.name = name
        self.house = house

    def get_info(self, data):

        query_s = "SELECT * FROM VSM.%s WHERE name='%s'" % (
            self.aptname, self.name)
        cursor.execute(query_s)

        record = cursor.fetchall()[-1]

        if data == "name":
            return record[1]
        elif data == "house":
            return record[2]
        elif data == "reason":
            return record[3]
        elif data == "itime":
            return record[4]
        elif data == "otime":
            return record[5]
        elif data == "accreg":
            return record[6]
        elif data == "all":
            return record


# App Title which is used in all screens
def constnt():
    # consistent GUI
    app_title = Label(app, text='ETALY', font=('Mono', 40))
    # app_title.config(background='white')
    app_title.grid(row=0, pady=20, padx=0, columnspan=2)


# SMTP service to send email notifications for new visitors
def vis_notif(aptname=str, name=str, reason=str, house=str, request=str):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "bwaklog@gmail.com"
    reciever_email = "bwaklog@gmail.com"
    password = 'tthf evvx ilva mxxv'

    msg = ""

    if request == "approve":
        msg = "You have approved the entry of %s to house %s in apartment %s for %s" % (
            name, house, aptname, reason)

    elif request == "deny":
        msg = "You have denied the entry of %s to house %s in apartment %s for %s" % (
            name, house, aptname, reason)

    elif request == "exit":
        msg = "%s has left the association" % (name)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, reciever_email, msg)

    print("msg sent")


# --------------------------------------------------------------------------


# Interface for start screen
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


def NEWAPT(apt=str):
    for i in app.winfo_children():
        i.destroy()

    constnt()

    l1 = Label(app, text=f'Would you want to create a table for {apt}')
    l1.grid(row=1, column=0, padx=5)

    def y_crt():
        crt_apt(aptname=apt)

    def n_crt():
        STARTSRC()

    crt_t = Button(app, text='Create Apartment', width=26, command=y_crt)
    crt_t.grid(row=2, columnspan=2, pady=5)
    crt_f = Button(app, text='Don\'t Create Apartment',
                   width=26, command=n_crt)
    crt_f.grid(row=3, columnspan=2, pady=5)

    qut = Button(app, text='Quit Application', width=26, command=app.destroy)
    qut.grid(row=4, columnspan=2, pady=1, padx=5)


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

        accreg = askyesno(title='House %s' % (
            house_info), message="Do you want to accept the entry of %s" % (name_info))

        if accreg:
            add_rec(aptname=apt, name=name_info, house=house_info,
                    reason=reason_info, accreg=1, status=1)
            vis_notif(aptname=apt, name=name_info, reason=reason_info,
                      house=house_info,  request='approve')
            print("Record has been added")
            print("Exiting to Home screen")
            HOMESCR(apt=apt)
            tkinter.messagebox.showinfo(
                "Confirmed entry", "Entry has been approved")

        else:
            HOMESCR(apt=apt)
            tkinter.messagebox.showinfo(
                "Entry Denied", "Entry has been denied")
            vis_notif(aptname=apt, name=name_info, reason=reason_info,
                      house=house_info, request='deny')

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

    addbtn = Button(app, text='Add Visitor', width=26, command=addition)
    addbtn.grid(row=5, columnspan=2, pady=1, padx=5)

    def back():
        HOMESCR(apt=apt)

    bck = Button(app, text='Back', width=26, command=back)
    bck.grid(row=6, columnspan=2, pady=1, padx=5)

    qut = Button(app, text='Quit Application', width=26, command=app.destroy)
    qut.grid(row=8, columnspan=2, pady=1, padx=5)


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

    def rem_visi():
        vis = Visitor(aptname=apt, name=ne.get(), house=he.get())
        reason = vis.get_info("reason")
        remove(aptname=apt, name=ne.get(), house=he.get())
        vis_notif(aptname=apt, name=ne.get(), reason=reason,
                  house=he.get(), request="exit")
        print("Executed")
        HOMESCR(apt=apt)

    def back():
        HOMESCR(apt=apt)

    bck = Button(app, text='Remove Visitor', width=26, command=rem_visi)
    bck.grid(row=5, columnspan=2, pady=1, padx=5)
    bck = Button(app, text='Back', width=26, command=back)
    bck.grid(row=6, columnspan=2, pady=1, padx=5)

    qut = Button(app, text='Quit Application', width=26, command=app.destroy)
    qut.grid(row=7, columnspan=2, pady=1, padx=5)

# Calling the interface for showing the tabulated form of the visiting history


def HISTORY(apt):
    show_rec(aptname=apt)


# Filters out the visiting history and returns a tabulated result of the people still inside the association
def VWINSD(apt):
    # status_in(aptname=apt)
    coln = ['Visitor', 'House', 'Reason', 'Entry']
    df = pd.DataFrame(columns=coln)
    query_i = "SELECT * FROM VSM.%s WHERE `status`=1;" % (apt)
    cursor.execute(query_i)
    records = cursor.fetchall()

    if len(records) >= 1:
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
            HOMESCR(apt=apt)

        btn = Button(app, text='Exit Home', command=ext_home, width=26).grid(
            row=i, pady=5, columnspan=len(records[0]))

    else:
        tkinter.messagebox.showinfo(
            "Status Check", "There are no visiors inside the association")


# Initiate app from Start Screen - to enter apartment name
STARTSRC()
app.title('ETALY')

app.mainloop()
