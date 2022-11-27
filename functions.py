# Functoins used for project
import mysql.connector as mysql
import os


def consoleClR(): return os.system(
    'cls' if os.name in ('nt', 'dos') else 'clear')


with open('config.txt', 'r') as f:
    l = f.readline()
    l.strip()
    l = l.split('/')


db = mysql.connect(
    host=l[0],
    user=l[1],
    passwd=l[2],
    database=l[3]
)

cursor = db.cursor()


# Creating a object for visitors
class Visitor:
    def __init__(self, aptname, name, house, reason):
        self.aptname = aptname
        self.name = name
        self.house = house
        self.reason = reason

    def getInfo(self, data):
        query = "SELECT * FROM %s.%s WHERE name = '%s'" % (
            db.database, self.aptname, self.name)
        cursor.execute(query)

        records = cursor.fetchall()[-1]

        if data == "name":
            return records[1]
        elif data == "house":
            return records[2]
        elif data == "reason":
            return records[3]
        elif data == "itime":
            return records[4]
        elif data == "otime":
            return records[5]
        elif data == "accreg":
            return records[6]
        elif data == "all":
            return records


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
        print("In list")
        print("Fetching table for", aptname)
    else:
        print("Not in list")


# Add a visitor to a table
def add_rec(aptname=str, name=str, house=str, reason=str, accreg=bool, status=bool):

    query = "INSERT INTO `%s`.`%s` (`name`, `house`, `reason`, `idate`, `fdate`, `accreg`, `status`) VALUES ('%s',\
     '%s', '%s', NOW(), NULL, %d, %d)" % (
        l[3], aptname, name, house, reason, accreg, status)
    cursor.execute(query)
    db.commit()


# Add the time of exit of a visitor - removing a visitor from the apartment
def remove(aptname=str, name=str, house=str):

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
