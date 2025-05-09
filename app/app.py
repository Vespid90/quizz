from flask import Flask, request, render_template, redirect, url_for
from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods =['GET', 'POST'])
def register():
    if request.method == "POST":
        lastname = request.form.get('last_name')
        firstname = request.form.get('first_name')
        email = request.form.get('email')
        password = request.form.get('password')
        pw_hash = bcrypt.generate_password_hash(password)

        # save lastname, firstname, email and pw_hash in DB

        return redirect(url_for('index'))
    return render_template('sign_up.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password_candidate = request.form.get('password')

        pw_hash = 'placeholder' # load password_hash from DB

        if bcrypt.check_password_hash(pw_hash, password_candidate):
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))  #Password incorrect. Try again
    return render_template('login.html')


if  __name__ == '__main__':
    app.run(debug=True)