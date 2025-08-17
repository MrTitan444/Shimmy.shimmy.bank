from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session
from website.functions import *
from random import randint
from datetime import date
views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('index.html')

@views.route('/ourservices')
def ourservices():
    print(session)
    return render_template('ourservices.html') 

@views.route('/confirm_acc',methods=['POST'])
def confirm_acc():
    acc=request.form.getlist('account')
    print(acc)
    if "savings" in acc:
        session['user']['sb']=randint(10000,99999)
        print(session)
        add_sb(session['user'])
    elif "current" in acc:
        session['user']['cb']=randint(10000,99999)
        print(session)
        add_cb(session['user'])
    else:
        session['user']['cb']=randint(10000,99999)
        session['user']['sb']=randint(10000,99999)
        add_sb(session['user'])
        add_cb(session['user'])
        print(session)
    return render_template('ourservices.html')

@views.route('/cc',methods=['POST'])
def cc():
    ccn1=''
    cvv1=str(randint(100,999))
    t=date.today()
    v=str(t.year + 10)+'-'+str(t.month)+'-'+str(t.day)
    for i in range(4):
        ccn+=str(randint(1000,9999))
        if i!=3:
             ccn+=' '
    cn=dict(ccn=ccn1,valid=v,cvv=cvv1)
    add_ccn(cn,session['user']['cid'])
    return render_template('ourservices.html')

@views.route('/transhistcur')
def transhistcur():
    l=get_t_cb(session['user'])
    return render_template('transhistcur.html',l=l)

@views.route('/transhistsav')
def transhistsav():
    l=get_t_sb(session['user'])
    return render_template('transhistsav.html',l=l)
