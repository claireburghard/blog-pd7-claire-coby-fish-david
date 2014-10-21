from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import csv

app = Flask(__name__)

conn = sqlite3.connect("database.db")
c = conn.cursor()
q = "create table if not exists User(username TEXT, password TEXT)"
t = "create table if not exists posts(name TEXT, title TEXT, blogpost TEXT)"
c.execute(q)
c.execute(t)
conn.commit()
conn.close()

#login page
@app.route("/", methods=["GET","POST"])
def list_posts():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM posts")
    for row in c.fetchall():
        print row
    conn.commit()
    conn.close()
    return render_template("mainpage.html")

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
                return redirect(url_for('index', name=username))
            else:
                return render_template("login.html", message = "Username/Password Invalid")
        else:
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
@app.route("/index/<name>", methods=["GET","POST"])
def index(name):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    if request.method=="GET":
        return render_template("index.html", name=name)
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
            conn.commit()
            conn.close()
            #link = "<a href='http://localhost:5000/'" + title + ">here</a>"
            posts = get_posts()
            return render_template("postadded.html", name=name, posts=posts)

def add_user(username, password):
    conn = sqlite3.connect('database.db')
    c=conn.cursor();
    BASE="INSERT INTO User VALUES('" + username +"', '" + password + "')"
    c.execute(BASE)
    conn.commit()
    conn.close()
    return BASE + "user added"

def authenticate(username, password):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM User WHERE username = '%s'" % username + "and password = '%s'" % password)
    conn.commit()
    if c.fetchone() is None:
        conn.close()
        return "Invalid"
    else:
        conn.close()
        return "Valid"

def get_posts():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    d = """
    SELECT name,title,blogpost
    FROM posts
    """
    result = c.execute(d)
    conn.commit()
    test_print = "ARGH!"
    for r in result:
        test_print = test_print + r[2] + "<br>"
    conn.close()
    return test_print

if __name__=="__main__":
    app.debug = True
    app.run()

