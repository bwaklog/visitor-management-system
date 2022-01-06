import mysql.connector as mysql
# from tqdm import tqdm
# import time

'''
Defining a database :db
'''
db = mysql.connect(
    host = 'localhost',
    user = 'root',
    passwd = '1029Adity@',
    database = 'datacamp'
)

cursor = db.cursor()

# Function to create a new table for an apartment in the database 'db'
def crt_apt(aptname=str):
    query = "CREATE TABLE "+aptname+" (id INT(255) NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), house_no VARCHAR(255), reason VARCHAR(255), accreg BOOLEAN, chk_ins BOOLEAN)"
    cursor.execute(query)
    db.commit()
    print("Sucessfully created a table in database for apt :", aptname)

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
    

# Fucntion to add a visitor to the appartment
def add_visi(name=str, house_no=str, reason=str, accreg=bool, chk_ins=bool, aptname=str):

    name = "\'"+name+"\'"
    house_no = "\'"+house_no+"\'"
    reason = "\'"+reason+"\'"
    query = "INSERT INTO datacamp.%s (name, house_no, reason, accreg, chk_ins) VALUES (%s, %s, %s, %d, %d)"%(aptname, name, house_no, reason, accreg, chk_ins)
    cursor.execute(query)
    db.commit()

# Fumction to show the record of a specific apartment(table)
def show_rec(aptname=str):
    query = "SELECT * FROM datacamp."+aptname+""
    cursor.execute(query)
    records = cursor.fetchall()
    for record in records:
        name, house_no, reason, accreg, chk_ins = record[1], record[2], record[3], record[4], record[5]
        print("Name :",name, " | House no :", house_no, " | Reason :", reason)#, '\n           ACCREG  CHK_INS \n       |-->',accreg, '      ',chk_ins)

def remove(vname=str, vhouse=str, aptname=str):
    sr_query = 'SELECT * FROM datacamp.'+aptname+' WHERE name=\''+vname+'\' AND house_no=\''+vhouse+'\''
    cursor.execute(sr_query)
    record = cursor.fetchall()
    record = record[0]
    if record[-1] == 1:
        query = 'UPDATE datacamp.'+aptname+' SET chk_ins = 0 WHERE name=\''+vname+'\' AND house_no=\''+vhouse+'\''
        cursor.execute(query)
        db.commit()


while True:
    aptselect = input("Enter the name of your apartment : ")
    aptselect = aptselect.replace(" ", "")

    print(aptselect)
    # chk_tbl(aptname=aptselect)
    chk_tbl(aptname=aptselect)
    while True:
        choice = int(input("1. Check existing tables \n2. Add Visitor \n3. Remove Visitor \n4. Change Apartment \n5.Quit \n>>>Enter your choice :"))
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
            quit()