#!/usr/local/bin/python3

from flask import Flask, render_template, request, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from yelp import find_coffee
from flask_login import current_user, login_user, login_required, logout_user
from models import db, login, UserModel


class loginForm(FlaskForm):
    username = StringField(label='User Name',validators=[DataRequired(), Length(min=4,max=16)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password',validators=[DataRequired(), Length(min=4,max=16)])
    submit = SubmitField(label='Login')

class registerForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired(), Length(min=4, max=16)])
    email = StringField(label='Email',validators=[DataRequired(), Email()])
    password = PasswordField(label='Password',validators=[DataRequired(), Length(min=4,max=16)])
    submit = SubmitField(label='Register')

app=Flask(__name__)
app.secret_key='a secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login.init_app(app)
login.login_view = 'login'

@app.before_first_request
def create_table():
    db.create_all()
    

@app.route('/')
def baseSite():
    return redirect("/login")

@app.route('/home')
def homepage():
    return render_template('home.html')
    
@app.route('/coffeeshops')
@login_required
def coffee():
    return render_template('coffeeshop.html',mydata=find_coffee())

@app.route('/about')
def about():
    return render_template('about.html')
            
@app.route('/login',methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect('/coffeeshops')
    form=loginForm()
    if form.validate_on_submit():
        if request.method == "POST":
            username=request.form["username"]
            pw=request.form["password"]
            user = UserModel.query.filter_by(username = username).first()
            if user is None:
                flash('You are not registered. Please register by clicking the link: Click to Register!')
                return redirect(url_for('login'))

            if user is not None and user.check_password(pw):
                login_user(user)
                return redirect('/coffeeshops')
            else:
                flash('Login not successful. User and password does not match. Re-enter')
                return render_template('login.html',form=form)
        else:
            return render_template('login.html',form=form)
    else:
        return render_template('login.html',form=form)


@app.route('/register',methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect('/coffeeshops')
    form=registerForm()
    if form.validate_on_submit():
        if request.method == "POST":
            username = request.form["username"]
            email=request.form["email"]
            pw=request.form["password"]
            user = UserModel.query.filter_by(email = email).first()
            if user is not None:
                flash('You are already registered. Proceed to login')
                return redirect(url_for('login'))

            if user is not None and user.check_password(pw):
                # login_user(user)
                # return redirect('/coffeeshops')
                return redirect('/login')
            else:
                user = UserModel(email=email)
                user.set_password(pw)
                user.email = email
                user.username = username
                db.session.add(user)
                db.session.commit()
                flash('Congratulations, You are now a registered user! Please login')
                return redirect(url_for('login'))
             #   return render_template('login.html',form=form)
        else:
            return render_template('login.html',form=form)
    else:
        return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/home')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
