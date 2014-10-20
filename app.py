from flask import Flask, render_template, request
import sqlite3
import csv

app = Flask(__name__)

conn = sqlite3.connect('database.db')
c=conn.cursor();

def create():
    q = "create table posts (name TEXT, title TEXT, blogpost TEXT)"
    c.execute(q)
    conn.commit()

def add(n,t,b):
    q = "INSERT INTO posts VALUES("
    q += n + ","
    q += t + ","
    q += b + ")"
    c.execute(q)
    conn.commit()

#index page
@app.route("/", methods=["GET","POST"])
def index():
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
            add(name,title,blogpost)
            link = "<a href='http://localhost:5000/'" + title + ">here</a>"
            return render_template("postadded.html",link=link)

if __name__=="__main__":
    app.debug = True
    app.run()

conn.commit()

