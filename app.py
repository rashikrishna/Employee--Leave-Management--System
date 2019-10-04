from flask import Flask, session, render_template,request, url_for,redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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

@app.route("/", methods=["GET","POST"])
def index():

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

    return render_template("index.html",message=message)

@app.route("/home",methods=["POST"])
def home():
    username =request.form.get("v_username")
    password = request.form.get("v_password")
    category = request.form.get("v_category")

    if category == "admin" :
        if (db.execute("SELECT * FROM admin WHERE userid=:username AND password=:password",{"username":username, "password":password}).fetchone() is None):
            message = ("Incorrect Username or Password Admin")
            return render_template("index.html",message=message)
        else :
            session["logged_user"]=username
            lists= db.execute("SELECT * FROM faculty_leave WHERE approved = 0").fetchall()
            return render_template("admin.html",lists=lists)

    elif category == "faculty" :
        query = db.execute("SELECT * FROM faculty WHERE userid=:username AND password=:password",{"username":username, "password":password}).fetchone()
        if (query is None):
            message = ("Incorrect Username or Password faculty")
            return render_template("index.html",message=message)
        else :
            session["logged_user"]=username
            return render_template("home.html",userdetail = query)

    else :
        if (db.execute("SELECT * FROM others WHERE userid=:username AND password=:password",{"username":username, "password":password}).fetchone() is None):
            message = ("Incorrect Username or Password Others")
            return render_template("index.html",message=message)
        else :
            session["logged_user"]=username
            return render_template("home.html")

@app.route("/admin")
def admin():
    ctr = 10;

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ =="__main__":
    app.run(port=5000)
