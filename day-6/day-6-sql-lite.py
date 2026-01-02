# Day 6: Learned how to do basic CRUD with Flask and SQLite.
# Created a simple users database and table for storing emails and passwords.
# Built routes to add, view, update, and delete users.
# Made sure the app checks that email and password are provided before saving.
# Handled errors like duplicate emails gracefully.
# Used Python's 'with' to safely open and close the database connection.
# Got a clear picture of how data moves from requests to the database.
from flask import Flask,request,jsonify
from create_db import get_db, init_db
import sqlite3

app=Flask(__name__)
@app.route("/register",methods=["POST"])
def register():
    data=request.get_json()
    if not data :
        return jsonify({"success":False,"message":"no data provided"}),400
    email=data.get("email")
    password=data.get("password")  
    if not email or not password:
        return jsonify({"success":False,"message":"email and password required"}),400
    try:
        with get_db() as conn:
            cursor=conn.cursor()
            cursor.execute("INSERT INTO users(email,password) VALUES(?,?)",(email,password))
            conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"success":False,"message":"email already registered"}),400      

    return jsonify({"success":True,"message":"user registered successfully"}),201

@app.route("/users",methods=["GET"])
def get_users():
    with get_db() as conn:
        cursor=conn.cursor()
        cursor.execute("SELECT id,email FROM users")
        users=cursor.fetchall()
    
    return jsonify({"success":True,"data":[{"id":u[0],"email":u[1]} for u in users]})
 
@app.route("/users/<int:user_id>",methods=["PUT"])
def update_user(user_id):
    data=request.get_json()
    new_email=data.get("email")
    if not new_email:
        return jsonify({"success":False, "error":"new email required"}),400
    try:
        with get_db() as conn:
            cursor=conn.cursor()
            cursor.execute("UPDATE users SET email=? where id=?",(new_email,user_id))
            conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"sucess":False,"error":"email already exists"}),400
    return jsonify({"success":True,"message":"user email updated successfully"})

@app.route("/users/<int:user_id>",methods=["DELETE"])
def delete_user(user_id):
    with get_db() as conn:
        cursor=conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=?",(user_id,))
        conn.commit()
        
    return jsonify({"success":True,"message":"user deleted successfully"})
            



if __name__=="__main__":
    init_db()
    app.run(debug=True)