from dis import dis
import os
import mysql.connector as mysql
from time import sleep
import pandas as pd

clear_console = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
clear_console()

with open('config.txt', 'r') as f:
    l = f.readline()
    l.strip('')
    l = l.split('/')
    
'''
Defining a database 

(Author Reference)
db = mysql.connect(
    host = 'localhost',
    user = 'root',
    passwd = '1029Adity@',
    database = 'datacamp'
)
'''
db = mysql.connect(
    host = l[0],
    user = l[1],
    passwd = l[2],
    database = l[3]
)

cursor = db.cursor()

# Function to create a new table for an apartment in the database 'db'
def crt_apt(aptname=str):
    query = "CREATE TABLE "+aptname+" (id INT(255) NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), house_no VARCHAR(255),\
    reason VARCHAR(255), accreg BOOLEAN, chk_ins BOOLEAN)"
    cursor.execute(query)
    db.commit()
    print("Sucessfully created a table in database for apt :", aptname)
# --------------------------------------------------------------------------------------------------------------------------------

# Function to check wether an apartment exists inside a database or not, and have operations follow it
def chk_tbl(aptname=str):  # sourcery skip: remove-redundant-pass
    # con_lod()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    tbl_list = [table[0] for table in tables]
    print(tbl_list)
    if aptname in tbl_list:
        print(True)
        show_rec(aptname=aptname)
    else:
        print(False)
        choice = input("Do you want to create one(y/n)")
        if choice.lower() == 'y':
            crt_apt(aptname=aptname)
        else: 
            pass
# --------------------------------------------------------------------------------------------------------------------------------

# Fucntion to add a visitor to the appartment
def add_visi(name=str, house_no=str, reason=str, accreg=bool, chk_ins=bool, aptname=str):

    name = "\'"+name+"\'"
    house_no = "\'"+house_no+"\'"
    reason = "\'"+reason+"\'"
    query = "INSERT INTO datacamp.%s (name, house_no, reason, accreg, chk_ins) VALUES\
    (%s, %s, %s, %d, %d)"%(aptname, name, house_no, reason, accreg, chk_ins)
    cursor.execute(query)
    db.commit()
# --------------------------------------------------------------------------------------------------------------------------------

# Fumction to show the record of a specific apartment(table)
coln = ['Visitor Name', 'House No', 'Reason', 'Accreg', 'Status']
def show_rec(aptname=str):
    df = pd.DataFrame(columns=coln)
    query = "SELECT * FROM datacamp."+aptname+""
    cursor.execute(query)
    records = cursor.fetchall()
    for record in records:
        name, house_no, reason, accreg, chk_ins = record[1], record[2], record[3], record[4], record[5]
        # print('~~')
        # print("Name :",name, " | House no :", house_no, " | Reason :", reason)
        # print('~~')

        df.loc[len(df.index)] = [name, house_no, reason, accreg, chk_ins]
    return print(df)

# --------------------------------------------------------------------------------------------------------------------------------

def remove(vname=str, vhouse=str, aptname=str):
    sr_query = 'SELECT * FROM datacamp.'+aptname+' WHERE name=\''+vname+'\' AND house_no=\''+vhouse+'\''
    cursor.execute(sr_query)
    record = cursor.fetchall()
    record = record[0]
    if record[-1] == 1:
        query = 'UPDATE datacamp.'+aptname+' SET chk_ins = 0 WHERE name=\''+vname+'\' AND house_no=\''+vhouse+'\''
        cursor.execute(query)
        db.commit()
# --------------------------------------------------------------------------------------------------------------------------------

def chk_ins(aptname=str):
    coln = ['Visitor Name', 'House no', 'Reason']
    df = pd.DataFrame(columns=coln)
    ins_query = 'SELECT * FROM ' + l[3] +'.'+aptname+" WHERE chk_ins = 1"
    cursor.execute(ins_query)
    records = cursor.fetchall()
    for record in records:
        name, house_no, reason, accreg, chk_ins = record[1], record[2], record[3], record[4], record[5]
        # print('~~')
        # print("Name :",name, " | House no :", house_no, " | Reason :", reason)
        # print('~~')

        df.loc[len(df.index)] = [name, house_no, reason]
    return print(df)

while True:
    aptselect = input("Enter the name of your apartment : ")
    aptselect = aptselect.replace(" ", "")

    print(aptselect)
    chk_tbl(aptname=aptselect)
    print("[SERVER] : Loading database...")
    sleep(1)
    clear_console()
    while True:
        choice = int(input("1. Check existing tables \n2. Add Visitor \n3. Remove Visitor \n4. Change Apartment\
             \n5.Show Visitors Inside \n6.Quit \n>>>Enter your choice :"))
        if choice == 1:
            show_rec(aptname=aptselect)
        elif choice == 2:
            vname = input("Enter the name of the visitor : ")
            vhouse = input("Enter the house visiting : ")
            vreason = input("Reason for visit : ")
            accrej = input("Accept(y/n)")
            if accrej.lower() == "y":
                vaccreg = 1
                vchk_ins = 1
            add_visi(name=vname, house_no=vhouse, reason=vreason, accreg=vaccreg, chk_ins=vchk_ins, aptname=aptselect)
        elif choice == 3:
            vname = input("Enter the Name of the person leaving : ")
            vhouse = input("Enter the house visited : ")
            remove(vname=vname, vhouse=vhouse, aptname=aptselect)
        elif choice == 4:
            break  
        elif choice == 5:
            chk_ins(aptname=aptselect)
        elif choice == 6:
            clear_console()
            print("~ Exiting application")
            sleep(2)
            clear_console()
            quit()
