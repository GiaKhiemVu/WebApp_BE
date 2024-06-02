from flask import jsonify, make_response
import dbAction as db

def validateToken(auth_header):
    if not auth_header:
        return jsonify({'error': 'Authorization header missing'}), 401

    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Invalid authorization header'}), 401

    token = auth_header.split(' ')[1]
    if not db.check_valid_Token(token):
        return jsonify({'error': 'Authorization expired header'}), 401
    
    return
