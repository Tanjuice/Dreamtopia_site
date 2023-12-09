from crypt import methods
from doctest import debug
from flask import Flask, redirect, url_for, render_template, request, session, flash

from datetime import timedelta

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(days=5)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/kingdoms")
def kingdoms():
    return render_template("kingdoms.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

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


@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out, {user}", "info")
    session.pop("user", None)
    
    return redirect(url_for("login"))

@app.route("/fairygrowth")
def fairygrowth():
    return render_template("fairygrowth.html")



if __name__ == "__main__":
    app.run()