#this file contains all functions
import smtplib
from random import randint
from flask import request, flash, session
import mysql.connector as sqltor

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
 
def add_user_sql(user):
    mycon=sqltor.connect(host='localhost', user='root1', password='12345',database='shimmy_shimmy_bank')
    cursor=mycon.cursor()
    try:
        cursor.execute("insert into users values(%s, %s, %s, %s, %s, %s,-1)", (user['cid'], user['name'], user['aadhaar'], user['email'], user['age'], user['password']))
        mycon.commit()
        mycon.close()
        return user
    except:
        return False

def check_login(user):
    mycon=sqltor.connect(host='localhost', user='root1', password='12345',database='shimmy_shimmy_bank')
    cursor=mycon.cursor()
    try:
        cursor.execute('select cid, password from users where cid={}'.format(user['cid'],user['password']))
        data=cursor.fetchone()
        if data==(user['cid'],user['password']):
            flash('Succesfully logged in','info')
            return True
        else:
            flash('Password or customer id is wrong','error')
            return False
    except:
        return False
    
def add_sb(user):
    mycon=sqltor.connect(host='localhost', user='root1', password='12345',database='shimmy_shimmy_bank')
    cursor=mycon.cursor()
    print('inside add_sb')
   ## try:
    cursor.execute('update users set sb=%s where cid="%s"'%(user['sb'],user['cid']))
    print('executed one cursor statemnt')
    cursor.execute(f'create table t_sb_{user["cid"]}(date date,amount int, particular enum("Deposit","Withdrawal"), balance int default 0, tid int)')
    mycon.commit()
    mycon.close()
    flash('Savings account succesfully created!!','info')
    return user
    ##except:
        #####return False
    


def add_c_loan(user):
    mycon=sqltor.connect(host='localhost', user='root1', password='12345',database='shimmy_shimmy_bank')
    cursor=mycon.cursor()
    try:
        cursor.execute('insert into loans(cid, cl, c_amt, c_tp, c_interest) values("%s","yes",%s,%s)'%(user['cid'],user['loans']['amt'],user['loans']['tp'],user['loans']['interest']))
        mycon.commit()
        mycon.close()
        return user 
    except:
        return False
    
def add_h_loan(user):
    mycon=sqltor.connect(host='localhost', user='root1', password='12345',database='shimmy_shimmy_bank')
    cursor=mycon.cursor()
    try:
        cursor.execute('insert into loans(cid, hl, h_amt, h_tp, h_interest) values("%s","yes",%s,%s)'%(user['cid'],user['loans']['amt'],user['loans']['tp'],user['loans']['interest']))
        mycon.commit()
        mycon.close()
        return user 
    except:
        return False

def get_info_login(user):
    mycon=sqltor.connect(host='localhost', user='root1', password='12345',database='shimmy_shimmy_bank')
    cursor=mycon.cursor()
    try:
        cursor.execute('select cid, email, sb from users where cid ={}'.format(user['cid']))
        data=list(cursor.fetchone())
        a=['cid','email','sb']
        user=dict(zip(a,data))
        mycon.close()
        return user 
    except:
        return False
    
    
def get_t_sb(user):
    mycon=sqltor.connect(host='localhost', user='root1', password='12345',database='shimmy_shimmy_bank')
    cursor=mycon.cursor()
    try:
        cursor.execute(f'select * from t_sb_{user["cid"]} where cid ="%s"'%(user['cid'],))
        data=cursor.fetchall()
        mycon.close()
        return data
    except:
        return False        

def add_ccn(cn,cid):
    mycon=sqltor.connect(host='localhost', user='root1', password='12345',database='shimmy_shimmy_bank')
    cursor=mycon.cursor()
    try:
        cursor.execute('insert into cc values({},{},{},{}) where cid={}'.format(cid,cn['ccn'],cn['cvv'],cn['valid'],cid))
        mycon.commit()
        mycon.close()
        flash('Succesuflly generated credit card')
        return True
    except:
        return False    


    

def check_sb(user):
    mycon=sqltor.connect(host='localhost', user='root1', password='12345',database='shimmy_shimmy_bank')
    cursor=mycon.cursor()
    try:
        cursor.execute('select sb form users where cid="{}"'.format(user['cid']))
        d=int(cursor.fetchone())
        if d!=-1:
            session['user']['sb']=d    
        mycon.close()
        return user
    except:
        return False
    
def check_sb_t(user):
    mycon=sqltor.connect(host='localhost', user='root1', password='12345',database='shimmy_shimmy_bank')
    cursor=mycon.cursor()
    try:
        cursor.execute('select sb form users where cid="{}"'.format(user))
        d=int(cursor.fetchone())
        mycon.close()
        if d:
            return user    
        else:
            flash('Savings bank account not found','error')
            return False
    except:
        return False

def sb_t(reciever,amt,user):
    mycon=sqltor.connect(host='localhost', user='root1', password='12345',database='shimmy_shimmy_bank')
    cursor=mycon.cursor()
    cursor.execute(f'select balance from t_sb_{user["cid"]}')
    a=cursor.fetchall()[-1]
    a=a[0]
    if amt>a:
        flash('Insuffecient funds','i_f')
        return False
    else:
        #table - date, amt, particular, balance,cid
        tid=randint(1000,9999)
        q=f'insert into t_sb_{user['cid']}'
        q+=' values(curdate(),%s,2,%s,%s)'%(amt,a-amt,tid)
        cursor.execute(q)
        cursor.execute(f'select balance from t_sb_{reciever}')
        z=cursor.fetchone()
        if not z:
            z=0
        q=f'insert into t_sb_{reciever}'
        q+=' values(curdate(),%s,1,%s,%s)'%(amt,amt+z,tid)
        cursor.execute(q)
        mycon.commit()
        mycon.close()
    flash('Transfered successfully')
    return True

#smtp fns


def send_mail_ver(s_email):
    email='shimmy.shimmy.bank@gmail.com'
    otp=randint(1000,9999)
    a='ofbi nazq fwmd ujmr'
    subject='Verification code for account creation at shimmy shimmy bank'
    message=f'''Hello {s_email}!!
 We have recieved a request to create an account at Shimmy Shimmy bank
 Here is the verification code: {otp}
 Regards
 Shimmy Shimmy Bank'''
    text=f'''Subject: {subject}

 {message}
This is a system generated email please do not reply'''
    try:
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(email, a)
        server.sendmail(email, s_email, text)
        print('Email has been sent',otp)
        return otp
    except :
        return False
 

def send_mail_acc(user):
    email='shimmy.shimmy.bank@gmail.com'
    a='ofbi nazq fwmd ujmr'
    cid=user['cid']
    subject='Confrimation of account creation'
    message=f'''Hello {user['email']}\nWe are happy to welcome you to Shimmy Shimmy Bank!!
    This is your customer id: {cid}
Please keep your customer id confidential as it will be used to login into our webpage
Regards Shimmmy Shimmy Bank Team
This is a system generated email please do not reply'''
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
Regards Shimmy Shimmy Bank Team
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
    
    
def send_mail_c_loan(user):
    email='shimmy.shimmy.bank@gmail.com'
    a='ofbi nazq fwmd ujmr'
    cid=user['cid']
    subject='Confirmation of car loan'
    message=f'''Hello {user['email']}\nWe are happy to confirm your Car loan under the customer id : {user['cid']}
    The amount is : {user['loans']['amt']}
Regards Shimmy Shimmy Bank Team
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
    
def send_mail_h_loan(user):
    email='shimmy.shimmy.bank@gmail.com'
    a='ofbi nazq fwmd ujmr'
    cid=user['cid']
    subject='Confirmation of home loan'
    message=f'''Hello {user['email']}\nWe are happy to confirm your Home loan under the customer id : {user['cid']}
    The amount is : {user['loans']['amt']}
Regards Shimmy Shimmy Bank Team
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
    
def send_mail_t(user,amt):
    email='shimmy.shimmy.bank@gmail.com'
    a='ofbi nazq fwmd ujmr'
    cid=user['cid']
    subject='Confirmation of transaction'
    message=f'''Hello {user['email']}
    A withdrawal of Rs{amt} has taken place.
Regards Shimmy Shimmy Bank Team
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