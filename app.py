from flask import Flask, render_template, request
import sqlite3
import csv

app = Flask(__name__)

conn = sqlite3.connect("database.db")
c = conn.cursor()
q = "create table if not exists User(username TEXT, password TEXT)"
t = "create table if not exists posts(name TEXT, title TEXT, blogpost TEXT)"
c.execute(q)
c.execute(t)

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
                index(username)
            else:
                return render_template("login.html", message = "Username/ Password Invalid")
                if button == "Register":
                    return redirect(url_for('register'))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method=="GET":
        return render_template("register.html", message = "")
    else:
        username = request.form["username"]
        password = request.form["password"]
        confirm = request.form["confirm_password"]
        name = request.form["name"]
        if (confirm == password):
            add_user(username, password)
            return redirect(url_for('login'))
        else:
            return render_template("register.html", message = "Password doesn't match confirmation")

#index page
@app.route("/", methods=["GET","POST"])
def index():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    if request.method=="GET":
        return render_template("index.html")
    else:
        button = request.form["b"]
        name = request.form["name"]
        title = request.form["title"]
        blogpost = request.form["blog"]
        if button=="cancel":
            return render_template("index.html")
        else:
            q = "INSERT INTO posts VALUES("
            q += "'" + name + "',"
            q += "'" + title + "',"
            q += "'" + blogpost + "')"
            c.execute(q)
            #link = "<a href='http://localhost:5000/'" + title + ">here</a>"
            return render_template("postadded.html",
                                   name=name)

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

    

if __name__=="__main__":
    app.debug = True
    app.run()

