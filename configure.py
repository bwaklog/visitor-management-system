import os
from tkinter import *
import tkinter as tk
from tkinter.messagebox import askyesno


def clear_console(): return os.system(
    'cls' if os.name in ('nt', 'dos') else 'clear')


clear_console()

root = Tk()
root.title("ETALY Config")


def CONFIG():
    for i in root.winfo_children():
        i.destroy()

    app_title = Label(root, text='ETALY', font=('Mono', 40))
    app_title.grid(row=0, pady=20, padx=0, columnspan=2)

    def addition():
        host = host_info.get()
        user = user_info.get()
        passwd = passwd_info.get()
        print(host, user, passwd)

        accq = askyesno(title='Confirmation', message="Do you want to proceed")

        if accq:
            CONFIG()
            with open('config.txt', 'r+') as f:
                lines = f.readlines()
                f.seek(0)
                f.truncate()
                f.writelines(lines[1:])

            with open('config.txt', 'a') as filea:
                filea.write(host + '/' + user + '/' + passwd)

            tk.messagebox.showinfo(
                "Confirmed Changes", "You have accepted changes to the config file!")

        else:
            CONFIG()
            tk.messagebox.showinfo(
                "Changes Denied", "You have cancelled the changes")

    nl = Label(root, text='Host :')
    nl.grid(row=1, column=0, padx=5)
    hl = Label(root, text='User :')
    hl.grid(row=2, column=0, padx=5)
    rl = Label(root, text='Password :')
    rl.grid(row=3, column=0, padx=5)

    host_info = StringVar()
    user_info = StringVar()
    passwd_info = StringVar()

    ne = Entry(root, textvariable=host_info)
    ne.grid(row=1, column=1, padx=5)
    he = Entry(root, textvariable=user_info)
    he.grid(row=2, column=1, padx=5)
    re = Entry(root, textvariable=passwd_info)
    re.grid(row=3, column=1, padx=5)

    addbtn = Button(root, text='Proceed', width=26, command=addition)
    addbtn.grid(row=5, columnspan=2, pady=1, padx=5)

    def clear():
        CONFIG()

    bck = Button(root, text='Clear', width=26, command=clear)
    bck.grid(row=6, columnspan=2, pady=1, padx=5)

    qut = Button(root, text='Quit Application', width=26, command=root.destroy)
    qut.grid(row=8, columnspan=2, pady=1, padx=5)


CONFIG()

root.mainloop()
