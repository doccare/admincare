import os
import secrets
from PIL import Image
import pandas as pd
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import (RegistrationForm, LoginForm, DoctorAccountForm,
                             PostForm, RequestResetForm, ResetPasswordForm, AppointmentForm,LabtestForm,PatientcareForm,LABAccountForm,CareAccountForm)
from flaskblog.models import User, Post, Doctor, Appointment,Labtest_Post,Labtest_Appointment,Patientcare_Post,Patientcare_Appointment,Labtest,PatientCare,OTP
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import datetime
import uuid
import smtplib
import pandas as pd
import math, random
from werkzeug.datastructures import MultiDict

@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

@app.route("/categorgy/<cname1>", methods=['GET','POST'])
@login_required
def categorgy(cname1):
    print(cname1)
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(categorgy=cname1).paginate(page=page, per_page=5)
    print(posts)
    #user = User.query.filter_by(unique_id=username1).first_or_404()
    '''page = request.args.get('page', 1, type=int)
    if "client" in str(user.type1):
    	posts = Appointment.query.filter_by(client_UID=username1).order_by(Appointment.date_posted.desc()).paginate(page=page, per_page=5)
    else:
    	posts = Appointment.query.filter_by(doc_UID=username1).order_by(Appointment.date_posted.desc()).paginate(page=page, per_page=5)'''
    return render_template('client.html', posts=posts)

@app.route("/delpost/<username>/delete", methods=['GET','POST'])
@login_required
def delete_post1(username):
    print(username)
    #print(time22)
    Appointment.query.filter_by(appunique_id=username).delete()
    #if post.author != current_user:
     #   abort(403)
    #db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/appt_history/<username1>", methods=['GET','POST'])
@login_required
def appt_history(username1):
    print(username1)
    print(type(username1))
    user = User.query.filter_by(unique_id=username1).first_or_404()
    page = request.args.get('page', 1, type=int)
    if "client" in str(user.type1):
    	posts = Appointment.query.filter_by(client_UID=username1).order_by(Appointment.date_posted.desc()).paginate(page=page, per_page=5)
    else:
    	posts = Appointment.query.filter_by(doc_UID=username1).order_by(Appointment.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('appt_history.html', posts=posts)


'''@app.route("/appt_history")
def appt_history():
    print(current_user)
    page = request.args.get('page', 1, type=int)
    posts = Appointment.query.filter_by(doc_UID='79502ce3-11a5-4dab-badf-7671fc129d87').order_by(Appointment.date_posted.desc()).paginate(page=page, per_page=5)
    print(posts)
    #posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('appt_history.html', posts=posts)#Appointment'''



@app.route("/about")
def about():
    return render_template('about.html', title='About')






#########################################################################################OTP LOGIN#########################################################################################################
#########################################################################################OTP LOGIN#########################################################################################################
#########################################################################################OTP LOGIN#########################################################################################################

	 	

@app.route("/otplogin", methods=['GET', 'POST'])
def otplogin():
    email="None"
    if request.method == "POST":
        email=request.form.get('email')
        digits = "0123456789"
        OTP123 = ""
        for i in range(4) :
        	OTP123 += digits[math.floor(random.random() * 10)]
        gmail_user = 'tt5216365@gmail.com'
        gmail_app_password = 'class="mb-3">Posts'
        sent_from = gmail_user
        sent_to = email
        sent_subject = "MY DOC"
        sent_body = ("Hi Friend\n\n" "Your OTP: "+OTP123)
        email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from,sent_to, sent_subject, sent_body)
        try:
        	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        	server.ehlo()
        	server.login(gmail_user, gmail_app_password)
        	server.sendmail(sent_from, sent_to, email_text)
        	server.close()
       		flash('Email sent!', 'success')
       		print('Email sent!')
        except Exception as exception:
        	print("Error: %s!\n\n" % exception)
        user = User.query.filter_by(email=email).first()
        otp = OTP(email=email,otp=OTP123)
        db.session.add(otp)
        db.session.commit()
        print(user)
        if "None" in str(user):
        	print(user)
        	return render_template('otpregister.html',email=email)
        else:
        	print("userrr1")
        	return render_template('otpverify.html',email=email)#, title='Login', form=form)
    
    return render_template('otplogin.html',email=email)#, title='Login', form=form)

@app.route("/otpregister", methods=['GET', 'POST'])
def otpregister():
    email="None"
    if request.method == "POST":
        #otp=request.form.get('otp')
        username=request.form.get('username')
        email=request.form.get('email')
        otp=request.form.get('otp')
        password=request.form.get('password')
        otp1 = OTP.query.filter_by(email=email).first()
        #otp1 = OTP.query.all()
        print(email)
        print(otp1)
        if otp1.otp==otp:
        	#otp=request.form.get('otp')
        	print(otp)
        	OTP.query.filter_by(email=email).delete()
        	db.session.commit()
        	u123=uuid.uuid4()
        	u123=str(u123)
        	#email=request.form.get('otp')  	
        	hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        	user = User(username=username, email=email,type1='client', password=hashed_password,unique_id=u123)
        	db.session.add(user)
        	db.session.commit()
        	print(user)
        	login_user(user)
        	next_page = request.args.get('next')
        	return redirect(next_page) if next_page else redirect(url_for('cient'))
        	flash('Your account has been created! You are now able to log in', 'success')
        else:
        	flash('Wrong OTP', 'danger')
    return render_template('otpregister.html',email=email)#, title='Register', form=form)

@app.route("/otpverify", methods=['GET', 'POST'])
def otpverify():
    email="None"
    if request.method == "POST":
        email=request.form.get('email')
        otp=request.form.get('otp')
        otp1 = OTP.query.filter_by(email=email).first()
        print(otp1.otp)
        if otp1.otp==otp:
        	user = User.query.filter_by(email=email).first()
        	OTP.query.filter_by(email=email).delete()
        	db.session.commit()
        	print(email)
        	print(user)
        	login_user(user)
        	next_page = request.args.get('next')
        	return redirect(next_page) if next_page else redirect(url_for('cient'))
        else:
        	#otp1 = OTP.query.all()
        	flash('Wrong OTP', 'danger')
    
    return render_template('otpverify.html',email=email)#, title='Login', form=form)






############################################################################################REGISTER#########################################################################################################
############################################################################################REGISTER#########################################################################################################
############################################################################################REGISTER#########################################################################################################


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    u123=uuid.uuid4()
    u123=str(u123)
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,type1=form.type1.data, password=hashed_password,unique_id=u123)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)





@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #print(user.unique_id)
        #type1 = User.query.filter_by(email.type1)
        print(user)
	#user = User.query.filter_by(user.type1)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if "client" in str(user):#ereturn redirect(next_page) if next_page else redirect(url_for('home'))
               print("1")
		#print("1")
            elif "Doctor" in str(user):#return redirectnt(next_page) if next_page else redirect(url_for('home'))
               print("2")
               return redirect(url_for('new_post'))
            elif "labtest" in str(user):
               return redirect(url_for('labtestpost_new_post'))
            elif "Patient_care" in str(user):
               return redirect(url_for('patientcare_post_new_post'))
	  	#print("2")
            #return redirect(next_page) if next_page else redirect(url_for('home'))
            return redirect(next_page) if next_page else redirect(url_for('cient'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)






@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))







###########################################################################HOME PAGE#########################################################################################################################
###########################################################################HOME PAGE#########################################################################################################################
###########################################################################HOME PAGE#########################################################################################################################

@app.route("/cient")
def cient():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('client.html', posts=posts)



@app.route("/lab")
def lab():
    page = request.args.get('page', 1, type=int)
    posts = Labtest_Post.query.order_by(Labtest_Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('lab.html', posts=posts)

@app.route("/care")
def care():
    page = request.args.get('page', 1, type=int)
    posts = Patientcare_Post.query.order_by(Patientcare_Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('care.html', posts=posts)







#############################################################################################ACCOUNT#########################################################################################################
#############################################################################################ACCOUNT#########################################################################################################
#############################################################################################ACCOUNT#########################################################################################################





@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = DoctorAccountForm()
    if form.validate_on_submit():
        doc = Doctor(username=form.username.data,email=form.email.data, categorgy=form.categorgy.data, year=form.year.data, address=form.address.data,unique_id=current_user.unique_id)#, author=current_user)
        db.session.add(doc)
        db.session.commit()
        flash('Account updated!', 'success')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
	#form.date.data = current_user.date
	#form.categorgy.data = current_user.categorgy
	#form.year.data = current_user.year
	#form.address.data = current_user.address
		
        #return redirect(url_for('home'))
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)	
    return render_template('account.html', title='Account',image_file=image_file,
                           form=form)#, legend='New Post')




@app.route("/docaccount", methods=['GET', 'POST'])
@login_required
def docaccount():

    if request.method == 'GET':
    	print(request.method)
    	print(request.method)
    	post= Doctor.query.filter_by(unique_id=current_user.unique_id).first()
    	#post= Labtest.query.all()
    	print(current_user.unique_id)
    	print(current_user.unique_id)
    	print(post)
    	if post is None:
    		form = DoctorAccountForm()
    		form.username.data = current_user.username
    		form.email.data = current_user.email
    		#image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    		#return render_template('lab_account.html', title='Account',image_file=image_file,
                 #          form=form,post=post)
    	else:
    		form = DoctorAccountForm(formdata=MultiDict({'username': post.username,'email': post.email,'categorgy': post.categorgy,'year': post.year,'fees': post.fees,'contact': post.contact,'state': post.state,'locality': post.locality,'address': post.address}))
    else:
    	form = DoctorAccountForm()
    	print(request.method)
    	post= Doctor.query.filter_by(unique_id=current_user.unique_id).first()

    	if form.validate_on_submit():
        	if form.picture.data:
        		picture_file = save_picture(form.picture.data)
        		current_user.image_file = picture_file
        	if post is None:
        		post = Doctor(unique_id=current_user.unique_id,username=form.username.data,email=form.email.data, categorgy=form.categorgy.data, year=form.year.data, fees=form.fees.data,contact=form.contact.data, state=form.state.data, locality=form.locality.data, address=form.address.data,image_file=current_user.image_file)
        		#if post is None:
        		#if post is None:
        		#if post is None:
        		db.session.add(post)
        		#db.session.add(post)
        		db.session.commit()
        	else:
        		doc = Doctor.query.filter_by(unique_id=current_user.unique_id).update(dict(username=form.username.data,email=form.email.data, categorgy=form.categorgy.data, year=form.year.data,fees=form.fees.data, contact=form.contact.data, state=form.state.data, locality=form.locality.data, address=form.address.data,image_file=current_user.image_file))#,unique_id=current_user.unique_id)#,author=current_user)
        		#db.session.add(doc)
        		db.session.commit()
        	flash('Account updated!', 'success')

		
        #return redirect(url_for('home'))
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)	
    
    return render_template('docaccount.html', title='Account',image_file=image_file,
                           form=form,post=post)#, legend='New Post')


@app.route("/labaccount", methods=['GET', 'POST'])
@login_required
def labaccount():
    if request.method == 'GET':
    	print(request.method)
    	print(request.method)
    	post= Labtest.query.filter_by(unique_id=current_user.unique_id).first()
    	#post= Labtest.query.all()
    	print(current_user.unique_id)
    	print(current_user.unique_id)
    	print(post)
    	if post is None:
    		form = LABAccountForm()
    		form.username.data = current_user.username
    		form.email.data = current_user.email
    		#image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    		#return render_template('lab_account.html', title='Account',image_file=image_file,
                 #          form=form,post=post)
    	else:
    		form = LABAccountForm(formdata=MultiDict({'username': post.username,'email': post.email,'categorgy': post.categorgy,'year': post.year,'fees': post.fees,'contact': post.contact,'state': post.state,'locality': post.locality,'address': post.address}))
    else:
    	form = LABAccountForm()
    	print(request.method)
    	post= Labtest.query.filter_by(unique_id=current_user.unique_id).first()

    	if form.validate_on_submit():
        	if form.picture.data:
        		picture_file = save_picture(form.picture.data)
        		current_user.image_file = picture_file
        	if post is None:
        		post = Labtest(unique_id=current_user.unique_id,username=form.username.data,email=form.email.data, categorgy=form.categorgy.data, year=form.year.data,fees=form.fees.data,contact=form.contact.data, state=form.state.data, locality=form.locality.data, address=form.address.data,image_file=current_user.image_file)
        		#if post is None:
        		#if post is None:
        		#if post is None:
        		db.session.add(post)
        		#db.session.add(post)
        		db.session.commit()
        	else:
        	#else:
        		doc = Labtest.query.filter_by(unique_id=current_user.unique_id).update(dict(username=form.username.data,email=form.email.data, categorgy=form.categorgy.data,year=form.year.data,fees=form.fees.data,contact=form.contact.data, state=form.state.data, locality=form.locality.data, address=form.address.data,image_file=current_user.image_file))
        		#db.session.add(doc)
        		db.session.commit()
        		flash('Account updated!', 'success')

		
        #return redirect(url_for('home'))
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)	
    
    return render_template('lab_account.html', title='Account',image_file=image_file,
                           form=form,post=post)#, legend='New Post')

@app.route("/Careaccount", methods=['GET', 'POST'])
@login_required
def Careaccount():
    if request.method == 'GET':
    	print(request.method)
    	print(request.method)
    	post= PatientCare.query.filter_by(unique_id=current_user.unique_id).first()
    	#post= Labtest.query.all()
    	print(current_user.unique_id)
    	print(current_user.unique_id)
    	print(post)
    	if post is None:
    		form = LABAccountForm()
    		form.username.data = current_user.username
    		form.email.data = current_user.email
    		#image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    		#return render_template('lab_account.html', title='Account',image_file=image_file,
                 #          form=form,post=post)
    	else:
    		form = CareAccountForm(formdata=MultiDict({'username': post.username,'email': post.email,'categorgy': post.categorgy,'year': post.year,'fees': post.fees,'contact': post.contact,'state': post.state,'locality': post.locality,'address': post.address}))
    else:
    	form = CareAccountForm()
    	print(request.method)
    	post= PatientCare.query.filter_by(unique_id=current_user.unique_id).first()

    	if form.validate_on_submit():
        	if post is None:
        		post = PatientCare(unique_id=current_user.unique_id,username=form.username.data,email=form.email.data, categorgy=form.categorgy.data,year=form.year.data,fees=form.fees.data,contact=form.contact.data, state=form.state.data, locality=form.locality.data, address=form.address.data,image_file=current_user.image_file)
        		#if post is None:
        		#if post is None:
        		#if post is None:
        		db.session.add(post)
        		db.session.add(post)
        		db.session.commit()
        	else:
        		doc = PatientCare.query.filter_by(unique_id=current_user.unique_id).update(dict(username=form.username.data,email=form.email.data, categorgy=form.categorgy.data,year=form.year.data,fees=form.fees.data,contact=form.contact.data, state=form.state.data, locality=form.locality.data, address=form.address.data,image_file=current_user.image_file))
#,unique_id=current_user.unique_id)#,author=current_user)
        		#db.session.add(doc)
        		db.session.commit()
        		flash('Account updated!', 'success')

		
        #return redirect(url_for('home'))
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)	
    
    return render_template('Care_account.html', title='Account',image_file=image_file,
                           form=form,post=post)#, legend='New Post')














########################################################################POST#################################################################################################################################
########################################################################POST#################################################################################################################################
########################################################################POST#################################################################################################################################


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    print(form.multi.data)
    print(type(form.multi.data))
    if request.method == 'GET':
    	#print(request.method)
    	#print(request.method)
    	post= Post.query.filter_by(docunique_id=current_user.unique_id).first()
    	#post= Labtest.query.all()
    	#print(current_user.username)
    	#print(current_user.unique_id)
    	#print(post)
    	if post is None:
    		print
    		#form.username.data = current_user.username
    		#form.email.data = current_user.email
    		#image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    		#return render_template('lab_account.html', title='Account',image_file=image_file,
                 #          form=form,post=post)
    	else:
    		form = PostForm(formdata=MultiDict({'content': post.content,'start_date': str(post.start_date),'end_date': str(post.end_date),'start_time': str(post.start_time),'end_time': str(post.end_time),'slot_time': str(post.slot_time),'multi': post.weekday}))
    #print("this one")
    aoo1=Doctor.query.filter_by(unique_id=current_user.unique_id).first()
    print(aoo1)
    if aoo1 is None:
    	flash('Please update Account Details', 'success')
    	return redirect(url_for('docaccount'))
    else:
    	print#(current_user)
    #print(current_user)
    #print(current_user)
    #print(current_user)
    if form.validate_on_submit():
        print(form.multi.data)
        print('aaaaaaaaaaaaaaaaaa')
        print(type(form.multi.data))
        post= Post.query.filter_by(title=current_user.unique_id).first()
        if str(current_user.unique_id) in str(post):
        	post.content = form.content.data
        	post.start_date = form.start_date.data
        	post.end_date = form.end_date.data
        	post.start_time = form.start_time.data
        	post.end_time = form.end_time.data
        	post.content = form.content.data
        	post.slot_time = form.slot_time.data
        	post.weekday = str(form.multi.data)
        	aoo1=Doctor.query.filter_by(unique_id=current_user.unique_id).first()#.all()
        	post.categorgy = aoo1.categorgy
        	post.year = aoo1.year
        	post.address = aoo1.address
        	db.session.commit()
        	post = Post.query.filter_by(title=current_user.unique_id).first_or_404()#.all()
        	post = Post.query.all()
        	#print(post)
        	post1=Post.query.all()
        	print(post1)
        	flash('Your post has been updated!', 'success')
        else:
        	start1=form.start_date.data		
        	end1=form.end_date.data
        	aoo1=Doctor.query.filter_by(unique_id=current_user.unique_id).first()#.all()
        	#post.categorgy = aoo1.categorgy
        	#post.year = oo1.year
        	print(form.multi.data)
        	print(type(form.multi.data))
        	post = Post(title=current_user.unique_id, content=form.content.data,start_date=start1,end_date=end1,start_time=form.start_time.data,end_time=form.end_time.data,categorgy=aoo1.categorgy,year=aoo1.year,fees= aoo1.fees,contact= aoo1.contact,state= aoo1.state,locality= aoo1.locality,address= aoo1.address,slot_time = form.slot_time.data,docunique_id = current_user.unique_id,weekday = str(form.multi.data),author=current_user)
        	#print(current_user)
        	post1=Post.query.all()
        	db.session.add(post)
        	db.session.commit()
        	print(post1)
        	flash('Your post has been created!', 'success')
        	return redirect(url_for('home'))

    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')





@app.route("/labtestpost/new", methods=['GET', 'POST'])
@login_required
def labtestpost_new_post():
    form = LabtestForm()
    if request.method == 'GET':
    	print(request.method)
    	print(request.method)
    	post= Labtest_Post.query.filter_by(labunique_id=current_user.unique_id).first()
    	#post= Labtest.query.all()
    	print(current_user.username)
    	print(current_user.unique_id)
    	print(post)
    	if post is None:
    		print
    		#form.username.data = current_user.username
    		#form.email.data = current_user.email
    		#image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    		#return render_template('lab_account.html', title='Account',image_file=image_file,
                 #          form=form,post=post)
    	else:
    		form = LabtestForm(formdata=MultiDict({'content': post.content,'start_date': str(post.start_date),'end_date': str(post.end_date),'start_time': str(post.start_time),'end_time': str(post.end_time),'slot_time': str(post.slot_time)}))
    #print("this one")
    aoo1=Labtest.query.filter_by(unique_id=current_user.unique_id).first()
    print(aoo1)
    if aoo1 is None:
    	flash('Please update Account Details', 'success')
    	return redirect(url_for('labaccount'))
    else:
    	print(current_user)
    #print(current_user)
    #print(current_user)
    #print(current_user)
    #print("this one")
    print(current_user)
    if form.validate_on_submit():
        #print(post.title)
        #print(post.content)
        #print(post.start_date)
        post= Labtest_Post.query.filter_by(title=current_user.unique_id).first()
        if str(current_user.unique_id) in str(post):
        	post.content = form.content.data
        	post.start_date = form.start_date.data
        	post.end_date = form.end_date.data
        	post.start_time = form.start_time.data
        	post.content = form.content.data
        	post.slot_time = form.slot_time.data
        	aoo1=Labtest.query.filter_by(unique_id=current_user.unique_id).first()#.all()
        	post.categorgy = aoo1.categorgy
        	post.year = aoo1.year
        	post.address = aoo1.address
        	db.session.commit()
        	post = Labtest_Post.query.filter_by(title=current_user.unique_id).first_or_404()#.all()
        	post = Labtest_Post.query.all()
        	print(post)
        	flash('Your post has been updated!', 'success')
        else:
        	start1=form.start_date.data		
        	end1=form.end_date.data
        	aoo1=Labtest.query.filter_by(unique_id=current_user.unique_id).first()#.all()
        	#post.categorgy = aoo1.categorgy
        	#post.year = oo1.year
        	print(current_user)
        	post = Labtest_Post(title=current_user.unique_id, content=form.content.data,start_date=start1,end_date=end1,start_time=form.start_time.data,end_time=form.end_time.data,categorgy=aoo1.categorgy,year=aoo1.year,fees= aoo1.fees,contact= aoo1.contact,state= aoo1.state,locality= aoo1.locality,address= aoo1.address,slot_time = form.slot_time.data,labunique_id = current_user.unique_id,author1=current_user)
        	post1=Labtest_Post.query.all()
        	db.session.add(post)
        	db.session.commit()
        	flash('Your post has been created!', 'success')
        	return redirect(url_for('home'))

    return render_template('lab_create_post.html', title='New Post',
                           form=form, legend='New Post')

@app.route("/patientcare_post_new_post/new", methods=['GET', 'POST'])
@login_required
def patientcare_post_new_post():
    #form = PatientcareForm()
    form = PatientcareForm()
    if request.method == 'GET':
    	print(request.method)
    	print(request.method)
    	post= Patientcare_Post.query.filter_by(careunique_id=current_user.unique_id).first()
    	#post= Labtest.query.all()
    	print(current_user.username)
    	print(current_user.unique_id)
    	print(post)
    	if post is None:
    		print
    		#form.username.data = current_user.username
    		#form.email.data = current_user.email
    		#image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    		#return render_template('lab_account.html', title='Account',image_file=image_file,
                 #          form=form,post=post)
    	else:
    		form = PatientcareForm(formdata=MultiDict({'content': post.content,'start_date': str(post.start_date),'end_date': str(post.end_date),'start_time': str(post.start_time),'end_time': str(post.end_time),'slot_time': str(post.slot_time)}))
    #print("this one")
    aoo1=PatientCare.query.filter_by(unique_id=current_user.unique_id).first()
    print(aoo1)
    if aoo1 is None:
    	flash('Please update Account Details', 'success')
    	return redirect(url_for('Careaccount'))
    else:
    	print(current_user)
    #print(current_user)
    #print(current_user)
    #print(current_user)
    #print("this one")
    print(current_user)

    if form.validate_on_submit():
        #print(post.title)
        #print(post.content)
        #print(post.start_date)
        post= Patientcare_Post.query.filter_by(title=current_user.unique_id).first()
        if str(current_user.unique_id) in str(post):
        	post.content = form.content.data
        	post.start_date = form.start_date.data
        	post.end_date = form.end_date.data
        	post.start_time = form.start_time.data
        	post.content = form.content.data
        	post.slot_time = form.slot_time.data
        	aoo1=PatientCare.query.filter_by(unique_id=current_user.unique_id).first()#.all()
        	post.categorgy = aoo1.categorgy
        	post.year = aoo1.year
        	post.address = aoo1.address
        	db.session.commit()
        	post = Patientcare_Post.query.filter_by(title=current_user.unique_id).first_or_404()#.all()
        	post = Patientcare_Post.query.all()
        	print(post)
        	flash('Your post has been updated!', 'success')
        else:
        	start1=form.start_date.data		
        	end1=form.end_date.data
        	aoo1=PatientCare.query.filter_by(unique_id=current_user.unique_id).first()#.all()
        	#post.categorgy = aoo1.categorgy
        	#post.year = oo1.year
        	#post.address = oo1.address
        	print(current_user)
        	post = Patientcare_Post(title=current_user.unique_id, content=form.content.data,start_date=start1,end_date=end1,start_time=form.start_time.data,end_time=form.end_time.data,categorgy=aoo1.categorgy,year=aoo1.year,fees= aoo1.fees,contact= aoo1.contact,state= aoo1.state,locality= aoo1.locality,address= aoo1.address,slot_time = form.slot_time.data,careunique_id = current_user.unique_id,author2=current_user)
        	post1=Patientcare_Post.query.all()
        	db.session.add(post)
        	db.session.commit()
        	flash('Your post has been created!', 'success')
        	return redirect(url_for('home'))

    return render_template('Care_create_post.html', title='New Post',
                           form=form, legend='New Post')
















##########################################################################APPOINTMENT#######################################################################################################################
##########################################################################APPOINTMENT#######################################################################################################################
##########################################################################APPOINTMENT#######################################################################################################################

@app.route("/appointment/<string:username>", methods=['GET', 'POST'])
@login_required
def appointment(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    print(user.unique_id)# = User.query.filter_by(unique_id=username).first_or_404()
    post1=Post.query.filter_by(title=user.unique_id).first_or_404()
    #a7=str(post1).replace("', '"," ").replace("Post('","").replace("')","")
    #print(a7)# = Post.query.filter_by(username=username).first_or_404()
    #a0,a1,a2,a3,a4,a5,a6,a8,a9=str(a7).split(' ')
    #print(a)
    b1,b2,b3=str(post1.start_date).split('-')
    c1,c2,c3=str(post1.end_date).split('-')
    d1,d2,d3=str(post1.start_time).split(':')
    e1,e2,e3=str(post1.end_time).split(':')
    #print(type(a8))
    start_time= str(d1)+':'+str(d2)
    #slot_time=1
    hours=[]
    end_time=str(e1)+':'+str(e2)#a9#datetime.time(int(e1),int(e2),int(e3))
    time = datetime.datetime.strptime(start_time, '%H:%M')
    end = datetime.datetime.strptime(end_time, '%H:%M')

    start_date= datetime.date(int(b1),int(b2),int(b3))
    end_date=datetime.date(int(c1),int(c2),int(c3))
    adates_2011_2013 = [ start_date + datetime.timedelta(n) for n in range(int ((end_date - start_date).days))]    
    print(list(post1.weekday))
    print(type(list(post1.weekday)))
    wday=list(post1.weekday)
    print(wday)
    print(adates_2011_2013)
    for datelist in adates_2011_2013:
    	print("#####################")
    	#print(datelist)
    	#print(adates_2011_2013.index(datelist))
    	temp = pd.Timestamp(datelist)
    	#print(temp.dayofweek)
    	wday3=temp.dayofweek
    	for wdayx in wday:
    		if str(wdayx) == str(wday3):
    			print(temp.dayofweek)
    			print(datelist)
    			abcdate=adates_2011_2013.index(datelist)
    			print(type(abcdate))
    			print("#####################")
    			adates_2011_2013 = adates_2011_2013[:abcdate] + adates_2011_2013[abcdate+1 :]
    	#print(datelist242)
    	#temp = pd.Timestamp(datelist)
    	#print(temp.dayofweek)
    #print(datelist242)
    print(adates_2011_2013)
    print(adates_2011_2013)
    #adates_2011_2013={"colors": ["red", "white", "blue"],"colors12": ["red1", "white1", "blue1"]}
    print(type(adates_2011_2013))
    appo = Appointment.query.filter_by(doc_UID=user.unique_id).all()
    #print(appo[1])   
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    print(type(posts))
    return render_template('appointmentbook.html', posts=posts, user=user,adates_2011_2013=adates_2011_2013,hours=hours)


@app.route("/appointmentbook", methods=['GET', 'POST'])
def appointmentbook():

    print(current_user)
    
    #post1=Post.query.filter_by(title=unique_code).first_or_404()
    if request.method == "POST":
    	unique_code = request.form.get("title")
    	docname = request.form.get("docname")
    	date50 = request.form.get("date50")
    	hours = request.form.get("hours")
    	date11 = request.form.get("date11")
    	user = request.form.get("user")
    	time50 = request.form.get("time50")
    	#slot_time = request.form.get("slot_time")
    	user = User.query.filter_by(username=docname).first_or_404()
    	#print(user.unique_id)# = User.query.filter_by(unique_id=username).first_or_404()
    	post1=Post.query.filter_by(title=unique_code).first_or_404()
    	#a7=str(post1).replace("', '"," ").replace("Post('","").replace("')","")
    	#print(a7)# = Post.query.filter_by(username=username).first_or_404()
    	#a0,a1,a2,a3,a4,a5,a6,a8,a9=str(a7).split(' ')
    	#print(a)
    	b1,b2,b3=str(post1.start_date).split('-')
    	c1,c2,c3=str(post1.end_date).split('-')
    	d1,d2,d3=str(post1.start_time).split(':')
    	e1,e2,e3=str(post1.end_time).split(':')
    	#print(type(a8))
    	start_time= str(d1)+':'+str(d2)
    	slot_time=post1.slot_time
    	slot_time=int(slot_time)
    	hours=[]
    	end_time=str(e1)+':'+str(e2)#a9#datetime.time(int(e1),int(e2),int(e3))
    	time = datetime.datetime.strptime(start_time, '%H:%M')
    	end = datetime.datetime.strptime(end_time, '%H:%M')
    	while time <= end:
    		hours.append(time.strftime("%H:%M"))
    		time += datetime.timedelta(minutes=slot_time)
    	print(hours)
    	print(current_user.username)
    	print(current_user.unique_id)
    	print(unique_code)
    	print(hours)
    	print(date50)
    	print(date11)
    	#return render_template('about.html')
    	appo = Appointment.query.filter_by(doc_UID=unique_code).all()
    	appo=str(appo).split(":00')")
    	for appo11 in appo:
    		#print(appo11)
    		appo22=str(appo11).split("', '")
    		#print(appo22)
    		for hr22 in hours:
    			#print(hr22)
    			if hr22 in str(appo22) and date11 in str(appo22):
    				print("to check time removal")
    				print(hr22)
    				hours.remove(hr22)
    				print(hours)
    			else:
    				print#("no")
    	#return render_template('about.html')
    		
    	if not time50:
    		print#('none')
    	else:
	    	t1,t2=str(time50).split(':')
	    	time50= str(t1)+':'+str(t2)
	    	#print(time50)
	    	d1,d2,d3=str(date11).split('-')
	    	date50= datetime.date(int(d1),int(d2),int(d3))
	    	#time50 = datetime.datetime.strptime(time50, '%H:%M')
	    	time50 = datetime.time(int(t1),int(t2))
	    	u123=uuid.uuid4()
	    	u123=str(u123)
	    	date50= datetime.date(int(d1),int(d2),int(d3))
	    	appoint = Appointment(clientname=current_user.username,client_UID=current_user.unique_id,docname=docname, doc_UID=unique_code, app_date=date50, app_time=time50,appunique_id=u123)
	    	#print(appoint)
	    	db.session.add(appoint)
	    	db.session.commit()
	    	flash('Booked', 'success')
	    	return redirect(url_for('cient'))
    	page = request.args.get('page', 1, type=int)
    	posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    	return render_template('appointmentbook.html',posts=posts,hours=hours,user=date50)






@app.route("/appointmentlab/<string:username>", methods=['GET', 'POST'])
@login_required
def appointmentlab(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    print(user.unique_id)# = User.query.filter_by(unique_id=username).first_or_404()
    post1=Labtest_Post.query.filter_by(title=user.unique_id).first_or_404()
    #a7=str(post1).replace("', '"," ").replace("Post('","").replace("')","")
    #print(a7)# = Post.query.filter_by(username=username).first_or_404()
    #a0,a1,a2,a3,a4,a5,a6,a8,a9=str(a7).split(' ')
    #print(a)
    b1,b2,b3=str(post1.start_date).split('-')
    c1,c2,c3=str(post1.end_date).split('-')
    d1,d2,d3=str(post1.start_time).split(':')
    e1,e2,e3=str(post1.end_time).split(':')
    #print(type(a8))
    start_time= str(d1)+':'+str(d2)
    #slot_time=1
    hours=[]
    end_time=str(e1)+':'+str(e2)#a9#datetime.time(int(e1),int(e2),int(e3))
    time = datetime.datetime.strptime(start_time, '%H:%M')
    end = datetime.datetime.strptime(end_time, '%H:%M')
    '''while time <= end:
    	hours.append(time.strftime("%H:%M"))
    	time += datetime.timedelta(minutes=slot_time)
    print(hours)'''
    

    start_date= datetime.date(int(b1),int(b2),int(b3))
    end_date=datetime.date(int(c1),int(c2),int(c3))
    adates_2011_2013 = [ start_date + datetime.timedelta(n) for n in range(int ((end_date - start_date).days))]    
    print(adates_2011_2013)
    print(adates_2011_2013)
    print(adates_2011_2013)
    print(adates_2011_2013)
    print(adates_2011_2013)
    print(adates_2011_2013)
    print(adates_2011_2013)
    #adates_2011_2013={"colors": ["red", "white", "blue"],"colors12": ["red1", "white1", "blue1"]}
    print(type(adates_2011_2013))
    appo = Labtest_Appointment.query.filter_by(doc_UID=user.unique_id).all()
    #print(appo[1])   
    posts = Labtest_Post.query.filter_by(author1=user)\
        .order_by(Labtest_Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    print(type(posts))
    return render_template('appointmentbooklab.html', posts=posts, user=user,adates_2011_2013=adates_2011_2013)#,hours=hours)


@app.route("/appointmentbooklab", methods=['GET', 'POST'])
def appointmentbooklab():

    print(current_user)
    
    #post1=Post.query.filter_by(title=unique_code).first_or_404()
    if request.method == "POST":
    	unique_code = request.form.get("title")
    	docname = request.form.get("docname")
    	date50 = request.form.get("date50")
    	hours = request.form.get("hours")
    	date11 = request.form.get("date11")
    	user = request.form.get("user")
    	time50 = request.form.get("time50")
    	#slot_time = request.form.get("slot_time")
    	user = User.query.filter_by(username=docname).first_or_404()
    	#print(user.unique_id)# = User.query.filter_by(unique_id=username).first_or_404()
    	post1=Labtest_Post.query.filter_by(title=unique_code).first_or_404()
    	#a7=str(post1).replace("', '"," ").replace("Post('","").replace("')","")
    	#print(a7)# = Post.query.filter_by(username=username).first_or_404()
    	#a0,a1,a2,a3,a4,a5,a6,a8,a9=str(a7).split(' ')
    	#print(a)
    	b1,b2,b3=str(post1.start_date).split('-')
    	c1,c2,c3=str(post1.end_date).split('-')
    	d1,d2,d3=str(post1.start_time).split(':')
    	e1,e2,e3=str(post1.end_time).split(':')
    	#print(type(a8))
    	start_time= str(d1)+':'+str(d2)
    	slot_time=post1.slot_time
    	slot_time=int(slot_time)
    	hours=[]
    	end_time=str(e1)+':'+str(e2)#a9#datetime.time(int(e1),int(e2),int(e3))
    	time = datetime.datetime.strptime(start_time, '%H:%M')
    	end = datetime.datetime.strptime(end_time, '%H:%M')
    	while time <= end:
    		hours.append(time.strftime("%H:%M"))
    		time += datetime.timedelta(minutes=slot_time)
    	print(hours)
    	print(current_user.username)
    	print(current_user.unique_id)
    	print(unique_code)
    	print(hours)
    	print(date50)
    	print(date11)
    	#return render_template('about.html')
    	appo = Labtest_Appointment.query.filter_by(doc_UID=unique_code).all()
    	appo=str(appo).split(":00')")
    	for appo11 in appo:
    		#print(appo11)
    		appo22=str(appo11).split("', '")
    		#print(appo22)
    		for hr22 in hours:
    			#print(hr22)
    			if hr22 in str(appo22) and date11 in str(appo22):
    				#print(hr22)
    				hours.remove(hr22)
    				#print(hours)
    			else:
    				print#("no")
    	#return render_template('about.html')
    		
    	if not time50:
    		print#('none')
    	else:
	    	t1,t2=str(time50).split(':')
	    	time50= str(t1)+':'+str(t2)
	    	#print(time50)
	    	d1,d2,d3=str(date11).split('-')
	    	date50= datetime.date(int(d1),int(d2),int(d3))
	    	#time50 = datetime.datetime.strptime(time50, '%H:%M')
	    	time50 = datetime.time(int(t1),int(t2))
	    	#print(type(time50))
	    	date50= datetime.date(int(d1),int(d2),int(d3))
	    	appoint = Labtest_Appointment(clientname=current_user.username,client_UID=current_user.unique_id,docname=docname, doc_UID=unique_code, app_date=date50, app_time=time50)
	    	#print(appoint)
	    	db.session.add(appoint)
	    	db.session.commit()
	    	flash('Booked', 'success')
    	page = request.args.get('page', 1, type=int)
    	posts = Labtest_Post.query.filter_by(author1=user)\
        .order_by(Labtest_Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    	return render_template('appointmenttimelab.html',posts=posts,hours=hours,user=date50)



@app.route("/appointmentcare/<string:username>", methods=['GET', 'POST'])
@login_required
def appointmentcare(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    print(user.unique_id)# = User.query.filter_by(unique_id=username).first_or_404()
    post1=Patientcare_Post.query.filter_by(title=user.unique_id).first_or_404()
    #a7=str(post1).replace("', '"," ").replace("Post('","").replace("')","")
    #print(a7)# = Post.query.filter_by(username=username).first_or_404()
    #a0,a1,a2,a3,a4,a5,a6,a8,a9=str(a7).split(' ')
    #print(a)
    b1,b2,b3=str(post1.start_date).split('-')
    c1,c2,c3=str(post1.end_date).split('-')
    d1,d2,d3=str(post1.start_time).split(':')
    e1,e2,e3=str(post1.end_time).split(':')
    #print(type(a8))
    start_time= str(d1)+':'+str(d2)
    #slot_time=1
    hours=[]
    end_time=str(e1)+':'+str(e2)#a9#datetime.time(int(e1),int(e2),int(e3))
    time = datetime.datetime.strptime(start_time, '%H:%M')
    end = datetime.datetime.strptime(end_time, '%H:%M')
    '''while time <= end:
    	hours.append(time.strftime("%H:%M"))
    	time += datetime.timedelta(minutes=slot_time)
    print(hours)'''
    

    start_date= datetime.date(int(b1),int(b2),int(b3))
    end_date=datetime.date(int(c1),int(c2),int(c3))
    adates_2011_2013 = [ start_date + datetime.timedelta(n) for n in range(int ((end_date - start_date).days))]    
    print(adates_2011_2013)
    print(adates_2011_2013)
    print(adates_2011_2013)
    print(adates_2011_2013)
    print(adates_2011_2013)
    print(adates_2011_2013)
    print(adates_2011_2013)
    #adates_2011_2013={"colors": ["red", "white", "blue"],"colors12": ["red1", "white1", "blue1"]}
    print(type(adates_2011_2013))
    appo = Patientcare_Appointment.query.filter_by(doc_UID=user.unique_id).all()
    #print(appo[1])   
    posts = Patientcare_Post.query.filter_by(author2=user)\
        .order_by(Patientcare_Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    print(type(posts))
    return render_template('appointmentbookcare.html', posts=posts, user=user,adates_2011_2013=adates_2011_2013)#,hours=hours)


@app.route("/appointmentbookcare", methods=['GET', 'POST'])
def appointmentbookcare():

    print(current_user)
    
    #post1=Post.query.filter_by(title=unique_code).first_or_404()
    if request.method == "POST":
    	unique_code = request.form.get("title")
    	docname = request.form.get("docname")
    	date50 = request.form.get("date50")
    	hours = request.form.get("hours")
    	date11 = request.form.get("date11")
    	user = request.form.get("user")
    	time50 = request.form.get("time50")
    	#slot_time = request.form.get("slot_time")
    	user = User.query.filter_by(username=docname).first_or_404()
    	#print(user.unique_id)# = User.query.filter_by(unique_id=username).first_or_404()
    	post1=Patientcare_Post.query.filter_by(title=unique_code).first_or_404()
    	#a7=str(post1).replace("', '"," ").replace("Post('","").replace("')","")
    	#print(a7)# = Post.query.filter_by(username=username).first_or_404()
    	#a0,a1,a2,a3,a4,a5,a6,a8,a9=str(a7).split(' ')
    	#print(a)
    	b1,b2,b3=str(post1.start_date).split('-')
    	c1,c2,c3=str(post1.end_date).split('-')
    	d1,d2,d3=str(post1.start_time).split(':')
    	e1,e2,e3=str(post1.end_time).split(':')
    	#print(type(a8))
    	start_time= str(d1)+':'+str(d2)
    	slot_time=post1.slot_time
    	slot_time=int(slot_time)
    	hours=[]
    	end_time=str(e1)+':'+str(e2)#a9#datetime.time(int(e1),int(e2),int(e3))
    	time = datetime.datetime.strptime(start_time, '%H:%M')
    	end = datetime.datetime.strptime(end_time, '%H:%M')
    	while time <= end:
    		hours.append(time.strftime("%H:%M"))
    		time += datetime.timedelta(minutes=slot_time)
    	print(hours)
    	print(current_user.username)
    	print(current_user.unique_id)
    	print(unique_code)
    	print(hours)
    	print(date50)
    	print(date11)
    	#return render_template('about.html')
    	appo = Patientcare_Appointment.query.filter_by(doc_UID=unique_code).all()
    	appo=str(appo).split(":00')")
    	for appo11 in appo:
    		#print(appo11)
    		appo22=str(appo11).split("', '")
    		#print(appo22)
    		for hr22 in hours:
    			#print(hr22)
    			if hr22 in str(appo22) and date11 in str(appo22):
    				#print(hr22)
    				hours.remove(hr22)
    				#print(hours)
    			else:
    				print#("no")
    	#return render_template('about.html')
    		
    	if not time50:
    		print#('none')
    	else:
	    	t1,t2=str(time50).split(':')
	    	time50= str(t1)+':'+str(t2)
	    	#print(time50)
	    	d1,d2,d3=str(date11).split('-')
	    	date50= datetime.date(int(d1),int(d2),int(d3))
	    	#time50 = datetime.datetime.strptime(time50, '%H:%M')
	    	time50 = datetime.time(int(t1),int(t2))
	    	#print(type(time50))
	    	date50= datetime.date(int(d1),int(d2),int(d3))
	    	appoint = Patientcare_Appointment(clientname=current_user.username,client_UID=current_user.unique_id,docname=docname, doc_UID=unique_code, app_date=date50, app_time=time50)
	    	#print(appoint)
	    	db.session.add(appoint)
	    	db.session.commit()
	    	flash('Booked', 'success')
    	page = request.args.get('page', 1, type=int)
    	posts = Patientcare_Post.query.filter_by(author2=user)\
        .order_by(Patientcare_Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    	return render_template('appointmenttimecare.html',posts=posts,hours=hours,user=date50)











'''@app.route("/post/<int:post_id>")
#@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)'''






############################################################################################ROUGH#########################################################################################################
############################################################################################ROUGH#########################################################################################################
############################################################################################ROUGH#########################################################################################################



@app.route("/post/<int:post_id>")
#@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    print("ddDadasdadassadas")
    print(picture_path)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn





