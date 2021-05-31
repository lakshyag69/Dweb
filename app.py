#!/usr/bin/python3
import subprocess
from flask import Flask, render_template, request, redirect, flash
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import current_user
from flask_login import login_user, logout_user
from flask_login import login_required
from sqlalchemy.util.langhelpers import methods_equivalent

app=Flask("myapp")
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///data/data.sqlite"
db=SQLAlchemy(app)
U_login=LoginManager(app)
class Users(UserMixin, db.Model):
    id=db.Column(db.Integer, primary_key=True)
    uname=db.Column(db.Text)
    email=db.Column(db.Text)
    passwd=db.Column(db.Text)

    def __init__(self, uname, email, passwd):
        self.uname=uname
        self.email=email
        self.passwd=passwd

db.create_all()

@U_login.user_loader
def load_user(id):
    return Users.query.get(int(id))


@app.route("/")
def home():
    return render_template("start.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/uadd", methods=["POST"])
def uadd():
        email = request.form.get('new-mail')
        uname = request.form.get('new-uname')
        password = request.form.get('new-psw')

        user = Users.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(uname) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = Users(uname=uname, email=email, passwd=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
        return redirect(url_for('home'))


@app.route("/login")
def login():
#    if current_user.is_authenticated:
#      return redirect(url_for('index'))
    return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/index", methods=["POST"])
def index():
    if request.method == 'POST':
        email = request.form.get('mail')
        password = request.form.get('psw')

        user = Users.query.filter_by(email=email).first()
        if user:
            if password == user.passwd:
                login_user(user, remember=True)
            else:
                redirect(url_for('login'))
        else:
            redirect(url_for('login'))
            
    cmd = "sudo docker ps --all"
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


