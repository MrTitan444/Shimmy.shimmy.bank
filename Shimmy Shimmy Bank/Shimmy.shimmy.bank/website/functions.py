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
        s='create table transactions_%s(cid char(6) references user(cid) on delete cascade on update cascade, date date, particulars varchar(100), withdrawal int, deposit int, balance int)' %(user['cid'])
        cursor.execute("insert into users(cid, name, aadhar, email, age, password) values(%s, %s, %s, %s, %s, %s)", (user['cid'], user['name'], user['aadhaar'], user['email'], str(user['age']), user['password']))
        cursor.execute(s)
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
    cursor.execute(f'create table t_sb_{user["cid"]}(cid char(6) refernces users(cid) on delete cascade on update cascade ,sb int refernces users(sb) on delete cascade on update cascde, date date, ToWhom varchar(25) default NULL ,amount int, particular enum("Deposit","Withdrawal"), balance int default 0)')
    cursor.execute(f'insert into t_sb_{user["cid"]}(sb) values(%s)'%(user['sb'],))
    mycon.commit()
    mycon.close()
    flash('Savings account succesfully created!!','info')
    return user
    ##except:
        #####return False
    
def add_cb(user):
    mycon=sqltor.connect(host='localhost', user='root1', password='12345',database='shimmy_shimmy_bank')
    cursor=mycon.cursor()
    try:
        cursor.execute('update users set cb=%s where cid="%s"'%(user['cb'],user['cid']))
        cursor.execute(f'create table t_cb_{user['cid']}(cid char(6) refernces users(cid) on delete cascade on update cascade,cb int refernces users(cb) on update cascade on delete cascade, date date, ToWhom varchar(25) default NULL, amount int, particular enum("Deposit","Withdrawal"), balance int default 0)')
        cursor.execute(f'insert into t_sb_{user["cid"]}(cb) values(%s)'%(user['cb'],))
        mycon.commit()
        mycon.close()
        flash('Current account succesfully created!!','info')
        return user
    except:
        return False


def get_info_login(user):
    mycon=sqltor.connect(host='localhost', user='root1', password='12345',database='shimmy_shimmy_bank')
    cursor=mycon.cursor()
    try:
        cursor.execute('select cid, email, sb, cb from users where cid ={}'.format(user['cid']))
        data=list(cursor.fetchone())
        a=['cid','email','sb','cb']
        user=dict(zip(a,data))
        mycon.close()
        return user 
    except:
        return False
    
def get_t_cb(user):
    print("goodmorning")
    mycon=sqltor.connect(host='localhost', user='root1', password='12345',database='shimmy_shimmy_bank')
    cursor=mycon.cursor()
    #try:
    cursor.execute(f'select * from t_cb_{user["cid"]} where cid ="%s"'%(user['cid'],))
    data=cursor.fetchall()
    print("goodmorning")
    mycon.close()
    return data
    #except:
        #return False    
    
def get_t_sb(user):
    mycon=sqltor.connect(host='localhost', user='root1', password='12345',database='shimmy_shimmy_bank')
    cursor=mycon.cursor()
    try:
        cursor.execute('select * from t_sb"{}" where cid ={}'.format(user['cid']))
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


def check_cb(user):
    mycon=sqltor.connect(host='localhost', user='root1', password='12345',database='shimmy_shimmy_bank')
    cursor=mycon.cursor()
    try:
        cursor.execute('select cb from users where cid="{}"'.format(user['cid']))
        d=int(cursor.fetchone())
        if d!=-1:
            session['user']['cb']=d    
        mycon.close()
        return user
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
    

def send_mail_cb(user):
    email='shimmy.shimmy.bank@gmail.com'
    a='ofbi nazq fwmd ujmr'
    cid=user['cid']
    subject='Creation of current bank account'
    message=f'''Hello {user['email']}\nWe are happy to confirm your creation of your current bank account under the customer id:{user['cid']}
    The account number is : {user['cb']}
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
    
