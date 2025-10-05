#this file contains all functions
import smtplib
from random import randint
from flask import request, session
import mysql.connector as sqltor
from datetime import date
from dateutil.relativedelta import relativedelta

#general fns

def chpwd(pwd):
    uc=lc=dc=sp=0
    a=len(pwd)>8
    for i in range(len(pwd)):
        if pwd[i].isdigit():
            dc+=1
        elif pwd[i].isupper():
            uc+=1
        elif pwd[i].islower():
            lc+=1
        else:
            sp+=1
    if dc and uc and lc and sp and a:
        return True
    else:
        return False
    

#sql fns

mycon=sqltor.connect(host='localhost',user='root1',password='12345',database='shimmy_shimmy_bank',autocommit=True)
cursor=mycon.cursor()

def s_sql():
    global mycon,cursor
    mycon=sqltor.connect(host='localhost',user='root1',password='12345',database='shimmy_shimmy_bank',autocommit=True)
    cursor=mycon.cursor()
    return mycon,cursor


def c_sql():
    global mycon
    mycon.close()
    return mycon

def add_user_sql(user):
    global mycon,cursor
    cursor.execute("insert into users values(%s, %s, %s, %s, %s, %s,'-1')", (user['cid'], user['name'], user['aadhaar'], user['email'], user['age'], user['password']))
    return user
    
def check_login(user):
    global mycon,cursor
    try:
        cursor.execute('select cid, password from users where cid={}'.format(user['cid'],user['password']))
        data=cursor.fetchone()
        if data==(user['cid'],user['password']):
            return True
        else:
            return False
    except:
        return False
    
def add_sb(user):    
    global mycon,cursor
    cursor.execute('update users set sb=%s where cid="%s"'%(user['sb'],user['cid']))
    cursor.execute(f'create table t_sb_{user["cid"]}(date datetime ,amount int, particular enum("Deposit","Withdrawal"), balance int default 0, tid int, To_From char(6) default "Self")')
    return user
    


def add_c_loan(user):  
    global mycon,cursor
    q='insert into h_loans values("%s",%s,%s,%s,curdate(),"%s")'%(user['cid'],user['h_loan']['amt'],user['h_loan']['tp'],user['h_loan']['interest'],date.today()+relativedelta(months=user['h_loan']['tp']))  
    cursor.execute(q)      
    session['c_loan']=True
    return user 
    
def add_h_loan(user): 
    global mycon,cursor   
    #cid, hl, h_amt, h_tp, interest, start date, close date   
    q='insert into h_loans values("%s",%s,%s,%s,curdate(),"%s")'%(user['cid'],user['h_loan']['amt'],user['h_loan']['tp'],user['h_loan']['interest'],date.today()+relativedelta(months=user['h_loan']['tp']))  
    cursor.execute(q)
    session['h_loan']=True
    return user 

def get_info_login(user):
    global mycon,cursor
    try:
        cursor.execute('select * from users where cid ={}'.format(user['cid']))
        data=list(cursor.fetchone())
        a=['cid','name','aadhar','email','age','password','sb']
        user=dict(zip(a,data))
        return user 
    except:
        return False
    
    
def get_t_sb(user):
    global mycon,cursor
    cursor.execute('select * from t_sb_{}'.format(user['cid']))
    data=cursor.fetchall()[::-1]
    cursor.execute(f'select balance from t_sb_{user["cid"]} where date=(select max(date) from t_sb_{user["cid"]})')
    a=cursor.fetchall()
    if a:
        a=a[0][0]
    else:
        a=0
    session['user']['sb_b']=a
    return data
    ##except:
       ## return []

    
def check_sb(user):
    global mycon,cursor
    try:
        cursor.execute('select sb form users where cid="{}"'.format(user['cid']))
        d=int(cursor.fetchone())
        if d!=-1:
            session['user']['sb']=d    
        return user
    except:
        return False
    
def check_sb_t(user):
    global mycon,cursor
    try:
        cursor.execute('select sb form users where cid="{}"'.format(user))
        d=int(cursor.fetchone())
        if d:
            return user    
        else:
            return False
    except:
        return False

def sb_t(reciever,amt,user):
    global mycon,cursor
    cursor.execute('select sb from users')
    if (str(reciever),) not in cursor.fetchall():
        print('not found')
        session['t_user_not_found']=True
        return False
    cursor.execute(f'select balance from t_sb_{user["cid"]} where date=(select max(date) from t_sb_{user["cid"]})')
    a=cursor.fetchall()
    if a:
        a=a[-1][0]
    else:
        a=0
    if amt>a:
        session['insufficient_funds']=True
        return False
    else:
        #table - date, amt, particular, balance,cid
        tid=randint(1000,9999)
        cursor.execute('select cid from users where sb=%s'%(reciever))
        x=cursor.fetchone() # reciver cid
        x=''.join(x)
        q=f'insert into t_sb_{user['cid']}'
        q+=' values(sysdate(),%s,2,%s,%s,"%s")'%(amt,a-amt,tid,reciever)
        cursor.execute(q)
        cursor.execute(f'select balance from t_sb_{x}')
        z=cursor.fetchall()
        if not z:
            z=0
        z=z[-1]
        z=int(z[0])
        cursor.execute('select sb from users where cid="%s"'%(user['cid']))
        e=cursor.fetchall()[-1][0]
        q=f'insert into t_sb_{x}'
        q+=' values(sysdate(),%s,1,%s,%s,%s)'%(amt,amt+z,tid,e)
        cursor.execute(q)
        session['s_transfer']=True
        return True

def withdraw_(user,amt):
    global mycon,cursor
    cursor.execute(f'select balance from t_sb_{user["cid"]}')
    a=cursor.fetchall()
    if a:
        a=int(a[-1][0])
    else:
        a=0
    if amt>a:
        session['s_withdraw']=False
        return False
    else:
        #table - date, amt, particular, balance,cid, to
        tid=randint(1000,9999)
        q=f'insert into t_sb_{user['cid']}'
        q+=' values(sysdate(),%s,2,%s,%s,"Self")'%(amt,a-amt,tid)
        cursor.execute(q)
        session['s_withdraw']=True
        return True

def deposit_(user,amt):
    global mycon,cursor
    tid=randint(1000,9999)
    cursor.execute(f'select balance from t_sb_{user["cid"]}')
    a=cursor.fetchall()
    if not a:
        a=0
    else:
        a=a[-1]
        a=int(a[0])
    # table - date , amt, particular, balance,tid,to_from
    q=f'insert into t_sb_{user['cid']}'
    q+=' values(sysdate(),%s,1,%s,%s,"Self")'%(amt,a+int(amt),tid)
    session['deposit_']=True
    cursor.execute(q)
    
def get_reciever_id(bn_no):
    global mycon, cursor
    cursor.execute('select email from users where sb=%s'%(bn_no))
    return cursor.fetchall()
    
def h_loan_transfer(user):
    tid=randint(1000,9999)
    cursor.execute(f'select balance from t_sb_{user['cid']} where date=(select max(date) from t_sb_{user['cid']})')
    d=cursor.fetchall()
    if not d:
        amt=0
    else:
        amt=d[0][0]
    print('balance:',amt,'loanamt:',user['h_loan']['amt'])                     #date, amt, particular,balance, tid, to/from
    q=f'insert into t_sb_{user["cid"]} values(sysdate(),%s,1,%s,%s,"Loan")'
    r=(user['h_loan']['amt'],user['h_loan']['amt']+amt,tid)
    cursor.execute(q,r)
    return user

def c_loan_transfer(user):
    tid=randint(1000,9999)
    cursor.execute(f'select balance from t_sb_{user['cid']} where date=(select max(date) from t_sb_{user['cid']})')
    d=cursor.fetchall()
    amt=d[0][0]                     #date, amt, particular,balance, tid, to/from
    cursor.execute(f'insert into t_sb_{user["cid"]} values(sysdate(),%s,1,%s,%s,"Loan")'%(user['c_loan']['amt'],user['c_loan']['amt']+amt,tid))
    return user    

#smtp fns


def send_mail_ver(s_email):
    email='shimmy.shimmy.bank@gmail.com'
    otp=randint(1000,9999)
    a='ofbi nazq fwmd ujmr'
    subject='Verification code for account creation at shimmy shimmy bank'
    message=f'''Hello {s_email}!!
 We have recieved a request to create an account at Shimmy Shimmy bank.
 Here is the verification code: {otp}
 Regards,
 Shimmy Shimmy Bank.'''
    text=f'''Subject: {subject}

 {message}
This is a system generated email. Please do not reply'''
    try:
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(email, a)
        server.sendmail(email, s_email, text)
        print('Email has been sent.',otp)
        return otp
    except :
        return False
 

def send_mail_acc(user):
    email='shimmy.shimmy.bank@gmail.com'
    a='ofbi nazq fwmd ujmr'
    cid=user['cid']
    subject='Confirmation of account creation'
    message=f'''Hello {user['email']}\nWe are happy to welcome you to Shimmy Shimmy Bank!!
This is your customer id: {cid}
Please keep your customer id confidential as it will be used to login into our webpage.
Regards,
Shimmy Shimmy Bank Team
This is a system generated email. Please do not reply.'''
    text=f'Subject: {subject}\n{message}'
    try:
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(email, a)
        server.sendmail(email, user['email'], text)
        return cid
    except:
        return False

def send_mail_sb(user):
    email='shimmy.shimmy.bank@gmail.com'
    a='ofbi nazq fwmd ujmr'
    cid=user['cid']
    user['sb_acc']=randint(10000,99999)
    subject='Creation of savings bank account'
    message=f'''Hello {user['email']}\nWe are happy to confirm your creation of your savings bank account under the customer id:{user['cid']}
The account number is : {user['sb']}
Regards,
Shimmy Shimmy Bank Team
This is a system generated email. Please do not reply.'''
    text=f'Subject:{subject}\n{message}'
    try:
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(email, a)
        server.sendmail(email, user['email'], text)
        return user 
    except:
        return False
    
    
def send_mail_c_loan(user):
    email='shimmy.shimmy.bank@gmail.com'
    a='ofbi nazq fwmd ujmr'
    cid=user['cid']
    subject='Confirmation of car loan'
    message=f'''Hello {user['email']}\nWe are happy to confirm your Car loan under the customer id : {user['cid']}
The amount is : {user['c_loan']['amt']}
Regards,
Shimmy Shimmy Bank Team
This is a system generated email. Please do not reply.'''
    text=f'Subject:{subject}\n{message}'
    try:
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(email, a)
        server.sendmail(email, user['email'], text)
        return user
    except:
        return False
    
def send_mail_h_loan(user):
    email='shimmy.shimmy.bank@gmail.com'
    a='ofbi nazq fwmd ujmr'
    cid=user['cid']
    subject='Confirmation of home loan'
    message=f'''Hello {user['email']}\nWe are happy to confirm your Home loan under the customer id : {user['cid']}
The amount is : {user['h_loan']['amt']}
Regards,
Shimmy Shimmy Bank Team
This is a system generated email please do not reply'''
    text=f'Subject:{subject}\n{message}'
    try:
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(email, a)
        server.sendmail(email, user['email'], text)
        return user
    except:
        return False
    
def send_mail_w(user,amt):
    email='shimmy.shimmy.bank@gmail.com'
    a='ofbi nazq fwmd ujmr'
    cid=user['cid']
    subject='Confirmation of transaction'
    message=f'''Hello {user['email']}
A withdrawal of Rs {amt} has taken place.
Regards,
Shimmy Shimmy Bank Team
This is a system generated email. Please do not reply.'''
    text=f'Subject:{subject}\n{message}'
    try:
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(email, a)
        server.sendmail(email, user['email'], text)
        return user
    except:
        return False
    
def send_mail_d(email1,amt):
    email='shimmy.shimmy.bank@gmail.com'
    a='ofbi nazq fwmd ujmr'
    subject='Confirmation of transaction'
    message=f'''Hello {email1}
A deposit of Rs {amt} has taken place.
Regards,
Shimmy Shimmy Bank Team
This is a system generated email. Please do not reply.'''
    text=f'Subject:{subject}\n{message}'
    try:
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(email, a)
        server.sendmail(email,email1,text)
        return True
    except:
        return False