# This code creates a Flask route to handle POST requests at "/register".
# It uses request.get_json() to read JSON data sent by the client.
# The function extracts the user's name, email, and password from the JSON.
# jsonify() formats a Python dictionary into a proper JSON response.
# When called, the route returns a success message confirming registration.

from flask import Flask,request,jsonify

app=Flask(__name__)
@app.route("/register", methods=["POST"])
def register():
    data=request.get_json()
    name=data.get("name")
    email=data.get("email")
    password=data.get("password")
    
    return jsonify({
        "success":True,
        "message":f"{name} registered successfully",
         "email":email
        })
    
    
if __name__=="__main__":
    app.run(debug=True)