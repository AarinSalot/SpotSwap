from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from spotswap.config import DevelopmentConfig
from flask_jwt_extended import JWTManager
# from twilio.rest import Client
import csv
import os
import openai
from flask_cors import CORS
from config import Config
 
openai.api_key = Config.OPENAI

# print(os.getcwd())
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
    from spotswap.auth import utils
    from spotswap.auth.blocklist import BLOCKLIST
    from spotswap.main.routes import main
    from spotswap.models.Bookings import Bookings
    from spotswap.models.Parkings import Parkings
    from spotswap.models.User import User
    from spotswap.models.UserToken import UserToken
    from spotswap.models.Wallet import Wallet 
    from spotswap.models.Address import Address
    from spotswap.models.Availability import Availability
    # from iot_security.api.routes import api
    from spotswap.user.routes import user
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

    with app.app_context():
        db.create_all()
        db.session.commit()

    return app

def get_response(message):
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        temperature = 1,
        messages = [
            {"role": "user", "content": message}
        ]
    )
    rv = response.choices[0]["message"]["content"]
    return rv


def get_price(city):
    surrounding_price = get_response("Create a lower bound guess on the average hourly parking price in" + city + "Make the best possible guess you can." +
                       "Return only the price, and say nothing else.")
    our_price = get_response("A parking spot in LA is" + surrounding_price +  "on average. A homeowner wants to rent out the spot for a lower amount that makes" + 
                        "his offering competitive, what should be charge if he lists it on a company that takes 30 percent in commision fees. Do not provide an explaination just a final price.")
    clean = float(our_price.remove("$", ""))
    return our_price 




