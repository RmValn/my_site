from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView 
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash
from flask_security import current_user, login_required, Security, SQLAlchemyUserDatastore, utils, logout_user

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)



login = LoginManager(app)
login.login_view = 'login'



bootstrap = Bootstrap(app)

from app import routers, models

user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)

admin = Admin(app, index_view=models.MyAdminIndexView())

admin.add_view(models.MyModelView(models.User, db.session))
admin.add_view(models.MyModelView(models.Role, db.session))
admin.add_view(models.MyModelView(models.Post, db.session))





@app.before_first_request
def create_user():
    admin_user = models.User.query.filter_by(email='valentyn@gmail.com').first()
    admin_role = models.Role.query.filter_by(name='admin').first()
    # user_datastore.delete_user(admin_user)
    # db.session.commit()
    if admin_user == None and admin_role == None:
        try:
            pass_hash = generate_password_hash('zzzzzzzz')
            user_datastore.create_role(name='admin', description='Administrator')
            first_user = user_datastore.create_user(email='valentyn@gmail.com',
                    password_hash=pass_hash, active=True, slug='1', firstname='admin', secondname='admin', roles=['admin'], username='valentyn')
            user_datastore.toggle_active(first_user)
            db.session.commit()
            logout_user()
            print('admin user created!')
        except:
            print('fail...')
