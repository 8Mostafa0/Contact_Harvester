import sqlite3 as sql
import pandas as pd
import os
import pyfiglet as pf
from alive_progress import alive_bar

#!============= PRINT TITLE 
title = "Contact Harvester"
textArt = pf.figlet_format(title)
print(textArt)


#!============ GET USERS LIST FROM DATABASE AND users TABLE
def getUsers():
        
    db = sql.connect(file)
    cur = db.cursor()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    db.close()

    return users



#=========== MAIN FUCNTION OF APP
def main():
    file = "users.db"
    if os.path.exists(file) :
        users = getUsers()
        userss = []
        print("Compress Users List ...")
        with alive_bar(len(users)) as bar:
            for u in users:
                phone = u[5]
                name = u[1]
                narr = name.split()
                N = narr[0]
                farr = narr[1:]
                F=""
                for i in farr:
                    F += i
                
                userss.append([N,F,phone])
                bar()    

        makeVCF(userss)    
    else:
        print("DATABASE NOT EXISTS\n PROGRAM CLOSED!")

#============= VCF FILE WRITE
def makeVCF(users):
    t = []
    print("CREATE ARRAY OF INFORMATION READY")
    with alive_bar(len(users)) as bar:
        for index,user in enumerate(users):
            t.append('BEGIN:VCARD')
            t.append('VERSION:2.1')
            t.append(f'N;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:;{user[1]};{user[0]};;;')
            t.append(f'FN;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:;{user[0]} {user[1]}')
            t.append(f'TEL;CELL:{user[2]}')
            t.append(f'REV:{(index + 1)}')
            t.append('END:VCARD')
            bar()
    with open("contacts.vcf", 'w',encoding='UTF-8') as f:
        f.writelines([l + '\n' for l in t])
    print("FILE WRITED SUCCESSFULLY!")
    print("APP CLOSED")

#=========== BEGINING OF PROGRAM
if __name__ == "__main__":
    main()
