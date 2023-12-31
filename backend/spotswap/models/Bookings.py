from datetime import datetime, timedelta
import math,random
# from werkzeug.security import generate_password_hash, check_password_hash
# from crop_analysis.models.utils import rand_pass
from flask_login import UserMixin
from spotswap import db


class Bookings(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parking_id = db.Column(db.Integer, db.ForeignKey('parkings.id'), nullable=False)
    start_time_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    end_time_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    payment_reference = db.Column(db.String(255), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    
    def __str__(self):
        return 'Bookings: {}'.format(self.id)

