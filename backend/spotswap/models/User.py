from datetime import datetime, timedelta
import math,random
# from werkzeug.security import generate_password_hash, check_password_hash
from spotswap.models.utils import rand_pass
from flask_login import UserMixin
from spotswap.utils.util_helpers import send_confirmation_mail
from spotswap import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    is_renter = db.Column(db.Boolean, default=False, nullable=False)
    
    #OTP 
    sm_code = db.Column(db.String(255), unique= True, nullable=True)
    valid_sm_sec = db.Column(db.Integer, nullable=True)
    valid_sm_code = db.Column(db.Boolean, default=False, nullable=False)
    sm_code_sent_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    tokens = db.relationship('UserToken', backref='user', lazy=True)
    parkings = db.relationship('Parkings', backref='user', lazy=True)
    bookings = db.relationship('Bookings', backref='user', lazy=True)
    wallet = db.relationship('Wallet', backref='user', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def __str__(self):
        return 'User: {}'.format(self.username)

    @staticmethod
    def generate_smcode(user_id, valid_sm_sec):
        OTP = rand_pass(9)                              # Generate password using rand_pass
        while User.query.filter_by(sm_code=OTP).first():
            OTP = rand_pass(9)                          #Incase OTP been generated before, create new one    
        user_token = User.query.filter_by(id=user_id).first()
        print ('OTP :', OTP)
        user_token.sm_code = OTP
        print (datetime.utcnow)
        user_token.valid_sm_sec = valid_sm_sec
        db.session.commit()
        send_confirmation_mail(user_token.email,OTP)
        return OTP

    # Check validity of password
    def is_valid(self):
        valid_till = self.sm_code_sent_at + timedelta(seconds=self.valid_sm_sec)
        return valid_till > datetime.utcnow()
