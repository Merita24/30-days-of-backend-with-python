# Day 5 focused on building a POST route in Flask to handle login functionality.
# The route '/login' accepts JSON input containing email and password from the client.
# request.get_json() is used to read the incoming JSON data.
# We validate that both email and password are provided by the user.
# Additional checks ensure the email contains '@' and the password is at least 8 characters long.
# Depending on the input, the route returns structured JSON responses for success or errors with proper HTTP status codes.
# I used Postman to verify the route works correctly with valid and invalid data.
# This exercise helped me understand POST requests, input validation, and testing API endpoints effectively.


from flask import Flask,request,jsonify
app=Flask(__name__)
@app.route("/login",methods=["POST"])
def login():
    data=request.get_json()
    
    if not data :
        return jsonify({
            "success":False,
            "error":"No data provided"
            
        }),400
        
    email=data.get("email")
    password=data.get("password")
    
    if not email or not password:
        return jsonify({
            "success":False,
            "error":"Email and password not provided",
            
        }),400
        
        
    if "@" not in email:
        return jsonify({
            "success":False,
            "error":"Invalid email format",
        }),400
        
    if len(password)<8:
        return jsonify({
            "success":False,
            "error":"Password must be at least 8 characters long"
        }),400
        
    return jsonify({
        "success":True,
        "message":"Login successful"
    })
if __name__=="__main__":
    app.run(debug=True)