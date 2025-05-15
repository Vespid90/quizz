from flask import Flask, request, render_template, redirect, url_for, jsonify, session
from flask_bcrypt import Bcrypt
from config import *
import random

num_questions_per_series = 5

app = Flask(__name__)
app.secret_key = 'LaTeamGoat'
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

            db = ConnectQuizzDb.get_connection()
            cur = db.cursor()
            try:
                cur.execute(""" INSERT INTO users(first_name, last_name, email, password)
                                  VALUES (%s, %s, %s, %s);
                                  """, (first_name, last_name, email, pw_hash))
                db.commit()
            except:
                return redirect(url_for('sign_up')) #error by executing the sql-query

            try:
                sql = "SELECT id_users FROM users WHERE email = %s"
                data = (email,)
                cur.execute(sql, data)
                user_id = cur.fetchone()[0]
            except:
                print("error by selecting id_users (sql)")

            try:
                cur.execute(""" INSERT INTO ranking(id_users, score)
                                                  VALUES (%s, 0);
                                                  """, (user_id,))
            except:
                print("error by inserting into ranking (sql)")

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

        db = ConnectQuizzDb.get_connection()
        cur = db.cursor()
        sql = "SELECT password, id_users, first_name, last_name FROM users WHERE email = %s"
        data = (email,)
        cur.execute(sql, data)
        query_result = cur.fetchone()
        cur.close()
        db.close()
        if query_result:
            pw_hash = query_result[0]
            if bcrypt.check_password_hash(pw_hash, password_candidate):
                session["user_id"] = query_result[1]
                session["first_name"] = query_result[2]
                session["last_name"] = query_result[3]
                return redirect(url_for('quiz', question_number=1))
            else: # password incorrect
                return redirect(url_for('login'))
        else: # email not found in DB
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/quiz/<int:question_number>', methods=['GET', 'POST'])
def quiz(question_number):

    names = []
    # if first question in series -> clear list of already selected personages and set points=0
    if question_number == 1:
        session['selected_personages'] = []
        session['points'] = 0

    already_selected_personages = session.get('selected_personages')
    db = ConnectQuizzDb.get_connection()
    cur = db.cursor()
    cur.execute("SELECT id_person FROM person")
    query_result = cur.fetchall()
    personages_ids = list(map(lambda x : x[0], query_result))

    # randomly select one personage (but not among those who was already selected earlier in this series of questions)
    curr_personage_id = random.choice(list(set(personages_ids) - set(already_selected_personages)))
    # add the personage to the list of selected personages in this series
    already_selected_personages.append(curr_personage_id)
    session['selected_personages'] = already_selected_personages

    # randomly select two other personages for false answers
    personages_ids.remove(curr_personage_id)
    false_answers_ids = random.sample(personages_ids,2)

    # get information about the selected personages (name + images)
    sql = "SELECT name, image1, image2, image3 FROM person WHERE id_person = %s"
    data = (curr_personage_id,)
    cur.execute(sql, data)
    selected_personage_row = cur.fetchone()
    # name
    correct_answer = selected_personage_row[0]
    print('correct_answer from sql',correct_answer)  # for testing
    names.append(correct_answer)

    # randomly select one of 3 images
    image_link = random.choice(selected_personage_row[1:4])

    # get names for 2 false answers
    sql = "SELECT name FROM person WHERE id_person in (%s, %s)"
    data = (false_answers_ids[0], false_answers_ids[1])
    cur.execute(sql, data)
    for res_row in cur.fetchall():
        names.append(res_row[0])

    cur.close()
    db.close()

    # shuffle 3 answers
    random.shuffle(names)

    return render_template('quiz.html',
                           names=names,
                           image_link=image_link,
                           question_number=question_number,
                           correct_answer = correct_answer,
                           points = session.get('points')
                           )

@app.route('/submit',methods=['POST'])
def submit():
    user_answer = request.form.get('name')
    correct_answer = request.form.get('correct_answer')
    question_number  = int(request.form.get('question_number'))
    if user_answer and user_answer == correct_answer:
        session['points'] =  session.get('points') + 1
        print(f"You chose: {user_answer}, correct answer:{correct_answer}, you are right! New points: {session.get('points')}")
    elif user_answer:
        print(f"You chose: {user_answer}, correct answer:{correct_answer}, you are wrong...")
    else:
        print('Name not chosen')

    if question_number >= num_questions_per_series:
        print("Your final points: ", session.get('points'))
        # add points to the score in DB
        db = ConnectQuizzDb.get_connection()
        cur = db.cursor()
        try:
            sql = """UPDATE ranking
                        SET score = score + %s, updated_at = now()
                        WHERE id_users = %s 
                        """
            data = (session.get('points'), session.get('user_id'))
            cur.execute(sql, data)
            db.commit()
        except:
            print("Error by updating table ranking")
        cur.close()
        db.close()

        return jsonify({'redirect': url_for('end')})
    else:
        return jsonify({'redirect':url_for('quiz', question_number = question_number+1)})


@app.route("/leader_board")
def learder_board():
    classement = {}

    db = ConnectQuizzDb.get_connection()
    cur = db.cursor()
    sql = """SELECT r.score, u.first_name, u.last_name
                FROM ranking r JOIN users u ON r.id_users = u.id_users
                ORDER  BY r.score DESC
                """
    cur.execute(sql)
    query_res = cur.fetchall()
    for row in query_res:
        classement[' '.join([row[1], row[2]])] = row[0]
    cur.close()
    db.close()

    return render_template("leader_board.html",classement=classement)

@app.route("/end")
def end():
    return render_template("end.html", points=session.get('points'))
  
if  __name__ == '__main__':
  app.run(debug=True)

