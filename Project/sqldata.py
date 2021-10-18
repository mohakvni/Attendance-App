import mysql.connector
import pickle
import os
from datetime import date
import webbrowser

if os.path.isfile("Login details.bin") == True:
    f = open("Login Details.bin", "rb")
    L = pickle.load(f)
    usern = L[0]
    passw = L[1]
    db = L[2]
    f.close()
else:
    print("You Login details haven't been saved/created")
    usern = input("Enter UserName:")#username of your mysql database :root
    passw = input("Enter Password:")
    db = input("Please name your database:")
    save = input("Do you want to save your password? <Y/N>:")
    if save == "Y" or "yes" or "y":
        f = open("Login details.bin", "ab")
        L = [usern, passw, db]
        pickle.dump(L, f)
        f.close()
mydb = mysql.connector.connect(
        host="localhost",
        user=f"{usern}",
        password=f"{passw}")

mycursor = mydb.cursor(buffered=True)
mycursor.execute(f"CREATE Database if not exists {db}")
mycursor.execute(f"use {db}")
mycursor.execute("CREATE table  if not exists Student(Adno integer PRIMARY KEY, Name Varchar(35) NOT NULL)")
mycursor.execute("CREATE table  if not exists class(Adno integer PRIMARY KEY,Name Varchar(35) NOT NULL, attendance char(1) default 'A' )")
mycursor.execute("CREATE TABLE if not exists Datesheet(Adno integer PRIMARY KEY, Name Varchar(35) NOT NULL) ")
def ddmmyy(date, splitsym, Underscore=False,same=False):
    L = str(date).split(f"{splitsym}")
    if Underscore == True and same==False:
        dmydate = L[2] + "_" + L[1] + "_" + L[0]
    elif Underscore == False and same==False:
        dmydate = L[2] + "-" + L[1] + "-" + L[0]
    elif Underscore == False and same == True:
        dmydate = L[0] + "-" + L[1] + "-" + L[2]
    return (dmydate)

def dateadder_ds():
    tdate = date.today()
    formatdate = ddmmyy(tdate,"-",True)
    mycursor.execute("Describe Datesheet")
    L = []
    flag=0
    for i in mycursor:
        L.append(i[0])
    for j in range(len(L)):
        if str(formatdate) in L:
            flag=1
            break
        else:
            flag=0
    if flag==0:
        mycursor.execute(f"Alter Table Datesheet ADD {str(formatdate)} char(1) Default 'A' ")
dateadder_ds()
def add_rec(temp):
    tdate=date.today()
    formatdate = ddmmyy(tdate, "-", True)
    for i in range(len(temp)):
        mycursor.execute(f"INSERT into Student Values ('{temp[i][0]}', '{temp[i][1]}')")
        mydb.commit()
        mycursor.execute(f"INSERT into Datesheet(adno,name,{formatdate}) Values ('{temp[i][0]}', '{temp[i][1]}','A')")
        mydb.commit()
        mycursor.execute(f"INSERT into class Values ('{temp[i][0]}','{temp[i][1]}','A')")
        mydb.commit()
def delrecord(d):
    if type(d)==str:
        mycursor.execute(f"delete from Student where name='{d}'")
        mydb.commit()
        mycursor.execute(f"delete from class where name='{d}'")
        mydb.commit()
        mycursor.execute(f"delete from Datesheet where name='{d}'")
        mydb.commit()
    else:
        mycursor.execute(f"delete from Student where adno='{d}'")
        mydb.commit()
        mycursor.execute(f"delete from class where adno='{d}'")
        mydb.commit()
        mycursor.execute(f"delete from datesheet where adno='{d}'")
        mydb.commit()
def extract_cls():
    mycursor.execute("select * from class")
    data=mycursor.fetchall()
    return data
def extract_ds():
    table=[]
    mycursor.execute("Describe Datesheet")
    L = []
    for i in mycursor:
        L.append(i[0])
    for j in range(2,len(L)):
        L[j]=ddmmyy(L[j],"_",False,True)
    table.append(L)
    mycursor.execute("select * from datesheet")
    for k in mycursor:
        table.append(list(k))
    return table
def update_A(record):
    tdate = date.today()
    formatdate = ddmmyy(tdate, "-", True)
    if type(record) == str:#for name
        mycursor.execute(f"Update class set attendance='A' where name='{record}'")
        mydb.commit()
        mycursor.execute(f"Update Datesheet set {formatdate}='A' where name='{record}'")
        mydb.commit()
    else:#for adno
        mycursor.execute(f"Update class set attendance='A' where adno='{record}'")
        mydb.commit()
        mycursor.execute(f"Update Datesheet set {formatdate}='A' where adno='{record}'")
        mydb.commit()
def update_P(record):
    tdate = date.today()
    formatdate = ddmmyy(tdate, "-", True)
    if type(record) == str:
        mycursor.execute(f"Update class set attendance='P' where name='{record}'")
        mydb.commit()
        mycursor.execute(f"Update Datesheet set {formatdate}='P' where name='{record}'")
        mydb.commit()
    else:
        mycursor.execute(f"Update class set attendance='P' where adno='{record}'")
        mydb.commit()
        mycursor.execute(f"Update Datesheet set {formatdate}='P' where adno='{record}'")
        mydb.commit()
def downcsv():
    urldown = 'https://docs.google.com/spreadsheets/d/1voI_yrt4p0Sz5sjYYZ8FnclIPj1b0nBNNimuenB-l_Y//export?format=csv&gid=1965412432'
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open(urldown)