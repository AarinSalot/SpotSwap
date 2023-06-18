# from functools import wraps
# from lib2to3.pgen2 import token
# from urllib import response
# from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
# from flask_login import login_user, current_user, login_required, logout_user

# user = Blueprint('user', __name__)

from functools import wraps
from lib2to3.pgen2 import token
from math import radians, sin, cos, sqrt
from urllib import response
from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_user, current_user, login_required, logout_user
from spotswap.models import User, Address, Parkings, Wallet
from spotswap.models.utils import rand_pass
from spotswap import db, jwt
from flask_sqlalchemy import func
from spotswap.utils.util_helpers import send_confirmation_mail
import json
from cerberus import Validator
from spotswap.auth.blocklist import BLOCKLIST
# from spotswap.schemas.user_apis import user_signup, user_login
from flask_api import FlaskAPI, status, exceptions
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                                unset_jwt_cookies, jwt_required, JWTManager

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








# @user.route('/confirmation/<string:token>')
# def email_confirmation(token):
#     # if current_user.is_authenticated:
#     #     return redirect(url_for('.dashboard'))

#     token_info = UserToken.query.filter_by(
#         token=token, token_type='email_confirmation').first()

#     if not token_info:
#         return "Token Not Found", status.HTTP_401_UNAUTHORIZED
#     if not token_info.is_valid():
#         return "Token Expired", status.HTTP_401_UNAUTHORIZED
#     token_info.user.email_verified = True
#     token_info.user.is_active = True

#     db.session.commit()
#     return "Mail Confirmation Successfull" ,status.HTTP_200_OK


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
        # price = request_body.get('price')
        user = User.query.filter_by(email=get_jwt_identity()).first()
        
        # Check if the address already exists
        address = Address.query.filter_by(street=street, city=city, state=state, zip=zip_code).first()
        if address is None:
            # Create a new Address object
            address = Address(street=street, city=city, state=state, zip=zip_code, latitude=None, longitude=None)
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
        result = {
            'id': parking_lot.id,
            'street': parking_lot.address.street,
            'city': parking_lot.address.city,
            'state': parking_lot.address.state,
            'zip': parking_lot.address.zip,
            'price': parking_lot.price,
            # Include other relevant data in the result
        }
        results.append(result)
    
    return jsonify(results), 200





# Error handler for 404 Not Found
@user.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not Found'}), 404


# Error handler for 500 Internal Server Error
@user.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500






# @user.route('/season', methods=['GET'])
# @jwt_required()
# def season_name():
#     season_data = []
#     season = Season.query.all()
#     print(season)
#     # write code from here. Get distrcit data and send it all to the user. do the same for season, crop, etc.
#     for i in season:
#         season_data.append(i.season_name)
#         # print(i.state_name)
#     data = {
#             "season" : season_data
#             }
#     return data, status.HTTP_200_OK




# @user.route('/crop', methods=['GET'])
# @jwt_required()
# def crop_name():
#     crop_data = []
#     crop = Crop.query.all()
#     print(crop)
#     # write code from here. Get distrcit data and send it all to the user. do the same for season, crop, etc.
#     for i in crop:
#         crop_data.append(i.crop_name)
#         # print(i.state_name)
#     data = {
#             "crop" : crop_data
#             }
#     return data, status.HTTP_200_OK


# @user.route('/myentries', methods=['GET'])
# @jwt_required()
# def myentries():
#     user = User.query.filter_by(email=get_jwt_identity()).first()
#     usercrop = UserCrop.query.filter_by(user_id=user.id).all()
#     print(usercrop)
#     result = []
#     if usercrop:
#         for j in usercrop:
    
#             cropdata = CropData.query.filter_by(crop_data_id=j.cropdata_id).all()
#             for i in cropdata:
#                 temp = {}
#                 cropname = Crop.query.filter_by(crop_id=i.crop_id).first()
#                 seasonname = Season.query.filter_by(season_id=i.season_id).first()
#                 districtname = District.query.filter_by(district_id=i.district_id).first()
#                 temp["cropdataid"] = i.crop_data_id
#                 temp["crop_name"] = cropname.crop_name
#                 temp["season_name"] = seasonname.season_name
#                 temp["district_name"] = districtname.district_name
#                 temp["area"] = i.area
#                 temp["production"] = i.production
#                 temp["yield_data"] = i.yield_data
#                 temp["profit"] = i.profit
#                 temp["rainfall"] = i.rainfall
#                 temp["year"] = i.year
#                 print(temp)
#                 result.append(temp)
#         print(result)
#         data = {
#             "crop" : result
#             }
#         return data, status.HTTP_200_OK
#     else:
#         return "No data found" ,status.HTTP_204_NO_CONTENT
    



# @user.route('/delete/cropdata', methods=['DELETE'])
# @jwt_required()
# def deletecropdata():
#     request_body = request.get_json()
#     cropid = request.json.get("crop_id", None)
#     print("sdasa",cropid)
#     try:
#         usercrop = UserCrop.query.filter_by(cropdata_id=cropid).delete()
#         cropdata = CropData.query.filter_by(crop_data_id=cropid).delete()
#         db.session.commit()
#     except Exception as err:
#         print('Error Logged : ', err)
#         return "Could not find crop data", status.HTTP_400_BAD_REQUEST
#     else:
#         return "Deleted Crop Data", status.HTTP_202_ACCEPTED
    

# @user.route('/update/cropdata', methods=['PUT'])
# @jwt_required()
# def updatecropdata():

#     cropid = request.json.get("crop_id", None)
#     cropdata = CropData.query.filter_by(crop_data_id=cropid).first()
#     print("ads", cropdata)
#     crop_name = request.json.get("crop_name", None)
#     season_name = request.json.get("season_name", None)
#     district_name = request.json.get("district_name", None)
#     area = request.json.get("area", None)
#     production = request.json.get("production", None)
#     yield_data = request.json.get("yeild_data", None)
#     profit = request.json.get("profit", None)
#     rainfall = request.json.get("rainfall", None)
#     year = request.json.get("year", None)
#     crop_id = Crop.query.filter_by(crop_name=crop_name).first()
#     season_id = Season.query.filter_by(season_name=season_name).first()
#     district_id = District.query.filter_by(district_name=district_name).first()

#     print(crop_id.crop_id)
#     print(season_id.season_id)
#     print(district_id.district_id)
#     # print(user.id)
#     print(area)
#     print(production)
#     print(yield_data)
#     print(profit)
#     print(rainfall)
#     print(year)



#     cropdata.crop_id = crop_id.crop_id
#     cropdata.season_id = season_id.season_id
#     cropdata.district_id = district_id.district_id
#     cropdata.area = area
#     cropdata.production = production
#     cropdata.yield_data = yield_data
#     cropdata.profit = profit
#     cropdata.rainfall = rainfall
#     cropdata.year = year

#     try:
#         db.session.commit()
#     except Exception as err:
#         print('Error Logged : ', err)
#         return "Could not update crop data", status.HTTP_400_BAD_REQUEST
#     else:
#         return "Updated Crop Data", status.HTTP_200_OK




# @user.route('/cropdata/add', methods=['POST'])
# @jwt_required()
# def crop_data_add():
#     request_body = request.get_json()
#     crop_name = request.json.get("crop_name", None)
#     season_name = request.json.get("season_name", None)
#     district_name = request.json.get("district_name", None)
#     area = request.json.get("area", None)
#     production = request.json.get("production", None)
#     yield_data = request.json.get("yeild_data", None)
#     profit = request.json.get("profit", None)
#     rainfall = request.json.get("rainfall", None)
#     year = request.json.get("year", None)
#     crop_id = Crop.query.filter_by(crop_name=crop_name).first()
#     season_id = Season.query.filter_by(season_name=season_name).first()
#     district_id = District.query.filter_by(district_name=district_name).first()
#     user = User.query.filter_by(email=get_jwt_identity()).first()
    
    
#     print(crop_id.crop_id)
#     print(season_id.season_id)
#     print(district_id.district_id)
#     print(user.id)
#     print(area)
#     print(production)
#     print(yield_data)
#     print(profit)
#     print(rainfall)
#     print(year)

#     cropdata = CropData()
#     cropdata.crop_id = crop_id.crop_id
#     cropdata.season_id = season_id.season_id
#     cropdata.district_id = district_id.district_id
#     cropdata.area = area
#     cropdata.production = production
#     cropdata.yield_data = yield_data
#     cropdata.profit = profit
#     cropdata.rainfall = rainfall
#     cropdata.year = year
    
#     try:
#         db.session.add(cropdata)
#         db.session.commit()
    
#     except Exception as err:
#         print('Error Logged : ', err)
#         return "Could not add crop data", status.HTTP_400_BAD_REQUEST
#     else:
#         usercrop = UserCrop()
#         usercrop.user_id = user.id
#         usercrop.cropdata_id = cropdata.crop_data_id
#         try:
#             db.session.add(usercrop)
#             db.session.commit()
#         except Exception as err:
#             print('Error Logged : ', err)
#             return "Could Not Map User and Crop", status.HTTP_400_BAD_REQUEST
#         else:
#             return "Data Added", status.HTTP_200_OK

    


@user.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    jti = get_jwt()["jti"]
    BLOCKLIST.add(jti)
    return response
  

# @user.route('/crop/visualize', methods=['POST'])
# @jwt_required()
# def crop_production_by_state():
#     district_name = request.json.get('district_name', '')
#     district_id = District.query.filter_by(district_name=district_name).first()
#     print("DSa", district_id.district_id)
#     crop_data = CropData.query.filter_by(district_id=district_id.district_id).all()
#     crop_data_obj = []
#     for crop in crop_data:
#         temp = {}
#         crop_id = Crop.query.filter_by(crop_id=crop.crop_id).first()
#         temp["crop_name"] = crop_id.crop_name
#         temp["area"] = crop.area
#         temp["production"] = crop.production
#         temp["yield_data"] = crop.yield_data
#         temp["profit"] = crop.profit
#         temp["rainfall"] = crop.rainfall
#         crop_data_obj.append(temp)
#     crops = {}
#     for data in crop_data_obj:
#         name = data['crop_name']
#         if name in crops:
#             crops[name]['profit'].append(data['profit'])
#             crops[name]['yield_data'].append(data['yield_data'])
#         else:
#             crops[name] = {'crop_name': name, 'profit': [data['profit']], 'yield_data': [data['yield_data']]}
    
#     result = []
#     for crop in crops.values():
#         crop['profit'] = sum(crop['profit']) / len(crop['profit'])
#         crop['yield_data'] = sum(crop['yield_data']) / len(crop['yield_data'])
#         result.append(crop)
#     result_final = {"data" : result}
#     return result_final, status.HTTP_200_OK
