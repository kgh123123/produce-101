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
            "number"	INTEGER,
            "name"	TEXT,
            "count"	INTEGER,
            "is_manager"	INTEGER,
            "is_already_vote"	INTEGER,
            "reason"	TEXT
        );
    ''')
    conn.commit()
    conn.close()

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
    cursor.execute('SELECT number, name FROM users')    #투표될 유저들 불러오기
    candidates=[str(row[0])+" "+row[1] for row in cursor.fetchall()]
    return render_template("vote.html", name=name,candidates=candidates)

@app.route('/POST_vote', methods=['POST'])
def POST_vote():
    number = request.form['number']

@app.route('/dashboard')
def dashboard():
    name = session.get('name', "로그인되지 않음")
    return render_template("dashboard.html", name=name)

@app.route('/POST_login', methods=['POST'])
def POST_login():
    number = int(request.form['number'])
    name = request.form['name']
    if check_user(number,name): #학번과 이름이 일치하지 않아도 로그인되는 버그 수정
        session['name'] = name
        return redirect('/')
    else:
        raise Exception("동아리 인원 외의 유저가 로그인을 시도하였습니다.")

#유저가 동아리 회원인지 확인하는 함수  
def check_user(number:int,name:str):
    cursor.execute('SELECT number FROM users')
    numbers = [row[0] for row in cursor.fetchall()]
    if number in numbers:
        cursor.execute(f'SELECT name FROM users WHERE number = {number}')
        names = [row[0] for row in cursor.fetchall()]
        return True if name in names else False
    return False

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('name', None)
    return redirect('/')

if __name__ == '__main__':
    #init_db()
    app.run(debug=True, host='0.0.0.0')
