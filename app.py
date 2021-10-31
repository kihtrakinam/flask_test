from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "hello world"

@app.route('/mani')
def mani():
    return "hello Mani!! Congratualtions on the first flask test."

if __name__ == '__main__':
    app.run(debug=True)
