import os
clear_console = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
clear_console()
import mysql.connector as mysql

with open('config.txt', 'r') as f:
    l = f.readline()
    l.strip('')
    l = l.split('/')
print(l)

db = mysql.connect(
    host = l[0],
    user = l[1],
    passwd = l[2],
    database = l[3]
)