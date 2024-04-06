from flask import Flask, render_template,request,jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html',name="유저")

# SQLite 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT NOT NULL,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 클라이언트로부터 전송된 정보를 데이터베이스에 저장하는 함수
def save_to_database(number,name):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (number,name) VALUES (?, ?)', (number,name))
    conn.commit()
    conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    number = data.get('number')
    name = data.get('name')
    save_to_database(number,name)
    # 데이터베이스에 저장
    return jsonify({'message': 'Data received and saved successfully!'})

if __name__ == '__main__':
    init_db()  # 데이터베이스 초기화
    app.run(debug=True)