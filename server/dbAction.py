import json
from flask_mysqldb import MySQL
from flask import Flask
from getToken import getToken

app = Flask(__name__)
mysql = MySQL(app)

def get_loginInfo_by_account(account):
    try:
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM `logininfo` WHERE `account` = %s;"
        cursor.execute(query, (account,))
        row = cursor.fetchone()

        if row:
            columns = [desc[0] for desc in cursor.description]
            user_data = dict(zip(columns, row))
            return user_data
        else:
            return None

    except Exception as e:
        return {"Error": str(e)}

    finally:
        if cursor:
            cursor.close()

def get_personalInfo_by_loginId(loginId):
    try:
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM `personalinfo` WHERE `loginId` = %s;"
        cursor.execute(query, (loginId,))
        row = cursor.fetchone()

        if row:
            columns = [desc[0] for desc in cursor.description]
            user_data = dict(zip(columns, row))
            return user_data
        else:
            return None

    except Exception as e:
        return {"Error": str(e)}

    finally:
        if cursor:
            cursor.close()

def get_personalInfo_by_token(token):
    try:
        cursor = mysql.connection.cursor()
        query = """
            SELECT * FROM `logininfo` AS l
            JOIN `personalinfo` AS p ON l.loginId = p.loginId
            WHERE l.token = %s;
        """
        cursor.execute(query, (token,))
        row = cursor.fetchone()

        if row:
            columns = [desc[0] for desc in cursor.description]
            user_data = dict(zip(columns, row))
            return user_data
        else:
            return None

    except Exception as e:
        return {"Error": str(e)}

    finally:
        if cursor:
            cursor.close()

def get_loginInfo_by_token(token):
    try:
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM `logininfo` WHERE `token` = %s;"
        cursor.execute(query, (token,))
        row = cursor.fetchone()

        if row:
            columns = [desc[0] for desc in cursor.description]
            user_data = dict(zip(columns, row))
            return user_data
        else:
            return None

    except Exception as e:
        return {"Error": str(e)}

    finally:
        if cursor:
            cursor.close()

def create_new_user(userData):
    try:
        cursor = mysql.connection.cursor()

        insertUser = "INSERT INTO loginInfo(account, password) VALUES (%s, %s)"
        cursor.execute(
            insertUser, (userData['account'], userData['password']))

        query = "SELECT loginID FROM loginInfo WHERE account = %s AND password = %s;"
        cursor.execute(query, (userData['account'], userData['password']))
        row = cursor.fetchone()
        if row is not None:
            login_id = row[0]
        else:
            raise Exception
        print("login_id:", login_id)

        insertInfo = "INSERT INTO PersonalInfo(loginId, firstName, lastName, email) VALUES (%s, %s, %s, %s)"
        cursor.execute(insertInfo, (login_id, userData['firstName'], userData['lastName'],
                                    userData['email']))

        mysql.connection.commit() 
        print("Create success")

    except Exception as e:
        mysql.connection.rollback()  
        print("Error:", e)

    finally:
        if cursor:
            cursor.close()

def update_user_token(account):
    token = getToken(account)
    try:
        cursor = mysql.connection.cursor()
        query = "UPDATE `loginInfo` SET `token` = %s WHERE `account` = %s;"
        cursor.execute(query, (token, account))
        mysql.connection.commit()

        return token

    except Exception as e:
        print("Error:", e)
        return None

    finally:
        if 'cursor' in locals():
            cursor.close()

def check_valid_Token(token):
    try:
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM `personalinfo` WHERE `token` = %s;"
        cursor.execute(query, (token,))
        row = cursor.fetchone()

        if row:
            return True
        else:
            return False

    except Exception as e:
        return {"Error": str(e)}

    finally:
        if cursor:
            cursor.close()