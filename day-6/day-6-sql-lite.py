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
  if not email or password:
      return jsonify({"success":False,"message":"email and password required"}),400
  try:
      with get_db() as conn:
          cursor=conn.cursor()
          cursor.execute("INSERT INTO users(email,password) VALUES(?,?)",(email,password))
          conn.commit()
  except sqlite3.IntegrityError:
        return jsonify({"success":False,"message":"email already registered"}),400      

  return jsonify({"success":True,"message":"user registered successfully"}),201

if __name__=="__main__":
    init_db()
    app.run(debug=True)