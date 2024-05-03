from flask import request, Flask
import jwt
import datetime
import os

app = Flask(__name__)
secret = os.environ.get('SECRET_KEY')


def getToken(username):
    try:
        expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=30)
        token = jwt.encode(
            {'user': username, 'exp': expiration_time},
            secret,
            algorithm='HS256'
        )
        return token
    except Exception as e:
        print("Error generating token:", e)
        return None
