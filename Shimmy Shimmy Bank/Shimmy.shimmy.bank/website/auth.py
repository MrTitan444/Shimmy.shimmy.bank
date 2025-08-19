from flask import Blueprint, render_template, jsonify, request, url_for, redirect, flash, session
from website.functions import *
import mysql.connector as sqltor
c=r=0
l_user={};user={}
mycon=sqltor.connect(host='localhost', user='root1', password='12345', database='shimmy_shimmy_bank')
cursor=mycon.cursor()
auth=Blueprint('auth', __name__)

@auth.route('/login',methods=['GET'])
def login():
    return render_template('login.html')
       
@auth.route('/login_btn',methods=['POST'])
def login_btn():
    l_user['cid'],l_user['password']=request.form['l_cid'],request.form['l_password']
    if check_login(l_user):
        s=get_info_login(l_user)
        session['user']=s
        return redirect(url_for('views.home'))
    else:
        return redirect(url_for('views.home'))

@auth.route('/update_btn',methods=['POST'])
def update_btn():
    l_user['aadhaar'],l_user['password'],l_user['name']=request.form['l_aadhaar'],request.form['l_password'],request.form['name']
    print(session['user']['cid'])
    cursor.execute("update users set name=%s, aadhar=%s, password=%s where cid=%s",(l_user['name'], l_user['aadhaar'], l_user['password'], session['user']['cid']))
    mycon.commit()
    print(l_user)
    return redirect(url_for('views.home'))

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
        add_user_sql(user)
        send_mail_acc(user)
        user['cb'],user['sb']=-1,-1 
        session['user']=user
        print(user)
        flash('You have been logged in','info')
        return redirect(url_for('views.home'))
    else:
        flash('Wrong otp another otp has been sent to your email')
        return redirect(url_for('auth.verify'))

@auth.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out','info')
    return redirect(url_for('views.home'))   

@auth.route('/update')
def update_profile():
    return render_template('update.html')