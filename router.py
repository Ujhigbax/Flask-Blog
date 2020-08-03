from flask import Flask, render_template, redirect, url_for, request, flash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from forms import LoginForm, RegisterForm, MessageForm
from flask_login import LoginManager, login_user, login_required, logout_user,current_user
app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)

login_manager=LoginManager()
login_manager.init_app(app)

from models import *

login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id==int(user_id)).first()

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('blogposts')
    login_form=LoginForm(request.form)
    if login_form.validate_on_submit():
        user=User.query.filter_by(username=request.form['username']).first()
        if user is not None:
            if bcrypt.check_password_hash(user.password,request.form['password']):
                login_user(user)
                flash('You were just logged in!')
                return redirect(url_for('blogposts'))
            else:
                flash('Incorrect Password.')
        else:
            flash('User Not Found.')
    return render_template('login.html', form=login_form)

@app.route('/register',methods=['GET','POST'])
def register():
    register_form=RegisterForm()
    if register_form.validate_on_submit():
        entered_username=User.query.filter_by(username=register_form.username.data).first()
        entered_email=User.query.filter_by(email=register_form.email.data).first()
        if entered_username is not None:
            flash('Username is already taken. Choose another username.')
            return render_template('register.html',form=register_form)
        if entered_email is not None:
            flash('Email is already used for an existing account. Choose another email.')
            return render_template('register.html',form=register_form)
        new_user=User(username=register_form.username.data,email=register_form.email.data,password=register_form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Account Registered.')
        flash('Please Login.')
        return redirect(url_for('login'))
    return render_template('register.html',form=register_form)

@app.route('/blogposts',methods=['GET','POST'])
@login_required
def blogposts():
    message_form=MessageForm()
    print(message_form)
    print(message_form.title.data)
    print(message_form.description.data)
    print(message_form.validate_on_submit())
    if message_form.validate_on_submit():
        print('Validated')
        new_message= BlogPost(message_form.title.data,message_form.description.data,current_user.id)
        db.session.add(new_message)
        db.session.commit()
        flash('New entry was successfully posted.Thanks!')
        return redirect(url_for('blogposts'))
    else:
        print('Not Submitted')
        posts=db.session.query(BlogPost).all()
        return render_template('blogposts.html',posts=posts,form=message_form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were just logged out!')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)