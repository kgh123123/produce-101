from flask import Flask, session, render_template, request, redirect
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('user.db', check_same_thread=False)
cursor = conn.cursor()
app.secret_key = 'LN$oaYB9-5KBT7G'

#SQLite 데이터베이스 초기화
def init_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT NOT NULL,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    name = session.get('name', "로그인되지 않음")
    return render_template("index.html", name=name, is_already_login='disabled' if name != "로그인되지 않음" else '')

@app.route('/login')
def login():
    name = session.get('name', "로그인되지 않음")
    return render_template("login.html", name=name, is_already_login='disabled' if name == "로그인되지 않음" else '')

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
    #try:
    number = request.form['number']
    name = request.form['name']
    cursor.execute('SELECT number, name FROM users')
    rows = cursor.fetchall()
    numbers = [row[0] for row in rows]
    names = [row[1] for row in rows]
    print(numbers)
    print(names)
    if name in names and number in numbers:
        session['name'] = name
        session.pop('login_error', None)
        return redirect('/')
    else:
        raise Exception("동아리 인원 외의 유저가 로그인을 시도하였습니다.")

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('name', None)
    return redirect('/')

if __name__ == '__main__':
    #init_db()  # 데이터베이스 초기화
    app.run(debug=True)
