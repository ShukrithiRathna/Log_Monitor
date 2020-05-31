import pandas as pd
import re
from datetime import datetime,timedelta
import calendar

def reboot_convert(infile,outfile):
    def convert_to_session(time_str):
        score=0
        month = {v: k for k,v in enumerate(calendar.month_abbr)}
        check=(time_str.replace("\t"," "))

        # checking for older sessions
        if check.find("-")>0:
            score=1 
            temp = check.split("-")
            temp_start=temp[0].split(" ")
            temp_end=temp[1].split("(")
            delta = temp_end[1][0:-2]

             #+ problem in sessions that last less than a day
            if delta.find("+") >0:
                session_days= delta.split("+")
                deltime = session_days[1].split(":")
                end_day=session_days[0]

            else:
                end_day=0
                deltime = delta.split(":")

        # if session is still running
        else: 
            temp_start=re.split("\s", check,4)

        # extra space problem in single digit dates
        if(len(temp_start))==6:
            temp_start.pop(2)
    
        start_time = temp_start[3].split(":")
        start_date = datetime(year=2020, month=month[temp_start[1]], day=int(temp_start[2]), hour=int(start_time[0]), minute=int(start_time[1]))

        if score==1: 
            duration=timedelta(days=int(end_day), hours=int(deltime[0]), minutes=int(deltime[1]))
            end_date = start_date + duration
        else:
            end_date=datetime.now()
            duration=(end_date-start_date)

        row=[start_date,end_date, duration]
        return row

    file = open(infile) 
    lines = file.readlines()
    lines = lines[:-3]
    reboot_data=pd.DataFrame(columns=['Action','Version','Start_time','End_time','Session_duration'])
    for item in lines:
        # row=[]
        action=(item[:20])

        x = re.split("\s", str(item[21:]),1)
        temp=re.split("\s", x[1],1)

        version=(temp[0])
        check=str(temp[1])
        times=convert_to_session(temp[1])
        start_time=times[0]
        end_time=times[1]
        session=times[2]    
        row=[action,version,start_time,end_time,session]
        # print(row)
        reboot_data=reboot_data.append(pd.Series(row,index=reboot_data.columns),ignore_index=True)

    reboot_data.to_csv(outfile)
# reboot_data.head()

def auth_convert(infile,outfile):
    def convert_to_timestamp(temp):
    # print(type(temp))
        try:
            date = datetime.strptime(temp,"%b %d %H:%M:%S")
            date = date.replace(year=2020)
            return date
        except (ValueError):
            x=re.search("[A-N]",temp)
            pos=x.start()
            # convert_to_timestamp(temp[pos+1:])
            date = datetime.strptime(temp[pos:-1],"%b %d %H:%M:%S")

            date = date.replace(year=2020)
            return date
    file = open(infile) 
    # print(f.readline())
    user = []
    key=[]
    message = []
    timestamp = []
    for item in file:
        # print(type(item))
        timestamp.append(item[:15])
        x = re.split("\s", str(item[16:]),1)
        temp=re.split(":", x[1],1)
        user_temp=x[0]
        y=re.search("[\'\"]",user_temp)
        if(y==None):
            user.append(user_temp)
        else:
            pos=y.start()
        # print(pos)
            user.append(user_temp[pos+1:])
        key.append(temp[0])
        msg_temp=str(temp[1:]).strip('[]') 
        message.append(msg_temp)
    timestamp = [convert_to_timestamp(str(item)) for item in timestamp]
    output = pd.DataFrame(list(zip(timestamp,user,key,message)),columns=['Time','User','Key/Agent' ,'Message'])
    output.to_csv(outfile)
    
def kern_convert(infile,outfile):
    def convert_to_time_stamp(time_str, year_str):
        month = {v: k for k,v in enumerate(calendar.month_abbr)}
        check=(time_str.replace("\t"," "))
        check=check.rstrip()
        temp_start=re.split("\s", check,4)
        start_time = re.split(":", temp_start[2],2)
        date = datetime(year=int(year_str), month=month[temp_start[0]], day=int(temp_start[1]), hour=int(start_time[0]), minute=int(start_time[1]))
        return(date)

    file = open('LogFiles/kern_error.txt') 
    # print(f.readline())
    user = []
    key=[]
    message = []
    timestamp = []
    output = pd.DataFrame(columns=['Time','User','Message'])
    for item in file:
        # print(type(item))
        timestamp=(item[:15])
        timestamp = convert_to_time_stamp(timestamp,'2020')
        x = re.split(":", str(item[16:]),1)
        temp=re.split("\s", x[1],1)
        user_temp=x[0]
        y=re.search("[\'\"]",user_temp)
        if(y==None):
            user=(user_temp)
        else:
            pos=y.start()
            user=(user_temp[pos+1:])
        message=(temp[-1])
        row=[timestamp, user, message]
        output=output.append(pd.Series(row,index=output.columns),ignore_index=True)


    output.to_csv(outfile)
  
def login_convert(infile,outfile):
    def convert_to_time_stamp(time_str, year_str):
        month = {v: k for k,v in enumerate(calendar.month_abbr)}
        check=(time_str.replace("\t"," "))
        check=check.rstrip()
        temp_start=re.split("\s", check,4)
        if(len(temp_start))==5:
                temp_start.pop(2)
        start_time = re.split(":", temp_start[3],2)
        date = datetime(year=int(year_str), month=month[temp_start[1]], day=int(temp_start[2]), hour=int(start_time[0]), minute=int(start_time[1]))
        return(date)

    file = open(infile) 

    lines = file.readlines()
    lines = lines[1:]

    user = []
    key=[]
    message = []
    username = []

    login_data=pd.DataFrame(columns=['Username','Port','Login_Time'])
    for item in lines:
        temp=re.split("\s",str(item),1)
        username = (temp[0])

        z=re.search("\*",temp[1])
        try:
            pos_login=z.start()
            login_port='None'
            # From='None'
            login_time = 'Not logged in'

        except (AttributeError ):
            x=re.search("[A-Z]",temp[1])
            pos=x.start()
            temp_login_time=re.split("\+",str(temp[1][pos:-1]),1)
            # print(temp_login_time)
            login_time=temp_login_time[0]
            year_temp=re.split("\s",str(temp_login_time[1]),1)
            login_year=year_temp[1]
            login_time=convert_to_time_stamp(login_time,login_year)
            # print(login_year)

            y=re.search("[a-z]",temp[1][0:pos])
            temp_port=temp[1][0:pos]
            login_port=temp_port[y.start():-1]
            login_port=login_port.rstrip()

        row=[username, login_port, login_time]
        login_data=login_data.append(pd.Series(row,index=login_data.columns),ignore_index=True)

    login_data.to_csv(outfile)
 
def syslog_convert(infile,outfile):
    def convert_to_timestamp(temp):
        try:
            date = datetime.strptime(temp,"%b %d %H:%M:%S")
            date = date.replace(year=2020)
            return date
        except (ValueError):
            x=re.search("[A-N]",temp)
            pos=x.start()
            # convert_to_timestamp(temp[pos+1:])
            date = datetime.strptime(temp[pos:-1],"%b %d %H:%M:%S")

            date = date.replace(year=2020)
            return date
    file = open('LogFiles/sys_log.txt', "rb") 
    # print(f.readline())
    user = []
    key=[]
    message = []
    timestamp = []
    for item in file:
        # print(type(item))
        timestamp.append(item[:15])
        x = re.split("\s", str(item[16:]),1)
        temp=re.split(":", x[1],1)
        user_temp=x[0]
        y=re.search("[\'\"]",user_temp)
        if(y==None):
            user.append(user_temp)
        else:
            pos=y.start()
        # print(pos)
            user.append(user_temp[pos+1:])
        key.append(temp[0])
        msg_temp=str(temp[1:]).strip('[]') 
        message.append(msg_temp)
    timestamp = [convert_to_timestamp(str(item)) for item in timestamp]
    output = pd.DataFrame(list(zip(timestamp,user,key,message)),columns=['Time','User','Key/Agent' ,'Message'])
    output.to_csv(outfile)
