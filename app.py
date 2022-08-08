
import email
from enum import unique
from turtle import title
from flask import Flask, redirect,render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#create a flask instance
app=Flask(__name__)
# Add database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Intialize the database
db=SQLAlchemy(app)
#create model
class Users(db.Model):#inheritaning
    sno=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(200), nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    phoneno=db.Column(db.Integer,nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)
def __repr__(self) -> str:
    return f"{self.sno} - {self.username}"

@app.route('/index.html')
def hello_world():
    return render_template('index.html')

@app.route('/',methods=['GET','POST'])
def contact():
    if request.method== 'POST':
        username=request.form['username']
        email=request.form['email']
        phoneno=request.form['phoneno']
        users=Users(username=username,email=email,phoneno=phoneno)
        db.session.add(users)
        db.session.commit()
    allusers=Users.query.all()
    print(allusers)
    return render_template('contact.html',allusers=allusers)

@app.route('/delete/<int:sno>')
def delete(sno):
    delusers=Users.query.filter_by(sno=sno).first()
    db.session.delete(delusers)
    db.session.commit()
    return redirect('/')


@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        phoneno=request.form['phoneno']
        users=Users.query.filter_by(sno=sno).first()
        users.username=username
        users.email=email 
        users.phoneno=phoneno
        db.session.add(users)
        db.session.commit()
        return redirect("/")
    users=Users.query.filter_by(sno=sno).first()
    return render_template('update.html',users=users)

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/products')
def products():
    return "This is produts page"


if __name__=="__main__":
    app.run(debug=True,port=5000)