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
    #c.execute(t)
    conn.commit()

#login page
@app.route("/", methods=["GET","POST"])
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        button = request.form["b"]
        if button == "Login":
            validity = authenticate(username, password)
            if validity == "Valid":
                return render_template("index.html")
            else:
                return "Invalid"
        if button == "Sign_Up":
            add_user(username, password)
            return render_template("login.html")

#index page
#@app.route("/index", methods=["GET","POST"])
#def index():
   # if request.method=="GET":
   #     return render_template("index.html")
    #else:
     #   button = request.form["b"]
    #    name = request.form["name"]
      #  title = request.form["title"]
      #  blogpost = request.form["blog"]
       # if button=="cancel":
        #    return render_template("index.html")
        #else:
          #  add(name,title,blogpost)
          #  link = "<a href='http://localhost:5000/'" + title + ">here</a>"
           # return render_template("postadded.html",link=link)


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
    c.execute("SELECT * FROM User WHERE username = '%s'" % username)
    if c.fetchone() is None:
     return "Invalid"
    else:
     return "Valid"


#def add(n,t,b):
   # q = "INSERT INTO posts VALUES("
   # q += n + ","
   # q += t + ","
   # q += b + ")"
    #c.execute(q)
    #conn.commit()

if __name__=="__main__":
    app.debug = True
    app.run(host="0.0.0.0",port=5000)

