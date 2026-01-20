from flask import Flask,request,jsonify
import sqlite3
import jwt
import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from create_db import get_db,init_db
init_db()

app=Flask(__name__)
JWT_SECRET="supersecretkey"
JWT_ALGORITHM="HS256"
JWT_EXP_MINUTES=30

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
    role="user"
    try:
        with get_db()as conn:
            cursor=conn.cursor()
            cursor.execute("INSERT INTO users(email,role,password) VALUES(?,?,?)",(email,role,hashed_password))
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
     cursor.execute("SELECT id,email,role,password FROM users WHERE email=?",(email,))
     user=cursor.fetchone()
    if user is None:
        return jsonify({"success":False,"error":"user not found"}),400
    stored_password=user[3]
    if not check_password_hash(stored_password,password):
        return jsonify({"success":False,"error":"invalid credentials"}),401
    payload={
        "user_id":user[0],
        "email":user[1],
        "role":user[2],
        "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=JWT_EXP_MINUTES)
    }
    token=jwt.encode(payload,JWT_SECRET,algorithm=JWT_ALGORITHM)
    return jsonify({"success":True,"token":token}),200



def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        auth_header=request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"success":False,"error":"token is missing"}),401
        try:
            token=auth_header.split(" ")[1]
            decoded=jwt.decode(token,JWT_SECRET,algorithms=[JWT_ALGORITHM])
            request.user=decoded
        except jwt.ExpiredSignatureError:    
            return jsonify({"success":False,"error":"token has expired"}),401
        except jwt.InvalidTokenError:
            return jsonify({"success":False,"error":"invalid token"}),401
        return f(*args,**kwargs)
    
    return decorated

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def wrapped(*args,**kwargs):
            if request.user["role"]!=required_role:
                return jsonify({"success":False,"error":"Forbidden"}),403
            return f(*args,**kwargs)
        return wrapped
    return decorator


@app.route("/dashboard")
@token_required
def dashboard():
    return jsonify({"success":True,"message":"welcome to your dashboard!"}),200

@app.route("/admin")
@token_required
@role_required("admin")
def admin_route():
    return jsonify({"success":True,"message":"welcome admin!"}),200



if __name__=="__main__":
    app.run(debug=True)

