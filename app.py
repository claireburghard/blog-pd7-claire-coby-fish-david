from flask import Flask, render_template, request
import sqlite3
import csv

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    q = "create table User (username text, password text)"
    t = "create table posts (name TEXT, title TEXT, blogpost TEXT)"
    c.execute(q)
    c.execute(t)
    conn.commit()

#login page
@app.route("/", methods=["GET","POST"])
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("login.html", message = "")
    else:
        username = request.form["username"]
        password = request.form["password"]
        button = request.form["b"]
        if button == "Login":
            validity = authenticate(username, password)
            if validity == "Valid":
<<<<<<< HEAD
                index(username)
=======
                return index(username)
>>>>>>> 7e7556183ccadf02d7748b850f95200c5c4e4195
            else:
                return render_template("login.html", message = "Username/ Password Invalid")
        if button == "Sign_Up":
            add_user(username, password)
            return render_template("login.html", message = "Account Created")

#index page
@app.route("/index/<name>", methods=["GET","POST"])
def index(name):
    if request.method=="GET":
        return render_template("index.html")
    else:
        button = request.form["b"]
<<<<<<< HEAD
        name = request.form["name"]
=======
        name = name
>>>>>>> 7e7556183ccadf02d7748b850f95200c5c4e4195
        title = request.form["title"]
        blogpost = request.form["blog"]
        if button=="cancel":
            return render_template("index.html")
        else:
            add(name,title,blogpost)
            link = "<a href='http://localhost:5000/'" + title + ">here</a>"
            return render_template("postadded.html",link=link)


def add_user(username, password):
    conn = sqlite3.connect('test.db')
    c=conn.cursor();
    BASE="INSERT INTO User VALUES('" + username +"', '" + password + "')"
    
    c.execute(BASE)
    conn.commit()
    return BASE + "user added"

def authenticate(username, password):
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    c.execute("SELECT * FROM User WHERE username = '%s'" % username + "and password = '%s'" % password)
    if c.fetchone() is None:
        return "Invalid"
    else:
        return "Valid"


def add(n,t,b):
<<<<<<< HEAD
    q = "INSERT INTO posts VALUES("
    q += n + ","
    q += t + ","
    q += b + ")"
    c.execute(q)
    conn.commit()
=======
   q = "INSERT INTO posts VALUES("
   q += n + ","
   q += t + ","
   q += b + ")"
        c.execute(q)
        conn.commit()
>>>>>>> 7e7556183ccadf02d7748b850f95200c5c4e4195

if __name__=="__main__":
    app.debug = True
    app.run(host="0.0.0.0",port=5000)

