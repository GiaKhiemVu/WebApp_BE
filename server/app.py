from flask import jsonify, make_response
from flask import Flask, request, jsonify, make_response
import dbAction as db
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv
from flask_cors import CORS
import json
import validateHeader as validate

load_dotenv()

app = Flask(__name__)
ver = 'v1.0'

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT'))
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app, supports_credentials=True)

mysql = MySQL(app)

# Test section
#######################################################################################


@app.route('/{}/api/test/<arg>'.format(ver), methods=['GET'])
def database(arg):
    print(arg)
    tables_json = db.get_all_table_data(arg)
    return jsonify({'data': tables_json})


@app.route('/{}/api/token'.format(ver), methods=['GET'])
def token():
    userData = db.get_loginInfo_by_account('123')
    personalData = db.get_personalInfo_by_loginId(userData['loginId'])
    del personalData['loginId']
    del personalData['userId']
    return personalData
#######################################################################################


@app.route('/{}/api/login'.format(ver), methods=['POST'])
def login():
    data = request.get_json()
    account = data.get('account')
    password = data.get('password')
    token = None
    message = "Login success"

    userData = db.get_loginInfo_by_account(account)

    if userData is None:
        message = "User doesn't exist"
    elif userData['password'] != password:
        message = "Incorrect password"
    else:
        token = db.update_user_token(account)

        resp = make_response({
            'message': message,
        })

        resp.set_cookie('token', token, httponly=False)
        return resp

    return jsonify({'message': message}), 401


@app.route('/{}/api/register'.format(ver), methods=['POST'])
def register():
    message = 'Create success'
    data = request.get_json()['data']
    userData = db.get_loginInfo_by_account(data['account'])
    if userData:
        message = "User already existed"
    else:
        db.create_new_user(data)

    return {
        'message': message,
    }


@app.route('/{}/api/getUser'.format(ver), methods=['GET'])
def getUser():
    auth_header = request.headers.get('Authorization')

    if auth_header:
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            if db.check_valid_Token(token):
                personalData = db.get_personalInfo_by_token(token)
                del personalData['token']
                del personalData['password']
                resp = make_response({
                    'message': 'User data retrieved successfully',
                    'user': personalData  # Include user data in the response
                })

                # Set user data in a cookie named 'user_info'
                resp.set_cookie('user_info', json.dumps(
                    personalData), httponly=False)
                return resp

            return jsonify({'message': 'Old Token or Invalid Token', 'token': token}), 200
        else:
            # If the Authorization header does not start with 'Bearer '
            return jsonify({'error': 'Invalid authorization header'}), 401
    else:
        # If no Authorization header is present in the request
        return jsonify({'error': 'Authorization header missing'}), 401


@app.route('/{}/api/getFullUserInfo'.format(ver), methods=['GET'])
def getFullUserInfo():
    auth_header = request.headers.get('Authorization')
    validate.validateToken(auth_header)

    data = db.get_full_user_info()
    res = make_response({
        'message': 'Get data success!',
        'data': data
    })
    
    return res


@app.route('/{}/api/getCategory'.format(ver), methods=['GET'])
def getCategory():
    auth_header = request.headers.get('Authorization')
    validate.validateToken(auth_header)

    data = db.get_category()
    res = make_response({
        'message': 'Get data success!',
        'data': data
    })

    return res

@app.route('/{}/api/getProduct'.format(ver), methods=['GET'])
@app.route('/{}/api/getProduct/<id>'.format(ver), methods=['GET'])
def getProduct(id=None):
    try:
        if id is not None:
            data = db.get_product_by_id(id)
            if data is None:
                return jsonify({'error': 'The product does not exist'}), 404
        else:
            data = db.get_product()

        return jsonify({'message': 'Get data success!', 'data': data})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/{}/api/getProductByCategory/<id>'.format(ver), methods=['GET'])
def getProductByCategory(id):
    try:
        if id is not None:
            data = db.get_product_by_category(id)
            if data is None:
                return jsonify({'error': 'The product does not exist'}), 404
        else:
            data = db.get_product()

        return jsonify({'message': 'Get data success!', 'data': data})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/{}/api/getProductByRecommend/<type>'.format(ver), methods=['GET'])
def getProductByRecommend(type):
    if type == "food":
        data = db.get_recommend_food()
    elif type == "drink":
        data = db.get_recommend_drink()
    else:
        return jsonify({'message': 'Invalid args'}), 404
    res = make_response({
        'message': 'Get data success!',
        'data': data
    })

    return res

@app.route('/{}/api/renewProduct'.format(ver), methods=['POST'])
def addProduct():
    auth_header = request.headers.get('Authorization')
    validate.validateToken(auth_header)
    data = request.get_json()['data']
    print(data)
    try:
        db.renew_product(data)
        return jsonify({"message": "Update success"}), 200

    except Exception as e:
        return jsonify({"message": "error on change data"}), 500


@app.route('/{}/api/createImg'.format(ver), methods=['POST'])
def createImg():
    auth_header = request.headers.get('Authorization')
    validate.validateToken(auth_header)
    try:
        data = request.get_json()['data']

        dataImg = db.get_image_by_Pid(data['Pid'])
        if (db.get_product_by_id(data['Pid'])):
            if dataImg is None:
                db.create_image(data)
                return jsonify({'message': 'Create success'}), 200
            else:
                db.update_image(data)
                return jsonify({'message': f'Update {data["Pid"]} success'}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({'message': 'Error processing request', 'error': str(e)}), 500


@app.route('/{}/api/addCart/<id>'.format(ver), methods=['POST'])
def addCart(id):
    auth_header = request.headers.get('Authorization')
    validate.validateToken(auth_header)
    data = request.get_json()['data']
    print(data)
    try:
        response, status_code = db.add_to_cart(data, id)

        return jsonify(response), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
