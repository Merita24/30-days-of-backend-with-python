# This code creates a basic Flask web application. 
# Flask() initializes the app and prepares it to handle web requests.
# @app.route("/") defines the URL path that triggers the function below it.
# The function returns a response that will be shown when that route is visited.
# app.run(debug=True) starts the local server and enables automatic reloads.

from flask import Flask,jsonify

app=Flask(__name__)

@app.route("/")
def home():
    return "Hello, there -Your Flask server is running"

@app.route("/about")
def about():
    return "This is a simple Flask application."

@app.route("/hello/<name>")
def hello(name):
    return f"hello,{name} welcome to Flask!"

@app.route("/square/<number>")
def square_number(number):
    return f"The square of {number} is {int(number)**2}"

@app.route("/user/<username>/<age>")
def user(username,age):
    return jsonify({
        "username":username,
        "age":age
         })
    
if __name__ == "__main__":
    app.run(debug=True)
