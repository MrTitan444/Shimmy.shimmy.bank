from flask import Blueprint, render_template, jsonify, request, url_for, redirect, session
from website.functions import *
import mysql.connector as sqltor
import time
c=r=0
l_user={};user={}
auth=Blueprint('auth', __name__)
mycon=sqltor.connect(host='localhost',user='root1',password='12345',database='shimmy_shimmy_bank',autocommit=True)
cursor=mycon.cursor()

@auth.route('/login',methods=['GET'])
def login():
    return render_template('login.html')
       
@auth.route('/login_btn',methods=['POST'])
def login_btn():
    l_user['cid'],l_user['password']=request.form['l_cid'],request.form['l_password']
    s_sql()
    if check_login(l_user):
        s=get_info_login(l_user)
        session['user']=s
        session['login']=True
        return redirect(url_for('views.home'))
    else:
        session['l_fail']=True
        return redirect(url_for('auth.login'))

@auth.route('/update_btn',methods=['POST'])
def update_btn():
    l_user['aadhaar'],l_user['password'],l_user['name']=request.form['l_aadhaar'],request.form['l_password'],request.form['name']
    print(session['user']['cid'])
    print(l_user)
    if l_user['aadhaar']:
        cursor.execute('update users set aadhar="%s" where cid="%s"'%(l_user['aadhaar'],session['user']['cid']))
    if l_user['password']:
        cursor.execute('update users set password="%s" where cid="%s"'%(l_user['password'],session['user']['cid']))
    if l_user['name']:
        cursor.execute('update users set name="%s" where cid="%s"'%(l_user['name'],session['user']['cid']))
    session['update']=True
    return redirect(url_for('auth.update'))

@auth.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@auth.route('/signup_btn',methods=['POST'])
def signup_btn():
    user['cid']=str(randint(100000,999999))
    user['name'],user['email']=request.form['name'],str(request.form['email'])
    user['password'],user['aadhaar'],user['age']=request.form['password'],request.form['aadhaar'],request.form['age']
    # user - cid, name, email, password, aadhaar, age
    return redirect(url_for('auth.verify'))


@auth.route('/verify', methods=['GET'])
def verify():
        global r
        global c
        if not c:
            r=send_mail_ver(user['email'])
            c+=1
        return render_template('verify.html')

@auth.route('/verify_btn',methods=['POST'])
def verify_btn():
    o=int(request.form['otp'])
    if o==r:
        s_sql()
        add_user_sql(user)
        send_mail_acc(user)
        user['sb']=-1
        session['user']=user
        session['login']=True
        return redirect(url_for('views.home'))
    else:
        session['v_fail']=True
        return redirect(url_for('auth.verify'))

@auth.route('/logout')
def logout():
    c_sql()
    session.pop('user', None)
    return redirect(url_for('views.home'))   

@auth.route('/update')
def update():
    return render_template('update.html')