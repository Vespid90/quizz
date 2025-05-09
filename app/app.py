from flask import Flask, request, render_template, redirect, url_for
from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return ''

@app.route('/register', methods =['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        pw_hash = bcrypt.generate_password_hash(password)
        # save username, email and pw_hash in DB
        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password_candidate = request.form.get('password')
        pw_hash = 'placeholder' # load password_hash from DB
        bcrypt.check_password_hash(pw_hash, password_candidate)
        if True:
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')


if  __name__ == '__main__':
    app.run(debug=True)