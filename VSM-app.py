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



# screen = Tk()
# screen.withdraw()
# screen.mainloop()
