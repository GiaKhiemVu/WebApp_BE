from flask import Flask, request, jsonify
import dbAction as db
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv
from getToken import getToken
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
ver = 'v1.0'

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT'))
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app)

mysql = MySQL(app)


@app.route('/{}/api/database'.format(ver), methods=['GET'])
def database():
    tables_json = db.get_user_table()
    return jsonify({'tables': tables_json})


@app.route('/{}/api/token'.format(ver), methods=['GET'])
def token():
    return getToken('tnta')

@app.route('/{}/api/user'.format(ver), methods=['GET'])
def user():
    userData = db.get_user_by_account('huyton')
    return {
        'message': 'success',
        'data': userData,
    }


@app.route('/{}/api/login'.format(ver), methods=['POST'])
def login():
    data = request.get_json()
    account = data.get('account')
    password = data.get('password')
    token = None
    message = "Login success"

    userData = db.get_loginId_by_account(account)
    if userData == None:
        message = "User doesn't exist"
    else:
        if userData['password'] == password:
           token = db.update_user_token(account)

    return {
        'message': message,
        'data': {
            'token': token,
        },
    }


@app.route('/{}/api/register'.format(ver), methods=['POST'])
def register():
    message = 'Create success'
    data = request.get_json()['data']
    print(data)
    userData = db.get_loginId_by_account(data['account'])
    if userData:
        message = "User already existed"
    else:
        db.create_new_user(data)

    return {
        'message': message,
    }


@app.route('/{}/api/getUser'.format(ver), methods=['GET'])
def getUser():
    status = None
    account = request.get_json()['account']

    return account


if __name__ == '__main__':
    app.run(debug=True)
