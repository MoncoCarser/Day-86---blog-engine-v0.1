from flask import Flask, redirect, render_template, session, request
from replit import db
import os
import datetime
import json

app = Flask(__name__)
app.secret_key = os.environ['session_key']


#db["Pasi"] = {"password": "pass123"}

#main page
    #view blog posts as a long list

def database_printer():
    entry = ""
    f = open("template.html", "r")
    entry = f.read()
    f.close()
    keys = db.keys()
    keys = list(keys)
    content = ""
    for key in reversed(keys):
        this_entry = entry
        if key != "Pasi":
            this_entry = this_entry.replace("{title}", db[key]["title"])
            this_entry = this_entry.replace("{body}", db[key]["blog_text"])
            content += this_entry
    return content


@app.route('/') 
def index():  
    if session.get("logged_in"):
        return redirect("/blog_writer")
    page = ""
    f = open("mainpage.html", "r")
    page = f.read()
    f.close()
    page = page.replace("{blog_printer}", database_printer())
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
        keys = db.keys() 
        username = form["username"]
        password = db[username]["password"]
        if form["username"] in keys:
            if form["password"] == password:
                session["logged_in"] = True
                session["name"] = username
                return redirect("/blog_writer")
            else: 
               return redirect("/")
        else: 
            return redirect("/")
    except:    
        return redirect("/")

@app.route("/blog_saved", methods=["POST"])
def blog_saved():
    form = request.form
    date = datetime.datetime.now()
    title = form["blog_title"]
    blog_text = form["blog_text"]
    db[date] = {"title": title, "blog_text": blog_text}
    return redirect("/blog_writer")


@app.route("/log_out")
def log_out():
    session.pop("logged_in", None)
    return redirect("/")
 
app.run(host='0.0.0.0', port=81)



