from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from crop_analysis.config import DevelopmentConfig
from flask_jwt_extended import JWTManager
from twilio.rest import Client
import csv
import os
from flask_cors import CORS


print(os.getcwd())
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
jwt = JWTManager()
cors = CORS()
login_manager = LoginManager()
login_manager.login_message = 'Please login to continue'
login_manager.login_view = 'user.login'
login_manager.login_message_category = 'info'
# limiter = Limiter(key_func=get_remote_address)

def create_app(config=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.session_protection = "strong"
    mail.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    from crop_analysis.auth import utils
    from crop_analysis.auth.blocklist import BLOCKLIST
    from crop_analysis.main.routes import main
    from spotswap.models.Bookings import Bookings
    from spotswap.models.Parkings import Parkings
    from spotswap.models.User import User
    from spotswap.models.UserToken import UserToken
    from spotswap.models.Wallet import Wallet 
    # from iot_security.api.routes import api
    from crop_analysis.user.routes import user
    app.register_blueprint(user,url_prefix='/api/user')
    # app.register_error_handler(404, handle_error_404)
    # app.register_error_handler(500, handle_error_500)
    # app.register_error_handler(429, handle_error_429)
    # app.register_blueprint(user)
    # login_manager.blueprint_login_views = {
    #     'admin' : '/admin/login',
    #     'user' : '/user/login'
    # }
    app.register_blueprint(main)
    # app.register_blueprint(admin,url_prefix='/admin')
    # app.register_blueprint(user,url_prefix='/user')
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST


    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )


    # Meghana - Create Table and Insert
    with app.app_context():
        db.create_all()
        db.session.commit()
    
      
   

    return app
