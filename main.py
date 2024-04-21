from flask import Flask, session,render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('user.db')
cursor = conn.cursor()

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
    userid = session.get('userid', None)
    return render_template("index.html",name=userid)

@app.route('/login', methods=['GET','POST'])  
def login():
    session['userid'] = 'userid' #form에서 가져온 userid를 session에 저장
    return redirect('/') #로그인에 성공하면 홈화면으로 redirect     
    #return render_template('login.html', form=form)


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
    init_db()  # 데이터베이스 초기화
    app.run(debug=True)