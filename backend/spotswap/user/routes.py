from functools import wraps
from lib2to3.pgen2 import token
from math import radians, sin, cos, sqrt
from urllib import response
from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_user, current_user, login_required, logout_user
from spotswap.models import User, Address, Parkings, Wallet, Availability, Bookings
from spotswap.models.utils import rand_pass
from spotswap import db, jwt
from flask_sqlalchemy import func
from spotswap.utils.util_helpers import send_confirmation_mail
import json
from spotswap.user.utils import is_time_slot_available
from cerberus import Validator
from spotswap.auth.blocklist import BLOCKLIST
from flask_api import FlaskAPI, status, exceptions
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                                unset_jwt_cookies, jwt_required, JWTManager
from spotswap.models.Address import Address
from spotswap.models.Availability import Availability
    
user = Blueprint('user', __name__)


@user.route('/signup', methods=["POST"])
def create_account():
    request_body = request.get_json()
    org = User()
    org.first_name = request.json.get("first_name", None)
    org.last_name = request.json.get("last_name", None)
    org.phone_number = request.json.get("phone_number", None)
    org.is_renter = request.json.get("is_renter", None)
    org.email = request.json.get("email", None)
    org.valid_sm_code = False
    try:
        db.session.add(org)
        db.session.commit()
    except Exception as err:
        print('Error Logged : ', err)
        return "Could not register user", status.HTTP_400_BAD_REQUEST
    else:
        return "User Created", status.HTTP_201_CREATED


@user.route('/login', methods=['POST'])
def login():
    request_body = request.get_json()
    email = request.json.get("email", None)
    
    org = User.query.filter_by(email=email).first()
    if org is None:
        return "Email does not Exist", status.HTTP_401_UNAUTHORIZED
    else:
        User.generate_smcode(org.id, 180)
        data = {
            "message" : "OTP SENT"
            }
        return data, status.HTTP_200_OK


@user.route('/login/verify', methods=['POST'])
def login_verify():
    request_body = request.get_json()
    otp = request.json.get("otp", None)
    
    org = User.query.filter_by(sm_code=otp).first()
    if org is None:
        return "Invalid Otp", status.HTTP_401_UNAUTHORIZED
    else:
        access_token = create_access_token(identity=org.email)
        data = {
            "access_token" : access_token,
            "message" : "Login Successful"
            }
        return data, status.HTTP_200_OK


@user.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    print(user.id)
    data = {
            "message" : "Welcome To The Dashboard " + user.first_name + " " + user.last_name
            }
    return data, status.HTTP_200_OK


@user.route('/parking-lots', methods=['POST'])
@jwt_required()
def create_parking_lot():
    try:
        request_body = request.get_json()
        
        # Extract parking lot data from the request
        street = request_body.get('street')
        city = request_body.get('city')
        state = request_body.get('state')
        zip_code = request_body.get('zip')
        latitude = request_body.get('latitude')
        longitude = request_body.get('longitude')
        # price = request_body.get('price')
        user = User.query.filter_by(email=get_jwt_identity()).first()
        
        # Check if the address already exists
        address = Address.query.filter_by(street=street, city=city, state=state, zip=zip_code).first()
        if address is None:
            # Create a new Address object
            address = Address(street=street, city=city, state=state, zip=zip_code, latitude=latitude, longitude=longitude)
            db.session.add(address)
            db.session.commit()
        
        # Create a new Parking object associated with the Address
        
        ####################
        # ADD OPENAI LOGIC #
        ####################
        parking = Parkings(address_id=address.id, price=0, owner_id=user.id)
        # Set other relevant columns of the parking lot
        
        db.session.add(parking)
        db.session.commit()
        
        response_data = {
            'id': parking.id,
            'street': street,
            'city': city,
            'state': state,
            'zip': zip_code,
            'price': 0,
            # Include other relevant data in the response
        }
        return jsonify(response_data), 201
    
    except Exception as e:
        error_message = "An error occurred while creating the parking lot"
        user.logger.exception(error_message)
        return jsonify({'error': error_message}), 500





@user.route('/search', methods=['GET'])
def search_parking_lots():
    # Get the user's current location from the request
    user_latitude = float(request.args.get('latitude'))
    user_longitude = float(request.args.get('longitude'))

    # Define the search radius in kilometers (adjust as needed)
    search_radius = 5

    # Convert the search radius to meters for distance calculation
    search_radius_meters = search_radius * 1000

    # Perform a query to find relevant parking lots within the search radius
    nearby_parking_lots = Parkings.query.join(Address).filter(
        Parkings.address_id == Address.id,
        func.sqrt(
            func.pow(radians(user_latitude - Address.latitude), 2) +
            func.pow(radians(user_longitude - Address.longitude), 2)
        ) * 6371 <= search_radius
    ).all()

    # Create a list to store the results
    results = []

    # Iterate over the nearby parking lots and extract relevant information
    for parking_lot in nearby_parking_lots:
        # Retrieve the availability information for the parking lot
        availabilities = Availability.query.filter_by(parking_id=parking_lot.id, is_available=True).all()

        # Create a list to store the availability data
        availability_data = []

        # Iterate over the availabilities and extract relevant information
        for availability in availabilities:
            availability_info = {
                'date': availability.date.strftime('%Y-%m-%d'),
                'start_time': availability.start_time.strftime('%H:%M'),
                'end_time': availability.end_time.strftime('%H:%M'),
                'is_available': availability.is_available
            }
            availability_data.append(availability_info)

        result = {
            'id': parking_lot.id,
            'street': parking_lot.address.street,
            'city': parking_lot.address.city,
            'state': parking_lot.address.state,
            'zip': parking_lot.address.zip,
            'price': parking_lot.price,
            'availability': availability_data
            # Include other relevant data in the result
        }
        results.append(result)

    if len(results) == 0:
        return jsonify({'message': 'No parking lots found in the area'}), 404

    return jsonify(results), 200


@user.route('/parking-lots/<int:parking_id>/availability', methods=['POST'])
def add_parking_lot_availability(parking_id):
    parking_lot = Parkings.query.get_or_404(parking_id)

    request_body = request.get_json()
    date = request_body.get('date')
    start_time = request_body.get('start_time')
    end_time = request_body.get('end_time')
    is_available = request_body.get('is_available', True)

    # Create a new availability record for the parking lot
    availability = Availability(
        parking_id=parking_id,
        date=date,
        start_time=start_time,
        end_time=end_time,
        is_available=is_available
    )

    db.session.add(availability)
    db.session.commit()

    response_data = {
        'id': availability.id,
        'date': availability.date.strftime('%Y-%m-%d'),
        'start_time': availability.start_time.strftime('%H:%M'),
        'end_time': availability.end_time.strftime('%H:%M'),
        'is_available': availability.is_available
    }

    return jsonify(response_data), 201


@user.route('/parking-lots/<int:parking_id>/availability/<int:availability_id>', methods=['PUT'])
def update_parking_lot_availability(parking_id, availability_id):
    parking_lot = Parkings.query.get_or_404(parking_id)

    availability = Availability.query.filter_by(id=availability_id, parking_id=parking_id).first()
    if not availability:
        return 'Availability not found', status.HTTP_404_NOT_FOUND

    request_body = request.get_json()
    date = request_body.get('date')
    start_time = request_body.get('start_time')
    end_time = request_body.get('end_time')
    is_available = request_body.get('is_available', True)

    # Update the availability record
    availability.date = date
    availability.start_time = start_time
    availability.end_time = end_time
    availability.is_available = is_available

    db.session.commit()

    response_data = {
        'id': availability.id,
        'date': availability.date.strftime('%Y-%m-%d'),
        'start_time': availability.start_time.strftime('%H:%M'),
        'end_time': availability.end_time.strftime('%H:%M'),
        'is_available': availability.is_available
    }

    return jsonify(response_data), 200


@user.route('/parking-lots/<int:parking_id>/availability/<int:availability_id>', methods=['DELETE'])
def delete_parking_lot_availability(parking_id, availability_id):
    parking_lot = Parkings.query.get_or_404(parking_id)

    availability = Availability.query.filter_by(id=availability_id, parking_id=parking_id).first()
    if not availability:
        return 'Availability not found', status.HTTP_404_NOT_FOUND

    db.session.delete(availability)
    db.session.commit()

    return '', 204


@user.route('/parking-lots/<int:parking_id>/bookings', methods=['POST'])
@jwt_required()
def create_booking(parking_id):
    request_body = request.get_json()

    # Extract booking data from the request
    start_date = request_body.get('start_date')
    start_time = request_body.get('start_time')
    end_date = request_body.get('end_date')
    end_time = request_body.get('end_time')
    # Other booking data...

    user = User.query.filter_by(email=get_jwt_identity()).first()
    parking_lot = Parkings.query.get_or_404(parking_id)

    # Check if the requested time slot is available
    availability = Availability.query.filter_by(parking_id=parking_id, is_available=True).first()
    if availability is None or not is_time_slot_available(availability, start_date, start_time, end_date, end_time):
        return "Time slot is not available", 400

    # Create the booking
    booking = Bookings(
        customer_id=user.id,
        parking_id=parking_id,
        start_date=start_date,
        start_time=start_time,
        end_date=end_date,
        end_time=end_time
        # Other booking data...
    )

    # Update the availability based on the booked time slot
    if start_time > availability.start_time and end_time < availability.end_time:
        # Booking is within the availability time slot, split it into two availabilities
        remaining_availability_1 = Availability(
            parking_id=parking_id,
            date=availability.date,
            start_time=availability.start_time,
            end_time=start_time
        )
        remaining_availability_2 = Availability(
            parking_id=parking_id,
            date=availability.date,
            start_time=end_time,
            end_time=availability.end_time
        )

        # Mark the original availability as booked
        availability.is_available = False

        db.session.add_all([booking, remaining_availability_1, remaining_availability_2])
    elif start_time > availability.start_time:
        # Booking starts after the availability start time, update the availability end time
        availability.end_time = start_time
        db.session.add_all([booking, availability])
    elif end_time < availability.end_time:
        # Booking ends before the availability end time, update the availability start time
        availability.start_time = end_time
        db.session.add_all([booking, availability])
    else:
        # Booking covers the entire availability time slot, mark it as booked
        availability.is_available = False
        db.session.add_all([booking, availability])

    db.session.commit()

    response_data = {
        'booking_id': booking.id,
        'parking_lot_id': parking_lot.id,
        'street': parking_lot.address.street,
        'city': parking_lot.address.city,
        'state': parking_lot.address.state,
        'zip': parking_lot.address.zip,
        'start_date': booking.start_date.strftime('%Y-%m-%d'),
        'start_time': booking.start_time.strftime('%H:%M'),
        'end_date': booking.end_date.strftime('%Y-%m-%d'),
        'end_time': booking.end_time.strftime('%H:%M')
        # Include other relevant booking data in the response
    }

    return jsonify(response_data), 201



@user.route('/parking-lots', methods=['GET'])
def get_user_parking_lots(user_id):
    # Retrieve the user associated with the given user_id
    user = User.query.filter_by(email=get_jwt_identity()).first()
    
    # Retrieve the parking lots listed by the user
    parking_lots = Parkings.query.filter_by(owner_id=user.id).all()
    
    # Create a list to store the parking lot data
    parking_lot_data = []
    
    # Iterate over the parking lots and extract relevant information
    for parking_lot in parking_lots:
        parking_lot_info = {
            'id': parking_lot.id,
            'street': parking_lot.street,
            'city': parking_lot.city,
            'state': parking_lot.state,
            'zip': parking_lot.zip,
            'price': parking_lot.price,
            # Include other relevant data in the response
        }
        parking_lot_data.append(parking_lot_info)
    
    response_data = {
        'user_id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'parking_lots': parking_lot_data
    }
    
    return jsonify(response_data), 200


@user.route('/wallet/money-made', methods=['GET'])
@jwt_required()
def get_money_made():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    
    # Retrieve the wallet transactions for the user
    transactions = Wallet.query.filter_by(user_id=user.id).all()
    
    total_money_made = 0
    
    # Calculate the total money made by summing the positive transaction amounts
    for transaction in transactions:
        if transaction.amount > 0:
            total_money_made += transaction.amount
    
    response_data = {
        'user_id': user.id,
        'money_made': total_money_made
    }
    
    return jsonify(response_data), 200


@user.route('/bookings', methods=['GET'])
def get_user_bookings():
    user = User.query.filter_by(email=get_jwt_identity()).first()

    # Retrieve the user's bookings
    bookings = Bookings.query.filter_by(customer_id=user.id).all()

    # Create a list to store the booking data
    bookings_data = []
    for booking in bookings:
        booking_data = {
            'id': booking.id,
            'start_time': booking.start_time_date.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': booking.end_time_date.strftime('%Y-%m-%d %H:%M:%S')
            
        }
        bookings_data.append(booking_data)

    return jsonify(bookings_data), 200


# Error handler for 404 Not Found
@user.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not Found'}), 404


# Error handler for 500 Internal Server Error
@user.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500





@user.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    jti = get_jwt()["jti"]
    BLOCKLIST.add(jti)
    return response