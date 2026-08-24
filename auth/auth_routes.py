from werkzeug.security import generate_password_hash,check_password_hash
from flask import Flask,jsonify,request,Blueprint
from db import db

auth_bp=Blueprint("auth",__name__)

@auth_bp.route("/register",methods=["POST"])
def register_user():
    data=request.get_json()

    if not data:
        return jsonify({
            "error":"Request body is required"
        }),400

    if "username" not in data:
        return jsonify({
            "error":"Missing required field:username"
        }),400

    if "password" not in data:
        return jsonify({
            "error":"Missing required field:password"
        }),400

    username=data["username"]
    password=data["password"]

    hashed_password=generate_password_hash(password)

    cursor=db.cursor(dictionary=True)

    cursor.execute("INSERT INTO users (username,password) VALUES (%s,%s)",(username,hashed_password))

    db.commit()

    user_id=cursor.lastrowid
    cursor.close()
    return jsonify({
        "message":"Registration successfull",
        "user":{
            "id":user_id,
            "username":username
        }
    }),201

@auth_bp.route("/login",methods=["POST"])
def login_user():
    data=request.get_json()

    if not data:
        return jsonify({
            "error":"Request body is required"
        }),400

    if "username" not in data:
        return jsonify({
            "error":"Missing Required field:username"
        }),400

    if "password" not in data:
        return jsonify({
            "error":"Missing Required field:password"
        }),400

    username=data["username"]
    password=data["username"]

    cursor=db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE username=%s",(username,))

    user=cursor.fetchone()

    if not user:
        cursor.close()
        return jsonify({
            "error":"User not found"
        })

    if not check_password_hash(user["password"],password):
        return jsonify({
            "error":"Invalid username or password"
        })
    cursor.close()
    return jsonify({
        "message":"Login successful",
        "user":{
            "id":user["id"],
            "username":user["username"]
        }
    }),201
