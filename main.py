from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html',name="유저")

@app.route('/login')
def login():
    return render_template('index.html')

@app.route('/dashborad')
def dashborad():
    return render_template('index.html',name="유저")

if __name__ == '__main__':
    app.run(debug=True)