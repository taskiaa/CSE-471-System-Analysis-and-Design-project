from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class RegularUser(UserMixin, db.Model):
    nid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    mobile = db.Column(db.String(150))
    user_type = db.Column(db.String(150), default='regular')
    balance = db.Column(db.Integer, default=0)
    location = db.Column(db.String(150), default='Dhanmondi')
    premium_user = db.Column(db.Boolean, default=False)
    
    # transactions = db.relationship('Transaction')
    def get_id(self):
        return self.nid
    
    def get_email(self):
        return self.email

class AdminUser(UserMixin, db.Model):
    nid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    mobile = db.Column(db.String(150))
    user_type = db.Column(db.String(150), default='admin')
    balance = db.Column(db.Integer, default=0)
    location = db.Column(db.String(150), default='')

    def get_id(self):
        return self.nid
    
    def get_email(self):
        return self.email
    
class Provider(UserMixin, db.Model):
    nid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    mobile = db.Column(db.String(150))
    user_type = db.Column(db.String(150), default='provider')
    balance = db.Column(db.Integer, default=0)
    location = db.Column(db.String(150), default='Banani')
    
    def get_id(self):
        return self.nid
    
    def get_email(self):
        return self.email

class Coupons(db.Model):
    coupon_id = db.Column(db.Integer, primary_key=True)
    coupon_code = db.Column(db.String(150), unique=True)
    coupon_discount = db.Column(db.Integer)
    coupon_usage = db.Column(db.Integer, default=1234)
    eligible_users = db.Column(db.String(150), default='all')
    

class Services(db.Model):
    service_id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(150))
    service_price = db.Column(db.Integer)
    service_description = db.Column(db.String(150))
    service_location = db.Column(db.String(150))
    service_provider_id = db.Column(db.Integer)
    rating = db.Column(db.Integer, default=0)
    rating_count = db.Column(db.Integer, default=0)
    
    
class Orders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime(timezone=True), default=func.now())
    order_status = db.Column(db.String(150), default='pending')
    order_user_id = db.Column(db.Integer)
    order_service_id = db.Column(db.Integer)
    order_provider_id = db.Column(db.Integer)
    order_price = db.Column(db.Integer)
    order_location = db.Column(db.String(150))
    order_service_name = db.Column(db.String(150))
