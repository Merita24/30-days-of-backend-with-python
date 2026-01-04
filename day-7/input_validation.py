# Day 7: Input validation and basic security
# I focused on making sure the backend only accepts clean and valid data
# The API checks for missing fields, invalid usernames, and weak passwords
# Passwords are hashed before being saved to protect user information
# This helps prevent errors, misuse, and security issues early on

from flask import Flask,request,jsonify
from create_db import get_db,init_db
from werkzeug.security import generate_password_hash, check_password_hash

import sqlite3

app=Flask(__name__)

@app.route("/add_user",methods=["POST"])
def add_user():
    valid_domain_names=["gmail.com","yahoo.com","outlook.com"]

    data=request.get_json()
    if not data:
        return jsonify({"success":False,"message":"no data provided"}),400
    username=data.get("username")
    email=data.get("email")
    raw_password=data.get("password")
    if not email or not username or not raw_password:
        return jsonify({"success":False,"message":"username,email and password required"}),400
    if not any((char.isdigit)for char in username):
        return jsonify({"success":False,"message":"username must contain at least one number"}),400
    if username[0].isdigit():
        return jsonify({"success":False,"message":"username cannot start with a number"}),400
    if "@" not in email:
        return jsonify({"success":False,"message":"invalid email format"}),400
    if email.split("@")[1] not in valid_domain_names:
        return jsonify({"success":False,"message":"Invalid email domain"}),400
    if len(raw_password)<8:
        return jsonify({"success":False,"message":"Password must be 8 characters long"}),400
    hashed_password=generate_password_hash(raw_password)
    try:
        with get_db() as conn:
            cursor=conn.cursor()
            cursor.execute("INSERT INTO test(email,username,password)VALUES(?,?,?)",(email,username,hashed_password))
            conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"success":False,"message":"email already registered"}),400
    return jsonify({"success":True,"message":"user added successfully"})