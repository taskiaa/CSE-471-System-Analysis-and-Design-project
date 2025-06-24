from flask import Blueprint
from flask import render_template, request
from flask import redirect
from flask import url_for
from flask_login import login_required, current_user, logout_user, login_user
from . import db 
import random
from .models import RegularUser, AdminUser, Provider, Coupons, Services, Orders
from .distances import calculate_distance


provider = Blueprint('provider', __name__, template_folder='templates/provider')

@provider.route('/add-new-service', methods=['GET', 'POST'])
def add_new_service():
    if request.method == "POST":
        print(request.form)
        
        new_service = Services(
            service_name = request.form.get('service_name'),
            service_price = request.form.get('service_price'),
            service_description = request.form.get('service_description'),
            service_location = request.form.get('service_location'),
            service_provider_id = current_user.nid
        )
        db.session.add(new_service)
        db.session.commit()
        
    print("Distance",calculate_distance("Gulshan", "Banani"))
    
    return render_template('add-new-service.html')

@provider.route('/manage-services', methods=['GET', 'POST'])
def manage_services():
    
    if request.method == "POST":
        print("POST")
        print(request.form)
        service_id = request.form.get('service_id')
        service_name = request.form.get('service_name')
        service_price = request.form.get('service_price')
        service_description = request.form.get('service_description')
        service_location = request.form.get('service_location')
        
        service = Services.query.filter_by(service_id=service_id).first()
        print(service)

        service.service_name = service_name
        service.service_price = service_price
        service.service_description = service_description
        service.service_location = service_location
        db.session.commit()
        
        print(f"Service Details Updated")

    
    services = Services.query.filter_by(service_provider_id=current_user.nid).all()
    return render_template('manage-services.html', services=services)

@provider.route('/manage-orders', methods=['GET', 'POST'])
def manage_orders():
    
    all_orders = Orders.query.all()
    print(all_orders)
    orders = []
    for order in all_orders:
        if order.order_provider_id == current_user.nid:
            orders.append(order)
        print(f"{order.order_provider_id=} {current_user.nid=}") 
    print(orders)
    if request.method == "POST":
        print("POST")
        print(request.form)
        order_id = request.form.get('order_id')
        order_status = request.form.get('new_status')
        
        order = Orders.query.filter_by(order_id=order_id).first()
        print(order)

        order.order_status = order_status
        db.session.commit()
        
        print(f"Order Status Updated")

    print(orders)
    return render_template('manage-orders.html', orders=orders)