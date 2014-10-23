import sqlite3
import csv

#adding a user
def add_user(username,name,password):
    conn = sqlite3.connect('database.db')
    c=conn.cursor();
    BASE="INSERT INTO User VALUES('" + username +"', '" + name + "', '" +  password + "')"
    c.execute(BASE)
    conn.commit()
    conn.close()
    return BASE + "user added"

#authenticating user for login
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

#to print all posts on the blog
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

#wrote these methods to fix apostrophes but they aren't needed anymore
#def replace_apos(text):
#    new = ""
#    for r in text:
#        if r == "'":
#            new = new + ""
#        else:
#            new = new + r
#    return new

#def getback_apos(text):
#    old = ""
#    for r in text:
#        if r =="^":
#            old = old + "'"
#        else:
#            old = old + r
#    return old
