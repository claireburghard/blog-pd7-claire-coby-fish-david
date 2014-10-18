from flask import Flask, render_template, request

app = Flask(__name__)

#index page
@app.route("/", methods=["GET","POST"])
def index():
    if request.method=="GET":
        return render_template("index.html")
    else:
        button = request.form["b"]
        name = request.form["name"]
        blogpost = request.form["blogpost"]
        if button=="cancel":
            return render_template("index.html")
        else:
            return render_template("posttest.html",
                                   name = name,
                                   text = blogpost)


if __name__=="__main__":
    app.debug = True
    app.run()
