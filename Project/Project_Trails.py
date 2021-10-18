import csv
from columnar import columnar
from backend import sqldata, dayfinder as df
import webbrowser
from datetime import date
import os
import sys
import time
def ddmmyy(date, splitsym, Underscore=False,same=False):
    L = str(date).split(f"{splitsym}")
    if Underscore == True and same==False:
        dmydate = L[2] + "_" + L[1] + "_" + L[0]
    elif Underscore == False and same==False:
        dmydate = L[2] + "-" + L[1] + "-" + L[0]
    elif Underscore == False and same == True:
        dmydate = L[0] + "-" + L[1] + "-" + L[2]
    return (dmydate)

def datesheet():
    ds=sqldata.extract_ds() #ds is datasheet
    c=input("Do you want to view the datesheet as a csv file?<If so , press Y>")
    if c=="y" or c=="Y":
        f=open(r"C:\Users\user\Desktop\attendance.csv","w")
        csvw=csv.writer(f)
        for i in range(len(ds)):
            if i == 0:
                ds[i].insert(1,"R.no")
                csvw.writerow(ds[i])
            else:
                ds[i].insert(1,i)
                csvw.writerow(ds[i])
        f.close()
        data=[]
        for i in range(len(ds)):
            if i == 0:
                header=["S.no", *ds[i]]
            else:
                L=[i,*ds[i]]
                data.append(L)
        table = columnar(data, header, no_borders=True)
        print(table)

    else:
        data = []
        for i in range(len(ds)):
            if i == 0:
                header = ["S.no", *ds[i]]
            else:
                L = [i, *ds[i]]
                data.append(L)
        table = columnar(data, header, no_borders=True)
        print(table)

def addstu():
    n=int(input("Please enter the number of students to be added:"))
    flag=1
    try:
        for i in range(n):
            sd = input(
                "Enter the student's admission number and Name separated by comma(eg:111,Ram):")  # 'sd' stands for StudentDetails(adno,name)
            stu = sqldata.extract_cls()
            for j in range(len(stu)):
                if sd.split(",")[0] == str(stu[j][0]):
                    flag = 0
                    break
                else:
                    flag = 1
            if sd != '' and flag == 1:
                temp = [[sd.split(",")[0], sd.split(",")[1]]]
                print("The student,", sd.split(",")[1], ",has been successfully added to your list")
                sqldata.add_rec(temp)
            else:
                print("adno already exists")
    except:
        print("Incorrect input")

def delstu():
    stu = sqldata.extract_cls()
    delc = input("Do you want to input name(Then type N) or adno(Then type A) of the student to be deleted")#delc stands for del choice
    if delc =="N" or delc == "n":
        dn = input("Enter the name of the student to be deleted(Press 0 to Exit):")  # dn stands for deletedname
        while dn != "0":
            flag = 0
            for i in range(len(stu)):
                if stu[i][1] == dn:
                    sqldata.delrecord(dn)
                    stu = sqldata.extract_cls()
                    print("The student named", dn, "has been successfully removed from your list")
                    flag = 1
                    break
            if flag == 0:
                print("The name", dn, "does't exist")
                dn = input("Input correct name(Press 0 to Exit):")
            else:
                dn = input(
                    "Enter the name of the student to be deleted(Press 0 to Exit):")  # dn stands for deletedname
    elif delc =="A" or delc =="a":
        da=int(input("Enter the admission no of the student to be deleted(Press 0 to Exit):"))
        while da != 0:
            flag = 0
            for i in range(len(stu)):
                if stu[i][0] == da:
                    sqldata.delrecord(da)
                    stu = sqldata.extract_cls()
                    print("The student with adno", da, "has been successfully removed from your list")
                    flag = 1
                    break
            if flag == 0:
                print("The adno", da, "does't exist")
                da = int(input("Input correct adno(Press 0 to Exit):"))
            else:
                da = int(input("Enter the adno of the student to be deleted(Press 0 to Exit):"))  # dn stands for deletedname
    else:
        print("wrong ans")
def markabs():
    stu = sqldata.extract_cls()
    abc=input("Do you want to input name(Then type N) or adno(Then type A) of the student to be marked absent")#abc stands for absent choice
    if abc=="N" or abc=="n":
        abn = input("Enter the names of the Students to be marked present(Make sure to separate them by commas):")
        abl = abn.split(",")
        flag = 0
        for i in abl:
            for j in range(len(stu)):
                if i == stu[j][1]:
                    sqldata.update_A(i)
                    flag = 1
                    stu = sqldata.extract_cls()
                    break
            if flag == 0:
                print("The name", i, "does't exist")
                corabn = input("Input correct name(s):")  # corabn==correct absent name
                abl.append(corabn)
        print("Respective students have been successfully marked as absent.")
    elif abc=="a"or abc=="A":
        abn = input("Enter the Adno of the Students to be marked present(Make sure to seperate them by commas):")
        abl = abn.split(",")
        flag = 0
        for i in abl:
            for j in range(len(stu)):
                if int(i) == stu[j][0]:
                    sqldata.update_A(int(i))
                    flag = 1
                    stu = sqldata.extract_cls()
                    break
            if flag == 0:
                print("The adno", i, "does't exist")
                corabn = input("Input correct adno:")  # corabn==correct absent name
                abl.append(corabn)
        print("Respective students have been successfully marked as absent.")
def markprsnt():
    stu = sqldata.extract_cls()
    prc=input("Do you want to input name(Then type N) or adno(Then type A) of the student to be marked present")#abc stands for present choice
    if prc=="N" or prc=="n":
        prn = input("Enter the names of the change attendance  to present(Make sure to separate them by commas):")
        prl = prn.split(",")
        flag = 0
        for i in prl:
            for j in range(len(stu)):
                if i == stu[j][1]:
                    sqldata.update_P(i)
                    flag = 1
                    stu = sqldata.extract_cls()
                    break
            if flag == 0:
                print("The name", i, "does't exist")
                corprn = input("Input correct name:")  # corprl==correct present name
                prl.append(corprn)
        print("Respective students have been successfully marked as present.")
    elif prc=="a"or prc=="A":
        prn = input("Enter the Adno of the absentees(Make sure to seperate them by commas):")
        prl = prn.split(",")
        flag = 0
        for i in prl:
            for j in range(len(stu)):
                if int(i) == stu[j][0]:
                    sqldata.update_P(int(i))
                    flag = 1
                    stu = sqldata.extract_cls()
                    break
            if flag == 0:
                print("The adno", i, "does't exist")
                corprn = input("Input correct adno:")
                prl.append(corprn)
        print("Respective students have been successfully marked as present.")
def displaystu():
    tdate = date.today()
    ymd = str(tdate).split("-")
    y=int(ymd[0])
    m=int(ymd[1])
    d=int(ymd[2])
    formatdate = ddmmyy(tdate, "-", False)
    stu = sqldata.extract_cls()
    if stu == []:
        print("You haven't entered any student names yet!!!!")
    else:
        header=["Sno","Adno","Name","Attendance","Date","Day"]
        data = []
        for i in range(len(stu)):
            L=[i + 1 , *stu[i] , formatdate, df.dayfinder(y,m,d)]
            data.append(L)
            #!!!!!TO work on modifying the attendance daily
        table = columnar(data, header, no_borders=True)
        print(table)
def getlink():
    #instructions to be elegantly presented
    print('''Copy and paste the below link in zoom chat window:
    \"https://docs.google.com/forms/d/e/1FAIpQLSc33SalOxg-wzhqWQRoPkmV5wn8P5C67LnZ6_d3stQ51ykwKw/viewform?usp=sf_link\" ''')
def autocheck():
    char={"m":2,"d":2}
    sqldata.downcsv()
    time.sleep(5)
    tdate = date.today()
    ymd = str(tdate).split("-")
    if ymd[2][0]=="0":  #for the month
        ymd[2]=ymd[2][1]
        char["m"]=1
    if ymd[1][0]=="0":  #for the day
        ymd[1]=ymd[1][1]
        char["d"]=1
    val=6+char["m"]+char["d"]
    mdystr=ymd[1]+"/"+ymd[2]+"/"+ymd[0]
    f = open(r'D:\Downloads M\Attendance (Responses) - Form Responses 1.csv', "r")#!!!!!!for trails i used my default download path but genarally it is C:\Downloads
    csvr = csv.reader(f)
    stu = sqldata.extract_cls()
    for j in range(len(stu)):
        for i in csvr:
            d=i[0][0:val]
            if d == mdystr:
                try:
                    if stu[j][0] == int(i[1]):
                        sqldata.update_P(int(stu[j][0]))
                        break
                    else:
                        sqldata.update_A(int(stu[j][0]))
                except:
                    sqldata.update_A(int(stu[j][0]))
            else:
                sqldata.update_A(int(stu[j][0]))
        f.seek(0)
    print("Attendance has been taken")
    displaystu()
    f.close()
def editwebdata():
    urledit = 'https://docs.google.com/spreadsheets/d/1voI_yrt4p0Sz5sjYYZ8FnclIPj1b0nBNNimuenB-l_Y/edit#gid=1965412432'
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open(urledit)

def automate():
    getlink()
    print("for Auto-attendance pls wait until class is over or all students have completed form filling")
    print("Please Select the Suboptions:\n"
          "a)Autoattendance\n"
          "b)edit the webserver data\n")
    autochoice=input("Enter a or b:")
    if autochoice=="a"or autochoice=="A":
        autocheck()
    elif autochoice=="b" or autochoice=="B":
        editwebdata()

def usermanual():
    print('''
    Using this Program you can perform the following functions:
    1.Automation**
    2.Mark Absent(Essentially you have to enter the name of the absentees , the rest will be marked present automatically)
    3.Change attendance from absent to present(if you by mistake entered someone absent then make it present)
    4.See the List of students(**MAKE SURE TO RUN FUNCTION 1 BEFORE RUNNING FUNCTION 4 TO GET TODAY'S ATTENDANCE)
    5.View Datesheet
    6.Add Student (This function adds the name of the student to your list)
    7.Delete Student(This function removes the  student from your list)
    8.User Manual
    When this code is executed, you will get an output screen requesting for the 
    choice number which is as indexed above. So Input the number of the function you want to execute. 
     ''')

def CHOICE():
        try:
            choice = int(input("Enter the Command Number of your choice(Press 0 to end):"))
            if choice==0:
                if os.path.isfile(r'D:\Downloads\Attendance (Responses) - Form Responses 1.csv') == True:
                    os.remove(r'D:\Downloads\Attendance (Responses) - Form Responses 1.csv')
                os.execv(sys.executable, ['python'] + sys.argv)  # terminates the program
            if choice == 1:
                automate()
            elif choice == 2:
                markabs()
            elif choice == 3:
                markprsnt()
            elif choice == 4:
                displaystu()
            elif choice == 5:
                datesheet()
            elif choice == 6:
                addstu()
            elif choice == 7:
                delstu()
            elif choice== 8:
                usermanual()
            else:
                print("Error")
        except ValueError:
            print("Incorrect Input")


temp = []  # this is the temporary list for storing and accessing data
stu = sqldata.extract_cls()
print('''Welcome to AttendanceTaker 1.0. This is a project developed using python by Meher, Ethan and Mohak.
Next few lines will give you options on what function you want to use. The User manual will give you an overview on how to run through the program.''')
print("These are few operations that you can perform using the student attendance management system.")
print('''
    1.Automation**
    2.Mark Absent(Essentially you have to enter the name of the absentees , the rest will be marked present automatically)
    3.Change attendance from absent to present(if you by mistake entered someone absent then make it present)
    4.See the List of students(**MAKE SURE TO RUN FUNCTION 1 BEFORE RUNNING FUNCTION 4 TO GET TODAY'S ATTENDANCE)
    5.View Datesheet
    6.Add Student (This function adds the name of the student to your list)
    7.Delete Student(This function removes the  student from your list)
    8.User Manual ''')
while True:
    CHOICE()