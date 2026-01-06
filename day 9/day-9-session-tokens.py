# Day 9: Sessions and logout handling
# The session object works like a dictionary and stores user data between requests.
# When a user logs out, we need to remove their identifier from the session.
# session.pop('user_id', None) safely deletes the key if it exists.
# Passing None prevents errors if the user is already logged out.
# This makes the logout process reliable and safe to call multiple times.
from flask import Flask, request,jsonify,session
import sqlite3
from create_db import get_db,init_db
init_db()
from werkzeug.security import generate_password_hash, check_password_hash


app=Flask(__name__)
app.secret_key="supersecretkey"
@app.route("/register",methods=["POST"])
def register_user():
    data=request.get_json()
    if not data:
        return jsonify({"success":False,"error":"no data provided"}),400
    email=data.get("email")
    password=data.get("password")
    if not email or not password:
        return jsonify({"success":False,"error":"email and password required"}),400
    hashed_password=generate_password_hash(password)
    try:
        with get_db()as conn:
            cursor=conn.cursor()
            cursor.execute("INSERT INTO users(email,password) VALUES(?,?)",(email,hashed_password))
            conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"success":False,"error":"email already registered"}),409
    return jsonify({"success":True,"message":"user registered successfully"}),201

@app.route("/login",methods=["POST"])
def login_user():
    data=request.get_json()
    if not data:
        return jsonify({"success":False,"error":"no data provided"}),400
    email=data.get("email")
    password=data.get("password")
    if not email or not password:
        return jsonify({"success":False,"error":"email and password required"}),400
    with get_db()as conn:
        cursor=conn.cursor()
        cursor.execute("SELECT id,password FROM users WHERE email=?",(email,))
        user=cursor.fetchone()
        if user is None:
            return jsonify({"success":False,"error":"user not found"}),400
        stored_password=user[1]
        if check_password_hash(stored_password,password):
            session['user_id']=user[0]
            return jsonify({"success":True,"message":"login successful"}),200
        return jsonify({"success":False,"error":"invalid credentials"}),401
    
@app.route("/dashboard",methods=["GET"])
def dashboard():
    if 'user_id' not in session:
        return jsonify({"success":False,"error":"unauthorized"}),401
    return jsonify({"success":True,"message":"welcome to your dashboard"}),200
 
@app.route("/logout",methods=["POST"])
def logout_user():
    session.pop('user_id',None)
    return jsonify({"success":True,"message":"logged out successfully"}),200

    