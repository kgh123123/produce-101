from flask import Flask, session, render_template, request, redirect
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('user.db', isolation_level= None)
cursor = conn.cursor()
app.secret_key = 'LN$oaYB9-5KBT7G'

login_error:bool = False

#SQLite 데이터베이스 초기화
def init_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number INTEGER NOT NULL,
            name TEXT NOT NULL,
            count INTEGER NOT NULL,
            manager BOOLEAN NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    name:str = session.get('name', "로그인되지 않음")
    print(f"{name}님이 로그인 했습니다.")
    already_login:str = 'disabled' if name == "로그인되지 않음" else ' '
    return render_template("index.html",name=name, is_already_login=already_login)

@app.route('/login')
def login():
    name:str = session.get('name', "로그인되지 않음")
    already_login:str = 'disabled' if name == "로그인되지 않음" else ' '
    return render_template("login.html",name=name, is_login_error=str(int(login_error)), is_already_login=already_login)

@app.route('/vote')
def vote():
    name:str = session.get('name', "로그인되지 않음")
    return render_template("vote.html",name=name)

@app.route('/dashboard')
def dashboard():
    name:str = session.get('name', "로그인되지 않음")
    return render_template("dashboard.html",name=name)

@app.route('/POST_login', methods=['POST'])
def POST_login():
    global login_error
    try:
        name = request.form['name']  # 폼 데이터에서 'userid' 값을 가져옴
        cursor.execute('SELECT number, name FROM users')
        rows = cursor.fetchall()
        conn.close()
        #numbers = [row[0] for row in rows]
        names = [row[1] for row in rows]
        if name in names:
            session['name'] = name #form에서 가져온 userid를 session에 저장
            login_error = False
            return redirect('/') #로그인에 성공하면 홈화면으로 redirect
        else:
            raise Exception("동아리 인원 외의 유저가 로그인을 시도하였습니다.")
    except:
        login_error = True
        return redirect('/login') #로그인에 실패하면 로그인화면으로 redirect


#TODO:GPT의 힘을 빌린 투표코드(현재 따옴표로 주석처리), 로그인 기능 완성 후 연동
'''@app.route('/')
def index():
    # 모든 후보자 가져오기
    cursor.execute("SELECT * FROM votes")
    candidates = cursor.fetchall()
    return render_template('index.html', candidates=candidates)

@app.route('/vote', methods=['POST'])
def vote():
    candidate = request.form['candidate']
    
    # 후보자의 득표수 업데이트
    cursor.execute("UPDATE votes SET votes = votes + 1 WHERE candidate = ?", (candidate,))
    conn.commit()
    
    flash('투표가 성공적으로 기록되었습니다!', 'success')
    return redirect(url_for('index'))'''

if __name__ == '__main__':
    #init_db()  #데이터베이스를 초기화시키는 명령이니 되도록 주석을 풀지 말 것
    app.run(debug=True)