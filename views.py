from flask import Blueprint
from flask import render_template, request
from flask import redirect
from flask import url_for
from flask_login import login_required, current_user, logout_user, login_user
from . import db
from .models import RegularUser, AdminUser, Provider, Coupons, Services, Orders
from .distances import calculate_distance

views = Blueprint('views', __name__, template_folder='templates/regular')


@views.route('/')
# @login_required
def index():
    print(current_user)
    return render_template('index.html')


@views.route('/dashboard')
@login_required
def dashboard():
    print(f"\n\n {current_user} \n\n")
    return render_template('dashboard.html')


@views.route('/apply-discount', methods=['GET', 'POST'])
def apply_discount():
    user = current_user
    message = None
    if request.method == "POST":
        print(request.form)
        coupon_code = request.form.get('code')
        coupon = Coupons.query.filter_by(coupon_code=coupon_code).first()
        if coupon:
            user = current_user
            user_type = 'premium' if user.premium_user else 'regular'

            coupon_type = coupon.eligible_users

            print(f"User Type: {user_type} | Coupon Type: {coupon_type}")

            if user_type == coupon_type or coupon_type == 'all':
                coupon_usage = coupon.coupon_usage
                if coupon_usage > 0:
                    coupon_usage -= 1
                    coupon.coupon_usage = coupon_usage
                    user.balance += coupon.coupon_discount
                    db.session.commit()

                    message = {
                        'type': 'success',
                        'title': f"Discount Applied",
                        'current_balance': f"Current Balance: {user.balance}",
                    }

                    print(f"Discount Applied")

                else:
                    print(f"Discount Limit Reached")
                    message = {
                        'type': 'error',
                        'title': f"Invalid Coupon Code",
                        'current_balance': f"Current Balance: {user.balance}",
                    }
        else:
            message = {
                'type': 'error',
                        'title': f"Invalid Coupon Code",
                        'current_balance': f"Current Balance: {user.balance}",
            }
            print(f"Invalid Coupon Code")
    return render_template('apply-discount.html', message=message)


@views.route('/find-services', methods=['GET', 'POST'])
def find_services():
    services = Services.query.all()
    return render_template('find-services.html', services=services)


@views.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == "POST":
        print(request.form)
        
        status = request.form.get('checkout_done')
        if status == 'ok':
            # change order status to confirmed
            user_cart_items = Orders.query.filter_by(order_user_id=current_user.nid).all()
            for item in user_cart_items:
                item.order_status = 'confirmed'
                db.session.commit()
            print("Order Confirmed")
            return render_template('checkout.html', message="Order Confirmed")
        
    user_cart_items_all = Orders.query.filter_by(order_user_id=current_user.nid).all()
    user_cart_items = []
    for item in user_cart_items_all:
        if item.order_status == 'pending':
            user_cart_items.append(item)
            
    item_total_price = 0
    for item in user_cart_items:
        item_total_price += item.order_price
    
    
    # print(f"{'='*10}")
    
    user_location = current_user.location
    # print(f"User Location: {user_location}")
    provider_location = user_cart_items_all[0].order_location
    # print(f"Provider Location: {provider_location}")
    # print(f"{'='*10}")
    
    
    
    
    user_balance = current_user.balance
    distance = calculate_distance(user_location, provider_location)
    shipping_charge = int(float(distance) * 10)
    
    total_price =  (item_total_price + shipping_charge) - (user_balance ) 

    
    return render_template('checkout.html', 
                        user_cart_items=user_cart_items, 
                        total_price=total_price,
                        sub_total=item_total_price,
                        discount=0,
                        user_balance=user_balance,
                        shipping_charge=shipping_charge,                        
                        )


@views.route('/add-to-cart/<int:service_id>', methods=['GET', 'POST'])
def add_to_cart(service_id):
    service = Services.query.filter_by(service_id=service_id).first()
    user = current_user

    new_order = Orders(
        order_user_id=user.nid,
        order_service_id=service.service_id,
        order_provider_id=service.service_provider_id,
        order_price=service.service_price,
        order_location=user.location,
        order_service_name=service.service_name,
    )
    db.session.add(new_order)
    db.session.commit()

    message = {
        'type': 'error',
        'title': f"Service Added to Cart",
    }

    return redirect(url_for('views.checkout'))


@views.route('/order-history', methods=['GET', 'POST'])
def order_history():
    user_orders = Orders.query.filter_by(order_user_id=current_user.nid).all()
    
    if request.method == "POST":
        print(request.form)
        order_provider_id = request.form.get('order_provider_id')
        new_rating = request.form.get('review')
        
        service_provider = Services.query.filter_by(service_id=order_provider_id).first()

        rating_count = service_provider.rating_count
        rating = service_provider.rating
        
        print(f"Rating_Count: {rating_count}")
        
        rating_count = int(rating_count) + 1
        rating = (rating + int(new_rating)) // rating_count
        
        
        service_provider.rating_count = rating_count
        service_provider.rating = rating
        db.session.commit()
        print(f"Rating: {rating} | Rating_Count: {rating_count}")

    return render_template('order-history.html', orders=user_orders)