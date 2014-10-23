from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import csv
from functions import add_user,authenticate,get_posts,getpost,get_name,getname,getcomments

#DIRECTORY
#"/":leads you to either login or register. Logging in brings you to "/home". Registering brings you to "/register"
#"/register":register page
#"/home":user's blog. Clicking "new post" brings you to "/index". Clicking "public posts" brings you to "/dashboard"
#clicking on the link to a post on the "/home" page brings you to "/ind/title_of_post"
#"/index":page where you make a new post
#"dashboard":all public posts

app = Flask(__name__)

conn = sqlite3.connect("database.db")
c = conn.cursor()
q = "create table if not exists User(username TEXT, name TEXT, password TEXT)"
t = "create table if not exists posts(name TEXT, title TEXT, blogpost TEXT, link TEXT, comments TEXT)"
c.execute(q)
c.execute(t)
conn.commit()
conn.close()

#login page
@app.route("/", methods=["GET","POST"])
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("login.html", message = "")
    else:
        global cur_user
        global cur_name
        username = request.form["username"]
        password = request.form["password"]
        button = request.form["b"]
        if button == "Login":
            validity = authenticate(username, password)
            if validity == "Valid":
                cur_user = username
                cur_name = get_name(username)
                return redirect(url_for('home'))
            else:
                return render_template("login.html", message = "Username/Password Invalid")
        else:
            return redirect(url_for('register'))
#register page
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
            add_user(username,name,password)
            return redirect(url_for('login'))
        else:
            return render_template("register.html", message = "Password doesn't match confirmation")

#user's blog
@app.route("/home", methods=["GET","POST"])
def home():
    if request.method=="GET":
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM posts WHERE name = '%s'" % cur_user)
        links = ""
        for l in c.fetchall():
            links += l[3]
        conn.commit()
        conn.close()
        return render_template("mainpage.html", links = links, name = cur_name)
    else:
        button = request.form["b"]
        if button == "New_Post":
            return redirect(url_for('index'))
        else:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute("SELECT * FROM posts WHERE name != '%s'" % cur_user)
            links = ""
            for l in c.fetchall():
                links += l[3]
            conn.commit()
            conn.close()
            return redirect(url_for('dashboard'))

#all public posts are displayed on the dashboard
@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    if request.method=="GET":
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM posts WHERE name != '%s'" % cur_user)
        links = ""
        for l in c.fetchall():
            links += l[3]
        conn.commit()
        conn.close()
        return render_template("dashboard.html", links = links)
    else:
        return redirect(url_for('home'))

#creating a new post
@app.route("/index", methods=["GET","POST"])
def index():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    name = cur_name
    if request.method=="GET":
        return render_template("index.html", name=name)
    else:
        button = request.form["b"]
        title = request.form["title"]
        blogpost = request.form["blog"]
        link = "localhost:5000/ind/" + title.replace(" ", "_")
        if button=="cancel":
            return render_template("index.html")
        else:
            q = "INSERT INTO posts VALUES("
            q += "'" + cur_user + "',"
            q += "'" + title.replace("'", "") + "',"
            q += "'" + blogpost.replace("'", "") + "',"
            q += "'" + link.replace("'", "") +  "', '')"
            c.execute(q)
            conn.commit()
            conn.close()
            posts = get_posts()
            return redirect(url_for('home'))

#individual post page
@app.route("/ind/<post_title>", methods=["GET", "POST"])
def postlink(post_title):
    title = post_title.replace("_", " ")
    blogpost = getpost(title)
    comments = getcomments(title)
    name = cur_name
    if request.method == "GET":
        return render_template("posts.html", title=title, blogpost=blogpost, name=name, comments=comments)
    else:
        comments = getcomments(title)
        #Now add the comment
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        comment = request.form["comment"]
        comments += comment + " - "  + cur_name + ' ' + "splittestholder123123"
        q = "UPDATE posts SET comments = '%s'" %comments + "WHERE title = '%s'" % title
        c.execute(q)
        conn.commit()
        conn.close()
        return render_template("posts.html", title=title, blogpost = blogpost, name=name, comments = comments)


if __name__=="__main__":
    app.debug = True
    cur_user = ""
    app.run()

