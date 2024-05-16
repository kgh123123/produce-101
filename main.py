from flask import Flask, session, render_template, request, redirect, g
import sqlite3

app = Flask(__name__)
app.secret_key = 'LN$oaYB9-5KBT7G'
DATABASE = 'user.db'

# Database connection management
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Routes
@app.route('/')
def index():
    name = session.get('name', "로그인되지 않음")
    return render_template("index.html", name=name, is_already_login='disabled' if name != "로그인되지 않음" else '')

@app.route('/login')
def login():
    name = session.get('name', "로그인되지 않음")
    return render_template("login.html", name=name, is_login_error=str(int(session.get('login_error', 0))), is_already_login='disabled' if name == "로그인되지 않음" else '')

@app.route('/vote')
def vote():
    name = session.get('name', "로그인되지 않음")
    return render_template("vote.html", name=name)

@app.route('/dashboard')
def dashboard():
    name = session.get('name', "로그인되지 않음")
    return render_template("dashboard.html", name=name)

@app.route('/POST_login', methods=['POST'])
def POST_login():
    try:
        number = request.form['number']
        name = request.form['name']
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT number, name FROM users')
        rows = cursor.fetchall()
        numbers = [row[0] for row in rows]
        names = [row[1] for row in rows]
        if name in names and int(number) in numbers:
            session['name'] = name
            session.pop('login_error', None)
            return redirect('/')
        else:
            raise Exception("동아리 인원 외의 유저가 로그인을 시도하였습니다.")
    except:
        session['login_error'] = True
        return redirect('/login')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('name', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
