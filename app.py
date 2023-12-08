from doctest import debug
from flask import Flask, redirect, url_for, render_template


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/kingdoms")
def kingdoms():
    return render_template("kingdoms.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")


if __name__ == "__main__":
    app.run()