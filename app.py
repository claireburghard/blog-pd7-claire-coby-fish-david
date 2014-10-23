from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import csv

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

#index page
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
            q += "'" + replace_apos(title) + "',"
            q += "'" + replace_apos(blogpost) + "',"
            q += "'" + replace_apos(link) +  "', '')"
            c.execute(q)
            conn.commit()
            conn.close()
            posts = get_posts()
            return redirect(url_for('home'))


@app.route("/ind/<post_title>", methods=["GET", "POST"])
def postlink(post_title):
    t = post_title.replace("_", " ")
    title = '"""' + getback_apos(t) + '"""'
    b = getpost(title)
    blogpost = getback_apos(b)
    c = getcomments(title)
    comments = getback_apos(c)
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

def add_user(username,name,password):
    conn = sqlite3.connect('database.db')
    c=conn.cursor();
    BASE="INSERT INTO User VALUES('" + username +"', '" + name + "', '" +  password + "')"
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
    test_print = ""
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

#for retrieving a user's name
def get_name(username):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    d = "SELECT name FROM User WHERE username = '%s'" % username
    result = c.execute(d)
    ret = ""
    for r in result:
        ret += r[0]
    conn.commit()
    conn.close()
    return ret

#for retrieving a post writer's name
def getname(title):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    d = "SELECT name FROM posts WHERE title = '%s'" % title
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

def replace_apos(text):
    new = ""
    for r in text:
        if r == "'":
            new = new + "^"
        else:
            new = new + r
    return new

def getback_apos(text):
    old = ""
    for r in text:
        if r =="^":
            old = old + "'"
        else:
            old = old + r
    return old

if __name__=="__main__":
    app.debug = True
    cur_user = ""
    app.run()

