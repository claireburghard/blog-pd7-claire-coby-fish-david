from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import csv

app = Flask(__name__)

conn = sqlite3.connect("database.db")
c = conn.cursor()
q = "create table if not exists User(username TEXT, password TEXT)"
t = "create table if not exists posts(name TEXT, title TEXT, blogpost TEXT, link TEXT, comments TEXT)"
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
    links = ""
    for l in c.fetchall():
        links += l[3]
    conn.commit()
    conn.close()
    return render_template("mainpage.html", links = links)

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
                return redirect(url_for('index'))
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
@app.route("/index", methods=["GET","POST"])
def index():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    name = "Needs Fixing"
    if request.method=="GET":
        return render_template("index.html", name=name)
    else:
        button = request.form["b"]
        name = request.form["name"]
        title = request.form["title"]
        blogpost = request.form["blog"]
        link = "localhost:5000/ind/" + title.replace(" ", "_")
        if button=="cancel":
            return render_template("index.html")
        else:
            q = "INSERT INTO posts VALUES("
            q += "'" + name + "',"
            q += "'" + title + "',"
            q += "'" + blogpost + "',"
            q += "'" + link +  "', '')"
            c.execute(q)
            conn.commit()
            conn.close()
            posts = get_posts()
            return render_template("postadded.html", name=name, posts=posts)

@app.route("/ind/<post_title>", methods=["GET", "POST"])
def postlink(post_title):
    title = post_title.replace("_", " ")
    blogpost = getpost(title)
    comments = getcomments(title)
    if request.method == "GET":
        return render_template("posts.html", title=title, blogpost = blogpost, comments = comments)
    else:
        comments = getcomments(title)
        #Now add the comment
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        comment = request.form["comment"]
        comments += comment
        q = "UPDATE posts SET comments = '%s'" %comments + "WHERE title = '%s'" % title
        c.execute(q)
        conn.commit()
        conn.close()
        return render_template("posts.html", title=title, blogpost = blogpost, comments = comments)

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

#for retrieving specific post
def getpost(title):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    d = "SELECT blogpost FROM posts WHERE title = '%s'" % title
    result = c.execute(d)
    ret = ""
    for r in result:
        ret += r[0]
    conn.commit()
    conn.close()
    return ret

#for retrieving a post's comments
def getcomments(title):
    #find old comments
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    q = "SELECT comments FROM posts WHERE title = '%s'" %title
    coms = c.execute(q)
    comments = ""
    for c in coms:
        comments += c[0]
    conn.commit()
    conn.close()
    return comments

if __name__=="__main__":
    app.debug = True
    app.run()

