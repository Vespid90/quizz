from flask import Flask, render_template, request, redirect, url_for
import requests


classement={"farid LeGoat","Larry LeMalicieux" ,"Jojo L'astico" ,"Tatiana LaGoat"}
#from config import base
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
   return render_template("login.html")


@app.route("/sign_up")
def sing_up():
   return render_template("sign_up.html")

@app.route("/quiz")
def quiz():
   return render_template("quiz.html")
@app.route("/leader_board")
def learder_board():
   return render_template("leader_board.html")



if __name__ == '__main__':
    app.run(debug=True)