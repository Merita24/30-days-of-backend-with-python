# Day 8: Authentication
# This code handles user registration and login.
# Passwords are hashed before storing to keep them secure.
# When users log in, their input is checked against the hashed password.
# The database stores email and password information safely.
# This is the foundation for building secure login systems in web apps.

from flask import Flask,request,jsonify
import sqlite3
from create_db import get_db,init_db
init_db()
from werkzeug.security import generate_password_hash,check_password_hash

app=Flask(__name__)

@app.route('/register',methods=["POST"])
def register_user():
    data=request.get_json()
    if not data:
        return jsonify({"success":False,"error":"no data provided"}),400
    email=data["email"]
    password=data["password"]
    if not email or not password:
        return jsonify({"success":False,"error":"email and password required"}),400
    hashed_password=generate_password_hash(password)
    with get_db()as conn:
        cursor=conn.cursor()
        cursor.execute('INSERT INTO login(email,password) VALUES(?,?)',(email,hashed_password))
        conn.commit()
        
    return jsonify({"success":True,"message":"user registered successfully"}),200

@app.route('/login',methods=['POST'])
def login_user():
    data=request.get_json()
    if not data:
        return jsonify({"success":False,"error":"no data provided"}),400
    email=data["email"]
    password=data["password"]
    if not email or not password:
        return jsonify({"success":False,"error":"email and password required"}),400
    with get_db()as conn:
        cursor=conn.cursor()
        cursor.execute("SELECT password FROM login WHERE email=?",(email,))
        user=cursor.fetchone()
        if user is None:
            return jsonify({"success":False,"error":"user not found"})
        stored_password=user[0]
        if check_password_hash(stored_password,password):
            return jsonify({"success":True,"message":"login successful"}),200
        return jsonify({"success":False,"error":"invalid credentials"}),400
        
            
        
if __name__=="__main__":
    app.run(debug=True)      
    