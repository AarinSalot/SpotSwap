from datetime import datetime, timedelta
import math,random
# from werkzeug.security import generate_password_hash, check_password_hash
# from crop_analysis.models.utils import rand_pass
from flask_login import UserMixin
from spotswap import db


class Wallet(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Integer, default=0, nullable=False)
    
    # -- Backrefrences for other tables
    # property_id = db.relationship('Property',backref='user',lazy=True)
    # tenant_id = db.relationship('Tenant',backref='user',lazy=True)
    # support_id = db.relationship('Supportquery',backref='user',lazy=True)
    
    def __str__(self):
        return 'User: {}'.format(self.username)

