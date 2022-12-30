from flask import Flask, redirect, render_template, session, request
from replit import db
import os

app = Flask(__name__)
app.secret_key = os.environ['session_key']

#below is user ID to log in to Replit database as the blog's owner
#db["user"] = {"username": "Pasi", "password": "pass123"}


def panties_for_yoshi():
    entry = ""
    f = open("./templates/template.html", "r")
    entry = f.read()
    f.close()
    keys = db.keys()
    keys = list(keys)
    content = ""
    for key in reversed(sorted(keys)):
        thisEntry = entry
        if key != "user":
            thisEntry = thisEntry.replace("{title}", db[key]["title"])
            thisEntry = thisEntry.replace("{date}", db[key]["date"])
            thisEntry = thisEntry.replace("{body}", db[key]["body"])
            content += thisEntry
    return content

@app.route('/') 
def index():  
    if session.get("logged_in"):
        return redirect("/blog_writer")
    page = ""
    f = open("./templates/mainpage.html", "r")
    page = f.read()
    f.close()
    page = page.replace("{blog_printer}", panties_for_yoshi())
    return page


@app.route('/blog_writer') 
def blog_writer():  
    if session.get("logged_in") == None:
       return redirect("/")
    return render_template("blogging.html")

@app.route('/log_in', methods=["POST"]) 
def log_in():  
    if session.get("logged_in"):
        return redirect("/blog_writer")
    try:
        form = request.form
        if form["username"] == db["user"]["username"] and form["password"] == db["user"]["password"]:
            session["logged_in"] = True
            return redirect("/blog_writer")
        else: 
           return redirect("/")
    except:    
        return redirect("/")

@app.route("/blog_saved", methods=["POST"])
def blog_saved():
    form = request.form
    entry = {"title": form["blog_title"], "date" : form["date"], "body": form["blog_text"]}
    db[form["date"]] = entry
    return redirect("/blog_writer")


@app.route("/log_out")
def log_out():
    session.pop("logged_in", None)
    return redirect("/")
 
app.run(host='0.0.0.0', port=81)



