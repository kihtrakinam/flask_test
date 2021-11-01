## Webpage
from flask import Flask
from flask import render_template, request, redirect
## Web Forms
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
## SQL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
import pymysql
import secret
import urllib.parse as ups

dbpass,dbuser,dbhost,dbname = ups.quote_plus(secret.dbpass),secret.dbuser,secret.dbhost,secret.dbname
conn = "mysql+pymysql://{}:{}@{}/{}".format(dbuser,dbpass,dbhost,dbname)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
db = SQLAlchemy(app)

class participants(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(50))
    #check_age, check_gender = 'age>18', 'gender in ('M','F')'
    #CheckConstraint("gender in ('M','F')",name='check_gender'), CheckConstraint("age>18",name='check_age')
    age = db.Column(db.Integer,nullable=False)
    gender = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return "id : {} | first_name : {1} | last name : {2} | age : {3} | gender : {4}".format(self.id,self.first_name,self.last_name,self.age,self.gender)

class ParticipantsForm(FlaskForm):
    first_name = StringField('First Name :',validators=[DataRequired()])
    last_name = StringField('Last Name :')
    age = StringField('Age :',validators=[DataRequired()])
    gender = StringField('Gender :',validators=[DataRequired()])

@app.route('/')
def index():
    return render_template('homepage.html',pageTitle='Flask server Home Page')

@app.route('/Author')
def author():
    return render_template('author.html',pageTitle='About Author')

@app.route('/Calculator')
def Calculator():
    return render_template('calc.html',display="",pageTitle='My Calculator')

@app.route('/add',methods=['GET','POST'])
def add():
    if request.method == 'POST':
        form = request.form
        try:
            numberOne = int(form['numOne'])
            numberTwo = int(form['numTwo'])
            calc = numberOne + numberTwo
            return render_template('calc.html',display=calc,pageTitle='My Calculator')
        except:
            return render_template('calc.html',display="Invalid entry",pageTitle='My Calculator')
    return redirect("/Calculator")

@app.route('/add_participant',methods=['GET','POST'])
def add_participant():
    form = ParticipantsForm()
    if form.validate_on_submit():
        first_name,last_name,age,gender = form.first_name.data,form.last_name.data,int(form.age.data),form.gender.data
        name = first_name+' '+last_name
        participant = participants(first_name=first_name,last_name=last_name,age=age,gender=gender)
        db.session.add(participant)
        db.session.commit()
        return render_template('add_participant.html',form=form,Name=name,Age=age,Gender=gender,pageTitle='Add a participant')
    return render_template('add_participant.html',form=form,Name="",Age="",Gender="",pageTitle='Add a participant')

@app.route('/all_participants')
def all_participants():
    all_part = participants.query.all()
    return render_template('all_participants.html',details=all_part,pageTitle='Flask server Home Page')

if __name__ == '__main__':
    app.run(debug=True)
