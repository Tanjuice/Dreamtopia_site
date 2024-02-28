from crypt import methods
from doctest import debug
from enum import unique
from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import timedelta, datetime

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Secret Key
app.secret_key = "hello"

app.permanent_session_lifetime = timedelta(days=5)
# Add Database (sqlite)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
# Initialize the database
db = SQLAlchemy(app)

# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email =db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create String
    def __repr__(self):
        return "<Name %r>" % self.name
        app.app_context().push()
# Create Form Class
class NamerForm(FlaskForm):
    name = StringField("Whats your name", validators=[DataRequired()])
    submit = SubmitField("Submit")



# Page Routes
@app.route("/")
def index():
    return render_template("index.html")

# ----- Kingdoms Section -----
@app.route("/kingdoms")
def kingdoms():
    return render_template("kingdoms.html")

@app.route("/kingdoms/spawn")
def spawn():
    return render_template("spawn.html")

@app.route("/kingdoms/fairygrowth")
def fairygrowth():
    return render_template("fairygrowth.html")

# ----- Projects Section -----
@app.route("/projects")
def projects():
    return render_template("projects.html")

# ----- TEST Form Page -----
@app.route("/form", methods=["GET", "POST"])
def form():
    name = None
    form = NamerForm()
    # Validate
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
    return render_template("form.html", name=name, form=form)



# ----- Login/Logout Sections -----

# ----- Login -----
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        flash("Login succesful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in!")
            return redirect(url_for("user"))
        return render_template("login.html")

# ----- Logout -----
@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out, {user}", "info")
    session.pop("user", None)
    
    return redirect(url_for("login"))

# ----- User Sessions -----
@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

# Custom Error Messages

# -- 404 -- Page Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# -- 500 -- Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

# ----- Testing Section -----
# @app.route("/test")
# def projects():
#     return render_template("test.html")

if __name__ == "__main__":
    app.run()