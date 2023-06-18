from datetime import datetime, timedelta
import math,random
from flask_login import UserMixin
from spotswap import db

# Harshita
class Parkings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    bookings = db.relationship('Bookings', backref='parkings', lazy=True)
    availabilities = db.relationship('Availability', backref='parkings', lazy=True)
    # images = db.relationship('ParkingImage', backref='parking', lazy=True)
    
    def __str__(self):
        return 'Parkings: {}'.format(self.id)