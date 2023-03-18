'''
Demo

Prog:       Demo_1
Date:       17.03.2023

Youtube:    Web Development mit Flask Tutorial - Flask & Jinja2 Basics
            Coding Crashkurse
            https://www.youtube.com/watch?v=U5qrFwQreyg
'''

from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

database = []


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        vorname = request.form.get("fname")
        nachname = request.form.get("lname")
        user = {"id": random.randint(0,100), "name": f'{vorname} {nachname}' }
        database.append(user)
        return redirect(url_for("dashboard", login_id=user.get("id")))
    return render_template("login.html")

@app.route('/dashboard/<int:login_id>')
def dashboard(login_id):
    for entry in database:
        if entry.get("id") == login_id:
            return render_template("dashboard.html", person=entry)
    return render_template("404.html")


'''
  Starten in der Bereitstellung.
  Flask bringt seinen eigenen Webserver mit
'''
#if __name__ == '__main__':
    #from waitress import serve
    #serve(app, host='0.0.0.0', port=8080)

'''
  Starten wären der Entwicklung.

  In der Konsole folgendes ausführen:
    flask --app main.py --debug run --port 5000
'''


