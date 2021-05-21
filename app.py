#!/usr/bin/python3
import subprocess
from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy


app=Flask("myapp")
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///data/data.sqlite"
db=SQLAlchemy(app)
class Users(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    uname=db.Column(db.Text)
    email=db.Column(db.Text)
    passwd=db.Column(db.Text)

    def __init__(self, uname, email, passwd):
        self.uname=uname
        self.email=email
        self.passwd=passwd

db.create_all()

@app.route("/")
def home():
    return render_template("start.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/index", methods=["POST"])
def index():
    cmd=cmd = "sudo docker ps --all"
    output = subprocess.getoutput(cmd)
    container_list = output.split("\n")
    uname=request.form.get("new-uname")
    email=request.form.get("new-mail")
    psw=request.form.get("new-psw")
    return render_template("console.html", c_list=container_list)


@app.route("/reset", methods=["POST"])
def pass_reset():
    return render_template("password-reset.html")

@app.route("/project")
def project():
    return render_template("project.html")


@app.route("/launch", methods=["POST"])
def launch():
    c_name=request.form.get("x")
    x=subprocess.getoutput("sudo docker run -d -i -t  --name {} party:latest".format(c_name))
    ip_addr=subprocess.getoutput("sudo docker inspect --format '{{.NetworkSettings.IPAddress}}' {}".format(c_name))
    y=subprocess.getoutput("sudo docker exec -d {} sed -i 's/lakshyagupta/{}/' /etc/sysconfig/shellinaboxd".format(c_name,ip_addr))
    z=subprocess.getoutput("sudo docker exec -d {} /usr/sbin/shellinaboxd --disable-ssl -b".format(c_name))
    return redirect(url_for("index"), code=307)

app.run(host='localhost', port=80, debug=True)


