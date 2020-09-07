from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

from flask_security import current_user, login_required, Security, SQLAlchemyUserDatastore, utils

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




# @app.before_first_request
# def before_first_request():

#     db.create_all()

#     user_datastore.find_or_create_role(name='admin', description='Administrator')

#     encrypted_password = utils.encrypt_password('admin')
#     if not user_datastore.get_user('someone@example.com'):
#         user_datastore.create_user(email='someone@example.com', password_hash=encrypted_password)

#     db.session.commit()

#     user_datastore.add_role_to_user('admin@example.com', 'admin')
#     db.session.commit()