from flask import Flask, session, render_template,request, url_for,redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from itsdangerous import URLSafeTimedSerializer
import smtplib
import math,random

app = Flask(__name__)

# Configure session to use filesystem

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("postgres://tlkbyctryyffkn:b0ab12cc98ffab444f5d1d07329271b38c4e253f6cf3d1368bed287623e3dda8@ec2-54-235-86-101.compute-1.amazonaws.com:5432/d4bmrsh5lptv18")
db = scoped_session(sessionmaker(bind=engine))

notes = []
#notes.append(note)
# Python code to illustrate Sending mail from
# your Gmail account

def generateotp():
    digits = "0123456789"
    OTP =""
    for i in range(4):
        OTP+=digits[math.floor(random.random() *10)]
    return OTP

OTP = generateotp()

@app.route("/sendotp", methods=["POST"])
def sendotp():
    receiver_email = request.form.get("email_id")
    if receiver_email is None:
        return "Please Enter Email FIrst"
    print(receiver_email)
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login("software.engwkze@gmail.com", "April@2017")
    # message to be sent
    message = OTP
    # sending the mail
    s.sendmail("software.engwkze@gmail.com", receiver_email, message)
    # terminating the session
    s.quit()
    return "OTP has been sent!!"

@app.route("/otpcheck", methods=["POST"])
def otpcheck():
    entered_otp = request.form.get("entered_otp")
    if(entered_otp == OTP):
        print(entered_otp)
        return "Successfully Verified"
    else :
        return "Incorrect OTP"






@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == "POST" :
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        category = request.form.get('category')

        if category == "admin" :
            if (db.execute("SELECT * FROM admin WHERE userid=:username",{"username":username}).fetchone() is None) :
                db.execute("INSERT INTO admin (name,userid,password) VALUES (:name,:username,:password)",{"username":username, "name":name, "password":password})
                db.commit()
                message = ("Successfully Registered as Admin")
            else :
                message = ("Username Already exists")

        elif category == "faculty":
            if (db.execute("SELECT * FROM faculty WHERE userid=:username",{"username":username}).fetchone() is None) :
                db.execute("INSERT INTO faculty (name,userid,password) VALUES (:name,:username,:password)",{"username":username, "name":name, "password":password})
                db.commit()
                message = ("Successfully Registered as faculty")
            else :
                message = ("Username Already exists")

        else:
            if (db.execute("SELECT * FROM others WHERE userid=:username",{"username":username}).fetchone() is None) :
                db.execute("INSERT INTO others (name,userid,password) VALUES (:name,:username,:password)",{"username":username, "name":name, "password":password})
                db.commit()
                message = ("Successfully Registered as others")
            else :
                message = ("Username Already exists")

    else :
        message=(" ")

    return render_template("register.html",message=message)

@app.route("/")
def index():
    return render_template("slide.html")

@app.route("/login")
def login():
    message = ("")
    return render_template("login.html",message=message)

@app.route("/home",methods=["POST"])
def home():
    username =request.form.get("v_username")
    password = request.form.get("v_password")
    category = request.form.get("v_category")

    if category == "admin" :
        if (db.execute("SELECT * FROM admin WHERE userid=:username AND password=:password",{"username":username, "password":password}).fetchone() is None):
            message = ("Incorrect Username or Password Admin")
            return render_template("login.html",message=message)
        else :
            session["logged_user"]=username
            lists= db.execute("SELECT * FROM faculty_leave WHERE approved = 0").fetchall()
            #info = db.execute("SELECT * FROM faculty_info WHERE id=:id",{"id":id}).fetchall()
            return render_template("admin.html",lists=lists)

    elif category == "faculty" :
        query = db.execute("SELECT * FROM faculty WHERE userid=:username AND password=:password",{"username":username, "password":password}).fetchone()
        if (query is None):
            message = ("Incorrect Username or Password faculty")
            return render_template("login.html",message=message)
        else :
            session["logged_user"]=username
            id = query.id
            info = db.execute("SELECT * FROM faculty_info WHERE id=:id",{"id":id}).fetchone()
            leave = db.execute("SELECT * FROM faculty_leave WHERE id=:id",{"id":id}).fetchone()
            if (leave is None) :
                leaveapplied = 0;
            else :
                leaveapplied = 1;
            return render_template("home.html",userdetail = query,userinfo=info,leaveapplied=leaveapplied)

    else :
        if (db.execute("SELECT * FROM others WHERE userid=:username AND password=:password",{"username":username, "password":password}).fetchone() is None):
            message = ("Incorrect Username or Password Others")
            return render_template("login.html",message=message)
        else :
            session["logged_user"]=username
            return render_template("home.html")

@app.route("/admin")
def admin():
    ctr = 10;

@app.route("/rejoin")
def rejoin():
    return render_template("rejoining.html")

@app.route("/leave")
def leave():
    return render_template("leaveapplication.html")

@app.route("/stationleave")
def stationleave():
    return render_template("stationleave.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

def sendmail(id):
    emails = []
    names = []
    queries = db.execute("SELECT * FROM faculty WHERE id=:id",{"id":id}).fetchall()
    for query in queries:
        emails.append(query.userid)
        names.append(query.name)





if __name__ =="__main__":
    app.run(port=5000)
