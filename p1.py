import uuid
import pymongo
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = 'mydb'


client = pymongo.MongoClient('localhost', 27017)
db = client.mydb
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydb"


print(db)
@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/sign_up")
def signup():
    return render_template("login.html")

@app.route("/sign_in")
def sign_in():
    return render_template("sign_in.html")

@app.route("/sign_up", methods=['POST','GET'])
def index():
    if (request.method == 'POST'):
        user = {
        "_id": uuid.uuid4().hex,
        'name' : request.form.get('user'),
        'email' : request.form.get('mail'),
        'password' : request.form.get('password'),
        'password1' : request.form.get('password1'),}

        if user['password'] == request.form.get('password1'):
            if db.users.insert_one(user):
                return render_template("sign_in.html")

        else:
            return render_template("login.html")
    return render_template("login.html")


@app.route("/sign_in", methods=['POST','GET'])
def signin():
    if (request.method == 'POST'):

        user = db.users.find_one({
            "name": request.form.get('user'),
            "password" : request.form.get('password')})

        if user['password'] == request.form.get('password'):
            return render_template("regis.html")

        else:
            flash("Enter Valid Password")
            return render_template("sign_in.html")

    return render_template("sign_in.html")

@app.route("/regis")
def reg():
    return render_template("regis.html")

@app.route("/regis", methods=['POST','GET'])
def regis():
    if (request.method == 'POST'):
        registration = {
        "_id": uuid.uuid4().hex,
        'name' : request.form.get('user'),
        'email' : request.form.get('mail'),
        'password' : request.form.get('pass'),
        'phno': request.form.get('phno'),
        'add' : request.form.get('add'),
        'pin' : request.form.get('pin')
        }
        print(registration)

        if db.registrations.insert_one(registration):
            return render_template("payment.html")
    return render_template("regis.html")

@app.route("/payment")
def pay():
    return render_template("payment.html")

@app.route("/payment", methods=['POST', 'GET'])
def payment():
    import re
    if request.method == 'POST':
        payment ={
            "username" : request.form.get('username'),
            "cardNumber" : request.form.get('cardNumber'),
            "month" : request.form.get("month"),
            "year" : request.form.get("year"),
            "cvv" : request.form.get("cvv")
        }
        print(payment)

        def isValidCVVNumber(str):
            regex = "^[0-9]{3}$"

            p = re.compile(regex)

            if (str == None):
                return False

            if (re.search(p, str)):
                db.payment.insert_one(payment)
                return True
            else:
                return False

        str = request.form.get("cvv")
        print(isValidCVVNumber(str))
    return render_template("index.html")

@app.route("/payment", methods=['POST', 'GET'])
def payment2():
    import re
    if request.method == 'POST':
        payment ={
            "username" : request.form.get('username'),
            "cardNumber" : request.form.get('cardNumber'),
            "month" : request.form.get("month"),
            "year" : request.form.get("year"),
            "cvv" : request.form.get("cvv"),
        }
        print(payment)

        def isValidCVVNumber(str):
            regex = "^[0-9]{3}$"

            p = re.compile(regex)

            if (str == None):
                return False

            if (re.search(p, str)):
                db.payment.insert_one(payment)
                return True
            else:
                return False

        str = request.form.get("cvv")
        print(isValidCVVNumber(str))
    return render_template("index.html")

@app.route("/upi")
def upi_pay():
    return render_template("upi.html")

@app.route("/upi", methods=['POST', 'GET'])
def upi():
    if request.method == 'POST':
        upi_pay ={
            "username" : request.form.get('username'),
            "upiId" : request.form.get('upiId'),
            "upiPin" : request.form.get("upiPin"),
        }
        print(upi_pay)

        if db.payment.insert_one(upi_pay):
            return render_template("index.html")
    return render_template("payment.html")

@app.route("/ground")
def ground_book():
    return render_template("ground.html")

@app.route("/ground", methods=['POST', 'GET'])
def ground():
    if request.method == 'POST':
        ground ={
            "username" : request.form.get('username'),
            "password" : request.form.get('pass'),
            "phone_number" : request.form.get("phno"),
            # "sports" : request.form.get('select0'),
            # "ground_name": request.form.get('select1'),
            # "hrs": request.form.get('select2'),
        }
        print(ground)

        if db.ground.insert_one(ground):
            flash("Thank you for the payment!")
            return render_template("payment.html")
    return render_template("ground.html")


@app.route("/confirm")
def confirm():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

app.run(debug=True)