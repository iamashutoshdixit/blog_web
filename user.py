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


