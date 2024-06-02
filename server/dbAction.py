import json
from flask_mysqldb import MySQL
from flask import Flask
from getToken import getToken
import base64

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


def get_full_user_info():
    try:
        cursor = mysql.connection.cursor()
        query = """
                SELECT * 
                FROM `PersonalInfo` 
                INNER JOIN `loginInfo` ON PersonalInfo.loginId = loginInfo.loginId
                """
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            user_data = []
            columns = [desc[0] for desc in cursor.description]
            for row in rows:
                user_data.append(dict(zip(columns, row)))
            return user_data
        else:
            return None

    except Exception as e:
        return {"Error": str(e)}

    finally:
        if cursor:
            cursor.close()


def get_product():
    try:
        cursor = mysql.connection.cursor()
        query = """
        SELECT Product.*, Image.ImageID, Image.Image
        FROM Product
        LEFT JOIN Image ON Product.Pid = Image.Pid;
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            product_data = []
            columns = [desc[0] for desc in cursor.description]
            for row in rows:
                data = dict(zip(columns, row))
                # Convert bytes data to base64 encoded string
                if data.get("Image"):
                    data["Image"] = base64.b64encode(
                        data["Image"]).decode("utf-8")
                product_data.append(data)
            return product_data
        else:
            return []

    except Exception as e:
        # Log the error for debugging
        print(f"Error fetching product data: {e}")
        return []

    finally:
        if cursor:
            cursor.close()


def get_product_by_id(id):
    try:
        cursor = mysql.connection.cursor()
        query = """
        SELECT Product.*, Image.ImageID, Image.Image
        FROM Product
        LEFT JOIN Image ON Product.Pid = Image.Pid
        WHERE Product.Pid = %s
        """
        cursor.execute(query, (id,))
        row = cursor.fetchone()

        if row:
            columns = [desc[0] for desc in cursor.description]
            product_data = dict(zip(columns, row))
            if product_data.get("Image") is not None:
                # Convert the binary image data to base64-encoded string
                product_data["Image"] = base64.b64encode(product_data["Image"]).decode("utf-8")
            return product_data
        else:
            return None

    except Exception as e:
        # Log the error for debugging
        print(f"Error fetching product data by ID: {e}")
        return {"Error": str(e)}

    finally:
        if cursor:
            cursor.close()


def get_product_by_category(id):
    try:
        cursor = mysql.connection.cursor()
        query = """
        SELECT Product.*, Image.ImageID, Image.Image
        FROM Product
        LEFT JOIN Image ON Product.Pid = Image.Pid
        WHERE Product.categoryId = %s
        """
        cursor.execute(query, (id,))
        rows = cursor.fetchall()

        if rows:
            product_data = []
            columns = [desc[0] for desc in cursor.description]
            for row in rows:
                data = dict(zip(columns, row))
                # Convert bytes data to base64 encoded string
                if data.get("Image"):
                    data["Image"] = base64.b64encode(
                        data["Image"]).decode("utf-8")
                product_data.append(data)
            return product_data
        else:
            return []

    except Exception as e:
        # Log the error for debugging
        print(f"Error fetching product data by ID: {e}")
        return {"Error": str(e)}

    finally:
        if cursor:
            cursor.close()


def create_image(imageData):
    cursor = None
    try:
        print(imageData)
        cursor = mysql.connection.cursor()

        insertImage = "INSERT INTO image(Pid, image) VALUES (%s, %s)"
        cursor.execute(insertImage, (imageData['Pid'], imageData['image']))

        query = "SELECT imageId FROM image WHERE Pid = %s AND image = %s;"
        cursor.execute(query, (imageData['Pid'], imageData['image']))
        row = cursor.fetchone()

        if row is not None:
            imageId = row[0]
        else:
            raise Exception("Image not found after insertion")

        mysql.connection.commit()
        print("imageId:", imageId)
        return imageId

    except Exception as e:
        if mysql.connection:
            mysql.connection.rollback()
        print("Error:", e)
        return None

    finally:
        if cursor:
            cursor.close()


def update_image(imageData):
    cursor = None
    try:
        cursor = mysql.connection.cursor()

        updateQuery = "UPDATE image SET image = %s WHERE Pid = %s"
        cursor.execute(updateQuery, (imageData['image'], imageData['Pid']))

        if cursor.rowcount == 0:
            raise Exception("No image found with the given Pid to update")

        mysql.connection.commit()
        print("Image updated successfully for Pid:", imageData['Pid'])
        return True

    except Exception as e:
        if mysql.connection:
            mysql.connection.rollback()
        print("Error:", e)
        return False

    finally:
        if cursor:
            cursor.close()


def get_image_by_Pid(Pid):
    cursor = None
    try:
        cursor = mysql.connection.cursor()

        query = "SELECT image FROM image WHERE Pid = %s"
        cursor.execute(query, (Pid,))
        row = cursor.fetchone()

        if row is not None:
            image = row[0]
            print("Image retrieved successfully for Pid:", Pid)
            return image
        else:
            raise Exception("No image found with the given Pid")

    except Exception as e:
        print("Error:", e)
        return None

    finally:
        # Close the cursor if it was initialized
        if cursor:
            cursor.close()


def get_category():
    try:
        cursor = mysql.connection.cursor()
        query = """
        SELECT *
        FROM Category
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            category = []
            columns = [desc[0] for desc in cursor.description]
            for row in rows:
                data = dict(zip(columns, row))
                category.append(data)
            return category
        else:
            return []

    except Exception as e:
        # Log the error for debugging
        print(f"Error fetching product data: {e}")
        return []

    finally:
        if cursor:
            cursor.close()


def get_recommend_food():
    try:
        cursor = mysql.connection.cursor()
        query = """
        SELECT * FROM Product
        WHERE recommend = 1 AND categoryId IN (1, 2, 3);
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            recommended_food = []
            columns = [desc[0] for desc in cursor.description]
            for row in rows:
                recommended_food.append(dict(zip(columns, row)))
            return recommended_food
        else:
            return []

    except Exception as e:
        return {"Error": str(e)}

    finally:
        if cursor:
            cursor.close()


def get_recommend_drink():
    try:
        cursor = mysql.connection.cursor()
        query = """
        SELECT * FROM Product
        WHERE recommend = 1 AND categoryId IN (4, 5, 6);
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            recommended_drink = []
            columns = [desc[0] for desc in cursor.description]
            for row in rows:
                recommended_drink.append(dict(zip(columns, row)))
            return recommended_drink
        else:
            return []

    except Exception as e:
        return {"Error": str(e)}

    finally:
        if cursor:
            cursor.close()


def get_all_table_data(table_name):
    try:
        cursor = mysql.connection.cursor()
        query = f"SELECT * FROM `{table_name}`;"
        cursor.execute(query)
        rows = cursor.fetchall()

        table_data = []
        for row in rows:
            columns = [desc[0] for desc in cursor.description]
            row_data = dict(zip(columns, row))
            table_data.append(row_data)

        return table_data

    except Exception as e:
        return {"Error": str(e)}

    finally:
        if cursor:
            cursor.close()
