## Webpage
from flask import Flask
from flask import render_template, request, redirect, url_for
## Web Forms
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import DataRequired
## SQL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, or_
import pymysql
import secret
import urllib.parse as ups

dbpass,dbuser,dbhost,dbname = ups.quote_plus(secret.dbpass),secret.dbuser,secret.dbhost,secret.dbname
conn = "mysql+pymysql://{}:{}@{}/{}".format(dbuser,dbpass,dbhost,dbname)

app_loc = Flask(__name__)
app_loc.config['SECRET_KEY'] = 'SuperSecretKey'
app_loc.config['SQLALCHEMY_DATABASE_URI'] = conn
db = SQLAlchemy(app_loc)

class participants(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(50))
    #check_age, check_gender = 'age>18', 'gender in ('M','F')'
    #CheckConstraint("gender in ('M','F')",name='check_gender'), CheckConstraint("age>18",name='check_age')
    age = db.Column(db.Integer,nullable=False)
    gender = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return "id : {0} | first_name : {1} | last name : {2} | age : {3} | gender : {4}".format(self.id,self.first_name,self.last_name,self.age,self.gender)

class ParticipantsForm(FlaskForm):
    first_name = StringField('First Name :',validators=[DataRequired()])
    last_name = StringField('Last Name :')
    age = StringField('Age :',validators=[DataRequired()])
    gender = SelectField('Gender :',choices=[('M','Male'),('F','Female')],validators=[DataRequired()])

class SearchForm(FlaskForm):
    search_value = StringField('Search')

@app_loc.route('/search',methods=['GET','POST'])
def search():
    form_search = SearchForm()
    if request.method == 'GET':
        search_term= request.args.get('search_value')
        if search_term is not None:
            search = search_term.strip(' ')
            if search == '':
                secret.prev_search = None
                return redirect('/all_participants')
            else:
                search = "%{0}%".format(search)
                secret.prev_search = search
                results = participants.query.filter(or_(participants.first_name.like(search),participants.last_name.like(search))).all()
                return render_template('all_participants.html',form_search=form_search,details=results,pageTitle='Participants after search')
    #else:
    flag = secret.prev_search
    if flag is None:
        return redirect('/all_participants')
    else:
        results = participants.query.filter(or_(participants.first_name.like(flag),participants.last_name.like(flag))).all()
        return render_template('all_participants.html',form_search=form_search,details=results,pageTitle='Participants after removal')

@app_loc.route('/')
def index():
    return render_template('index.html',pageTitle='Flask server Home Page')

@app_loc.route('/Author')
def author():
    return render_template('author.html',pageTitle='About Author')

@app_loc.route('/Calculator')
def Calculator():
    return render_template('calc.html',display="",pageTitle='My Calculator')

@app_loc.route('/add',methods=['GET','POST'])
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

@app_loc.route('/add_participant',methods=['GET','POST'])
def add_participant():
    form_add = ParticipantsForm()
    if form_add.validate_on_submit():
        first_name,last_name,age,gender = form_add.first_name.data,form_add.last_name.data,int(form_add.age.data),form_add.gender.data
        name = first_name+' '+last_name
        participant = participants(first_name=first_name,last_name=last_name,age=age,gender=gender)
        db.session.add(participant)
        db.session.commit()
        return render_template('add_participant.html',form_add=form_add,Name=name,Age=age,Gender=gender,pageTitle='Add a participant')
    return render_template('add_participant.html',form_add=form_add,Name="",Age="",Gender="",pageTitle='Add a participant')

@app_loc.route('/all_participants',methods=['GET','POST'])
def all_participants():
    form_search = SearchForm()
    secret.prev_search = None
    all_part = participants.query.all()
    return render_template('all_participants.html',form_search=form_search,details=all_part,pageTitle='All Participants')

@app_loc.route('/remove_participant/<int:participant_id>',methods=['GET','POST'])
def remove_participant(participant_id):
    if request.method == 'POST':
        participant = participants.query.get_or_404(participant_id)
        db.session.delete(participant)
        db.session.commit()
        return redirect('/search')
    else:
        return redirect('/search')

@app_loc.route('/update_participant/<int:participant_id>',methods=['GET','POST'])
def update_participant(participant_id):
    participant = participants.query.get_or_404(participant_id)
    form_update = ParticipantsForm()
    if form_update.validate_on_submit():
        participant.first_name = form_update.first_name.data
        participant.last_name = form_update.last_name.data
        participant.age = form_update.age.data
        participant.gender = form_update.gender.data
        db.session.commit()
        return redirect('/search')
    else:
        form_update.first_name.data = participant.first_name
        form_update.last_name.data = participant.last_name
        form_update.age.data = participant.age
        form_update.gender.data = participant.gender
        return render_template('participant_details.html',details=participant,form_update=form_update,pageTitle='Participant Details')

if __name__ == '__main__':
    app_loc.run(debug=True)
