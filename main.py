from flask import Flask, session, render_template, request, redirect
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('user.db', check_same_thread=False)
cursor = conn.cursor()
app.secret_key = 'LN$oaYB9-5KBT7G'

@app.route('/')
def index():
    name = session.get('name', "로그인되지 않음")
    return render_template("index.html", name=name)

@app.route('/login')
def login():
    name = session.get('name', "로그인되지 않음")
    return render_template("login.html", name=name)

@app.route('/vote')
def vote():
    name = session.get('name', "로그인되지 않음")
    return render_template("vote.html", name=name,candidates=["하나","둘"])

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
    if name in names and int(number) in numbers:
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
    app.run(debug=True)
