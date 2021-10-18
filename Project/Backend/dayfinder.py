def dayfinder(y,mon,date):
    if ((y // 100) % 4 == 0):
        cencode = 6
    elif ((y // 100) % 4 == 1):
        cencode = 4
    elif ((y // 100) % 4 == 2):
        cencode = 2
    elif ((y // 100) % 4 == 3):
        cencode = 0
    if (mon==1):
        moncode=0
    elif (mon==2):
        moncode=3
    elif (mon==3):
        moncode=3
    elif (mon==4):
        moncode=6
    elif (mon==5):
        moncode=1
    elif (mon==6):
        moncode=4
    elif (mon==7):
        moncode=6
    elif (mon==8):
        moncode=2
    elif (mon==9):
        moncode=5
    elif (mon==10):
        moncode=0
    elif (mon==11):
        moncode=3
    elif (mon==12):
        moncode=5
    a=y%100 
    if (a%4!=0):
        daycode=(a+cencode+moncode+a//4+date)%7
    elif a%4==0 and mon==1 : 
        daycode=(a+cencode+moncode+a//4+date-1)%7
    elif a%4==0 and mon==2 :
        daycode=(a+cencode+moncode+a//4+date-1)%7
    else:
        daycode=(a+cencode+moncode+a//4+date)%7
    if (daycode==0):
        day=("SUNDAY")
    if (daycode==1):
        day=("MONDAY")
    if (daycode==2):
        day=("TUESDAY")
    if (daycode==3):
        day=("WEDNESDAY")
    if (daycode==4):
        day=("THURSDAY")
    if (daycode==5):
        day=("FRIDAY")
    if (daycode==6):
        day=("SATURDAY")

    return day
