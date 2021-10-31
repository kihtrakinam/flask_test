from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',pageTitle='Flask server Home Page')

@app.route('/Author')
def author():
    return render_template('author.html',pageTitle='About Author')

if __name__ == '__main__':
    app.run(debug=True)
