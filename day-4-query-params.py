# Day 4 taught me how to accept user input through URL query parameters using request.args.
# I learned the difference between required parameters and optional ones with default values.
# I validated inputs to make sure the user provided correct and safe values before processing.
# I returned clear JSON responses showing either errors or the successful conversion result.
# This day helped me understand how real APIs handle dynamic input sent from clients.


from flask import Flask,request,jsonify

app=Flask(__name__)
@app.route("/convert")
def convert():
    amount=request.args.get("amount",type=float)
    rate=request.args.get("rate",default=100,type=float)
    
    if amount is None:
        return jsonify({
            "sucess":False,
            "error":"Amount parameter is required"
            
            
        }),400
        
    if amount<=0 or rate<=0:
        return jsonify ({
            "success":False,
            "error":"Amount and rate must be a positive numbers"
            
        }),400
        
        
    return jsonify({
        "success":True,
        "converted_amount":amount*rate,
        "message":"Conversion successful"    
        
    })
    
if __name__ =="__main__":
    app.run(debug=True)
        