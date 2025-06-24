from flask import Blueprint
from flask import render_template, request
from flask import redirect
from flask import url_for
from flask_login import login_required, current_user, logout_user, login_user
from . import db 
import random
from .models import RegularUser, AdminUser, Provider, Coupons

admin = Blueprint('admin', __name__, template_folder='templates/admin')

@admin.route('/manage-users', methods=['GET', 'POST'])
@login_required
def manage_users():
    print('Manage Users')

    if request.method == "POST":
        print(request.form)
        email = request.form.get('user_email')
        new_status = request.form.get('new_status')
        
        user = RegularUser.query.filter_by(email=email).first()
        
        if new_status == 'premium':
            user.premium_user = True
            db.session.commit()
        elif new_status == 'regular':
            user.premium_user = False
            db.session.commit()
        else:
            print("Invalid Status")
        print(f"User Status Updated to {new_status}")
    
    regular_users = RegularUser.query.all()
    print(regular_users)
    return render_template('manage-users.html', regular_users=regular_users)

@admin.route('/edit-users', methods=['GET', 'POST'])
def edit_users():
    if request.method == "POST":
        print(request.form)
        email = request.form.get('user_email')
        user_first_name = request.form.get('user_first_name')
        user_mobile = request.form.get('user_mobile')
        user_location = request.form.get('user_location')
        user_balance = request.form.get('user_balance')

        user = RegularUser.query.filter_by(email=email).first()
        user.first_name = user_first_name
        user.mobile = user_mobile
        user.location = user_location
        user.balance = user_balance
        db.session.commit()

        print(f"User Details Updated")
    regular_users = RegularUser.query.all()
    return render_template('edit-users.html', regular_users=regular_users)


@admin.route('/coupons', methods=['GET', 'POST'])
def coupons():
    coupons = Coupons.query.all()
    
    if request.method == "POST":
        print(request.form)
        coupon_id = request.form.get('coupon_id')
        coupon_code = request.form.get('coupon_code')
        coupon_discount = request.form.get('coupon_discount')
        coupon_usage_limit = request.form.get('coupon_usage')
        coupon_eligible_users = request.form.get('coupon_eligible_users')

        coupon = Coupons.query.filter_by(coupon_id=coupon_id).first()
        print(f"Updating Coupon {coupon_id}")
        
        coupon.coupon_code = coupon_code
        coupon.coupon_discount = coupon_discount
        coupon.coupon_usage = coupon_usage_limit
        coupon.eligible_users = coupon_eligible_users
        db.session.commit()


        print(f"Coupon Details Updated")
        coupons = Coupons.query.all()

    return render_template('coupons.html', coupons=coupons)

@admin.route('/new-coupons', methods=['GET', 'POST'])
def new_coupon():
    if request.method == "POST":
        print(request.form)
        coupon_code = request.form.get('coupon_code')
        coupon_discount = request.form.get('coupon_discount')
        coupon_usage_limit = request.form.get('coupon_usage_limit')
        coupon_eligible_users = request.form.get('coupon_eligible_users')

        new_coupon = Coupons(
            coupon_code = coupon_code,
            coupon_discount = coupon_discount,
            coupon_usage = coupon_usage_limit,
            eligible_users = coupon_eligible_users,
        )
        db.session.add(new_coupon)
        db.session.commit()
        
    return render_template('new-coupon.html')