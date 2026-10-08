from flask import Flask, request, render_template, jsonify
import jinja2
import json
import predict as pred

app = Flask(__name__)

@app.route("/imnosy")
def helloworld():
    return render_template("index.html")

@app.route("/", methods=["GET", "POST"])
def predict():
    year, make, model, price = None, None, None, None
    if request.method == "POST":
        miles = request.form.get("miles-input")
        year = request.form.get("year-input")
        enginesize = request.form.get("enginesize-input")
        make = request.form.get("make")
        model = request.form.get("model")
        body = request.form.get("body")
        drivetrain = request.form.get("drivetrain")
        transmission = request.form.get("transmission")
        fuel = request.form.get("fuel")
        for name, value in request.form.items():
            print(f"{name}: {value}")
        price = pred.predict(miles, year, enginesize, make, model, body, drivetrain, transmission, fuel)
        print("price:", price)
        
    #browser automatically sends "GET" request    
    return render_template("predict.html", year = year, make = make, model = model, price = price)

@app.route("/options", methods=["GET"])
def send_options():
    with open("./model/encoded_categories.json", "r") as file:
        options = json.load(file)
    return jsonify(options)

if __name__ == "__main__":
    app.run(debug=True)