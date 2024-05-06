from flask import Flask, request, jsonify, make_response
import dbAction as db
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv
from getToken import getToken
from flask_cors import CORS
import json

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


@app.route('/{}/api/database'.format(ver), methods=['GET'])
def database():
    tables_json = db.get_user_table()
    return jsonify({'tables': tables_json})


@app.route('/{}/api/token'.format(ver), methods=['GET'])
def token():
    userData = db.get_loginInfo_by_account('123')
    personalData = db.get_personalInfo_by_loginId(userData['loginId'])
    del personalData['LoginId']
    del personalData['UserId']
    return personalData


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
    print(data)
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
            if(db.check_valid_Token(token)):
                personalData = db.get_personalInfo_by_token(token)
                resp = make_response({
                    'message': 'get User Successfully',
                })

                del personalData['token']
                del personalData['password']

                resp.set_cookie('user_info', json.dumps(personalData), httponly=False)
                return resp

            return jsonify({'message': 'Old Token or Invalid Token', 'token': token}), 200
        else:
            # If the Authorization header does not start with 'Bearer '
            return jsonify({'error': 'Invalid authorization header'}), 401
    else:
        # If no Authorization header is present in the request
        return jsonify({'error': 'Authorization header missing'}), 401

    return


if __name__ == '__main__':
    app.run(debug=True)
