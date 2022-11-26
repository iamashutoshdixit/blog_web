from flask import Flask, request
import models
from flask_cors import CORS, cross_origin
from datetime import datetime
import traceback
import uttils
import random
import string
from passlib.hash import sha256_crypt

salt="As12!@#$%^&*"

app = Flask(__name__)
cors=CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"



@app.route("/")
def home():
    print(request.headers)
    return "Server is up and running!"

#signup api
@app.route("/user/signup/", methods = ["POST"])
def signup(db = models.session()):
    try:
        dict_data = request.get_json()
        check_email = db.query(models.User).filter(models.User.email==dict_data["email"]).all()
        if check_email != []:
            db.close()
            return {"detail":"this user is already exits"},400

        unhashed_pass = dict_data["password"] + salt
        password = sha256_crypt.encrypt(unhashed_pass)

        new_user_data = models.User(name = dict_data["name"],
                            user_name = dict_data["email"],
                            email = dict_data["email"],
                            password = password,
                            created_at = datetime.now() )


        db.add(new_user_data)
        db.commit()
        db.close()

        return {"message":"user has been registered"}, 201

        
    except Exception as e:
        traceback.print_exc()
        err = str(e)
        return {"detail":err}, 404


@app.route("/user/login/", methods = ["POST"] )
@cross_origin()
def login(db = models.session()):
    try:
        user_data = request.get_json()
        db_user = db.query(models.User).filter(models.User.email==user_data["email"]).all()
        db.close()
        if db_user == []:
            return {"detail": "user not found" }, 404
        db_user = db_user[0]
        db_password = db_user.password
        # to verify password
        check_password = sha256_crypt.verify(user_data["password"]+salt, db_password)
        print(check_password)
        if check_password == True:
            user_id = db_user.user_id
            jwt_token = uttils.get_jwt(user_id)
           
            return {"detail": "login succesfull", "token":jwt_token, "user_name":db_user.name} , 200
        return  {"detail":"invalid password"}, 404
    except Exception as e:
        traceback.print_exc()
        err = str(e)
        return {"detail":err}, 404




@app.route("/user/updatepassword/", methods=["POST"])
def updatepassword(db=models.session()):
    try:
        auth_headers=request.headers
        
        if "Authorization" not in  auth_headers:
            db.close()
            return {"details":"jwt token missing"}, 400

        auth_token = auth_headers["Authorization"].split(' ')[1]
        print(auth_token)
        user_id=uttils.decode_jwt(auth_token)
        
        if user_id is False:
            db.close()
            return {"details":"invalid token"}

        user_id = user_id["user_id"]
        dict_data=request.get_json()

        db_password=db.query(models.User).filter(models.User.user_id==user_id)
        # to check old /new pasword
        old_password=dict_data["old_password"]+salt
        check_password = sha256_crypt.verify(old_password, db_password[0].password)
        print(check_password)
        if check_password==False:
            db.close()
            return {"details":"wrong old password"}
        new_password = sha256_crypt.encrypt(dict_data["new_password"]+salt)
        
        db_password[0].password = new_password
        
        db.commit()
        db.close()
            
        return {"detail": "password succesfull updated"} , 200
         

    except Exception as e:
        traceback.print_exc()
        err = str(e)
        return {"detail":err}, 404 



        





