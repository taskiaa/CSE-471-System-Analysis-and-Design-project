# from flask import Blueprint
# from flask import render_template, request, flash
# from flask import redirect
# from flask import url_for
# from flask_login import login_required, current_user, logout_user, login_user
# from .models import RegularUser, AdminUser, Provider
# from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask import Blueprint
from .models import RegularUser, AdminUser, Provider
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    print("Sign-up")
    if request.method  == 'POST':
        print(request.form)
        email = request.form.get('email')
        password = request.form.get('password')
        last_name = request.form.get('last_name').lower()
        
        regular, admin, provider = RegularUser.query.filter_by(email=email).first(), \
                                   AdminUser.query.filter_by(email=email).first(),\
                                   Provider.query.filter_by(email=email).first()
        
        if any([regular, admin, provider]):
            print("Email already exists")
            if regular:
                flash('Regular user email already exists.', category='error')
            if admin:
                flash('Admin email already exists.', category='error')
            if provider:
                flash('provider email already exists.', category='error')
                
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
            pass
        elif len(password) < 4:
            flash('Password must be greater than 3 characters.', category='error')
            pass
        else: 
            if last_name.lower() == "admin":
                print("Creating ADMIN")
                new_user = AdminUser(
                    nid = request.form.get('nid_number'),
                    first_name = request.form.get('first_name'),
                    last_name = request.form.get('first_name'),
                    mobile = request.form.get('mobile'),
                    email=email, 
                    password=generate_password_hash(password, method='sha256'),
                    user_type = 'admin',
                    location= request.form.get('location'),
                    )
                db.session.add(new_user)
                db.session.commit()
                flash('Logged in successfully!', category='success')
                login_user(new_user, remember=True)
                print(f"\n\n ADMIN ADDED \n\n")
                return redirect(url_for('views.index'))
            if last_name.lower() == "provider":
                print("Creating Provider")
                new_user = Provider(
                    nid = request.form.get('nid_number'),
                    first_name = request.form.get('first_name'),
                    last_name = request.form.get('first_name'),
                    mobile = request.form.get('mobile'),
                    email=email, 
                    password=generate_password_hash(password, method='sha256'),
                    user_type = 'provider',
                    location= request.form.get('location'),
                    )
                db.session.add(new_user)
                db.session.commit()
                flash('Logged in successfully!', category='success')
                login_user(new_user, remember=True)
                print(f"\n\n HOSPITAL ADDED \n\n")
                return redirect(url_for('views.index'))
            else:
                print("Creating REGULAR USER")
                new_user = RegularUser(
                    nid = request.form.get('nid_number'),
                    email=email, 
                    password=generate_password_hash(password, method='sha256'),
                    first_name = request.form.get('first_name'),
                    last_name = request.form.get('last_name'),
                    mobile = request.form.get('mobile'),
                    balance = 0,
                    user_type = 'regular',
                    location= request.form.get('location'),
                    )
                db.session.add(new_user)
                db.session.commit()
                flash('Logged in successfully!', category='success')
                login_user(new_user, remember=True)
                print(f"\n\n REGULAR USER ADDED \n\n")
                return redirect('/index')

    return render_template('signup.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    print("Login")
    if request.method == "POST":
        email = request.form.get('email')
        password =  request.form.get('password')
        print(email, password)
        
        if email.split('@')[1] == 'admin.com':
            print(f"Admin User Detected! Logging In: {email} from Admin")
            user = AdminUser.query.filter_by(email=email).first()
        elif email.split('@')[1] == 'provider.com':
            print(f"Provider User Detected! Logging In: {email} from Provider")
            user = Provider.query.filter_by(email=email).first()
        else: 
            print(f"Regular User Detected! Logging In: {email} from Regular User")
            user = RegularUser.query.filter_by(email=email).first()
        print(f"{user=} Found! Initiating Password Check")
        if user:
            if check_password_hash(user.password, password):
                print("Password Verified!")
                flash('Logged in successfully!', category='success')
                
                login_user(user, remember=True)
                print(f"\n\n {current_user} \n\n")

                return redirect(url_for('views.dashboard'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html")

@auth.route('/logout')
@login_required
def logout():
    print("Logout")
    logout_user()
    return redirect(url_for('auth.login'))
    
    
    