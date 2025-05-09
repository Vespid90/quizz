from flask import Flask, request, render_template, redirect, url_for
from flask_bcrypt import Bcrypt
from config import *
import random

num_questions = 5
selected_personages = []

app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign_up/', methods =['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        last_name = request.form.get('last_name')
        first_name = request.form.get('first_name')
        email = request.form.get('email')
        password = request.form.get('password')
        if password:
            pw_hash = bcrypt.generate_password_hash(password).decode('utf8')

            db = Config.get_connection()
            cur = db.cursor()
            cur.execute(""" INSERT INTO users(first_name, last_name, email, password)
                               VALUES (%s, %s, %s, %s);
                                """, (first_name, last_name, email, pw_hash))
            db.commit()
            cur.close()
            db.close()
            return redirect(url_for('index'))
        else:
            return redirect(url_for('sign_up'))
    return render_template('sign_up.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password_candidate = request.form.get('password')

        db = Config.get_connection()
        cur = db.cursor()
        sql = "SELECT password FROM users WHERE email = %s"
        data = (email,)
        cur.execute(sql, data)
        query_result = cur.fetchone()
        cur.close()
        db.close()
        if query_result:
            pw_hash = query_result[0]
            if bcrypt.check_password_hash(pw_hash, password_candidate):
                return redirect(url_for('quiz', question_number=1))
            else: # password incorrect
                return redirect(url_for('login'))
        else: # email not found in DB
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/quiz/<int:question_number>', methods=['GET', 'POST'])
def quiz(question_number):
    global selected_personages
    if question_number == 0:
        selected_personages = []

    personages_ids = []

    db = Config.get_connection()
    cur = db.cursor()
    cur.execute("SELECT id_person FROM person")
    query_result = cur.fetchall()

    for personage in query_result:
        personages_ids.append(personage[0])
    curr_personage_id = random.choice(personages_ids)
    while curr_personage_id in selected_personages:
        curr_personage_id = random.choice(personages_ids)
    selected_personages.append(curr_personage_id)

    sql = "SELECT * FROM person WHERE id_person = %s"
    data = (curr_personage_id,)
    cur.execute(sql, data)
    query_result = cur.fetchone()
    cur.close()
    db.close()

    #return str(curr_personage_id)
    #return query_result[1]
    return render_template('quiz_test.html', curr_personage_name = query_result[1], selected_personages=selected_personages)

if  __name__ == '__main__':
    app.run(debug=True)


