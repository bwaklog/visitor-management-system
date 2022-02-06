import os
import time
import datetime

clear_console = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
clear_console()

start = time.time()
print('[SYSTEM] LOCAL :', datetime.datetime.now())
print('[SYSTEM]       : WARNING')
print('[SYSTEM]       : config files will be effected')

host = input("~ HOST NAME    : ")
user = input("~ USER NAME    : ")
passwd = input("~ PASSWORD     : ")
database = input("~ DATABASE NAME: ")
proceed = input('[SYSTEM]       : Would you like to proceed (y/n)\n~ $ ')

if proceed.lower() == 'n':
    print('[SYSTEM]       : Reverting changes')
    quit()

with open('config.txt', 'r+') as f:
    lines = f.readlines()
    f.seek(0)
    f.truncate()
    f.writelines(lines[1:])

with open('config.txt', 'a') as filea:
    filea.write(host+ '/'+user+ '/'+passwd+ '/'+database)
    filea.close()
    print('[SYSTEM]       : Config files have been modified')
    print('[SYSTEM]       : %s seconds' % (time.time()-start))
    print('[SYSTEM] LOCAL :', datetime.datetime.now())
    quit()
