from flask import Blueprint, render_template, request, redirect, url_for, session
from website.functions import *
from random import randint
from datetime import date
views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@views.route('/ourservices', methods=['GET'])
def ourservices():
    return render_template('ourservices.html') 


@views.route('/profile')
def profile():
    session["user"]["sb_b"]=get_sb_b(session['user'])
    return render_template('profile.html',user=session['user'])


@views.route('/transhistsav',methods=['GET'])
def transhistsav():
    l=get_t_sb(session['user'])
    #date amount particular balance tid
    return render_template('transhistsav.html',lasvegas=l)

@views.route('/carloan',methods=['GET'])
def carloan():
    return render_template('carloan.html')

@views.route('carloan_btn',methods=['POST'])
def carloan_btn():
    interest={3:5,6:5.5,12:12,24:14,60:17,120:20,240:24}
    amt=int(request.form['loan_amt'])
    form_tp=int(request.form.get('time_period'))
    tp=date.today()+relativedelta(months=form_tp)
    c_loan_details={'amt':amt,'tp':form_tp,'interest':interest[form_tp]}
    session['user']['c_loan']=c_loan_details
    add_c_loan(session['user'])
    send_mail_c_loan(session['user'])
    return redirect(url_for('views.carloan'))


@views.route('/homeloan',methods=['GET'])
def homeloan():
    return render_template('homeloan.html')

@views.route('/homeloan_btn',methods=['POST'])
def homeloan_btn():
    interest={3:5,6:5.5,12:12,24:14,60:17,120:20,240:24}
    amt=int(request.form['loan_amt'])
    form_tp=int(request.form.get('time_period'))
    print(form_tp, type(form_tp))
    tp=date.today()+relativedelta(months=form_tp)
    h_loan_details={'amt':amt,'tp':form_tp,'interest':interest[form_tp]}
    session['user']['h_loan']=h_loan_details
    add_h_loan(session['user'])
    send_mail_h_loan(session['user'])
    return redirect(url_for('views.homeloan'))

@views.route('/transfer',methods=['GET'])
def transfer():
    return render_template('transfer.html')

@views.route('/s_transfer_btn',methods=['POST'])
def s_transfer_btn():
    s_amt=int(request.form['s_transfer_amt'])
    s_no=request.form['s_no']
    print(s_no)
    # reciever amt user
    t=sb_t(s_no,s_amt,session['user'])
    if t:
        send_mail_d(get_reciever_id(s_no),s_amt)
        send_mail_w(session['user'],s_amt)
    return redirect(url_for('views.transfer'))


@views.route('/withdraw',methods=['GET'])
def withdraw():
    return render_template('withdraw.html')

@views.route('/withdraw_btn',methods=['POST'])
def withdraw_btn():
    amt=int(request.form['amt'])
    if withdraw_(session['user'],amt):
        send_mail_w(session['user'],amt)
    return redirect(url_for('views.withdraw'))

@views.route('/deposit',methods=['GET'])
def deposit():
    return render_template('deposit.html')

@views.route('/deposit_btn',methods=['POST'])
def deposit_btn():
    amt=request.form['amt']
    deposit_(session['user'],amt)
    send_mail_d(session['user'],amt)
    return redirect(url_for('views.deposit'))

@views.route('hl_t_btn',methods=['POST'])
def hl_t_btn():
    h_loan_transfer(session['user'])
    session['h_loan_transfer']=True
    print(session['user']['h_loan']['amt'])
    send_mail_d(session['user'],session['user']['h_loan']['amt'])
    return redirect(url_for('views.homeloan'))

@views.route('cl_t_btn',methods=['POST'])
def cl_t_btn():
    c_loan_transfer(session['user'])
    session['c_loan_transfer']=True
    send_mail_d(session['user'],session['user']['c_loan']['amt'])
    return redirect(url_for('views.carloan'))