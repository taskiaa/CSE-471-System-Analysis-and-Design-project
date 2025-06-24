from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
db = SQLAlchemy()
DB_NAME = "laundry.db"


def create_app():
    app = Flask(__name__,
                static_url_path='/',
                static_folder='static',
                template_folder='templates',
                )

    app.config['SECRET_KEY'] = "SUPERSECRETKEY123"
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root@localhost/laundry"

    db.init_app(app)
    migrate = Migrate(app, db)
    migrate.init_app(app, db)

    
    from .views import views
    from .auth import auth
    from .admin import admin
    from .provider import provider
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')
    app.register_blueprint(provider, url_prefix='/')
    from .models import RegularUser, AdminUser, Provider, Coupons 

    # from .models import User, Note

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(nid):
        print(nid)
        user = RegularUser.query.filter_by(nid=nid).first()
        if user:
            return user
        user = AdminUser.query.filter_by(nid=nid).first()
        if user:
            return user
        user = Provider.query.filter_by(nid=nid).first()
        if user:
            return user
        return None
    return app
