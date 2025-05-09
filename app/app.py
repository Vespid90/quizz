from flask import Flask, request, render_template, redirect, url_for
from flask_bcrypt import Bcrypt
from config import *

temp = ''

app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign_up', methods =['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        last_name = request.form.get('last_name')
        first_name = request.form.get('first_name')
        email = request.form.get('email')
        password = request.form.get('password')
        pw_hash = bcrypt.generate_password_hash(password)

        db = Config.get_connection()
        cur = db.cursor()
        cur.execute(""" INSERT INTO users(first_name, last_name, email, password)
                               VALUES (%s, %s, %s, %s);
                                """, (first_name, last_name, email, pw_hash))
        cur.close()
        db.close()

        return redirect(url_for('index'))
    return render_template('sign_up.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password_candidate = request.form.get('password')

        db = Config.get_connection()
        cur = db.cursor()
        SQL = "SELECT password FROM users WHERE email = %s"
        data = (email,)
        cur.execute(SQL, data)
        pw_hash = cur.fetchone()[0]
        cur.close()
        db.close()

        if bcrypt.check_password_hash(pw_hash, password_candidate):
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')


if  __name__ == '__main__':
    app.run(debug=True)


