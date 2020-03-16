from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from flask_qa.extensions import db
from flask_qa.models import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        unhashed_password = request.form['password']
        user = User(
            name=name,
            unhashed_password=unhashed_password,
            admin=False,
            expert=False
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        user = User.query.filter_by(name=name).first()
        error = None
        if not user or not check_password_hash(user.password, password):
            error = True
            flash("Lo siento mucho")
            return redirect(url_for('auth.login'))

        if not error:
            login_user(user)
            return redirect(url_for('main.index'))

    return render_template('login.html') 

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
