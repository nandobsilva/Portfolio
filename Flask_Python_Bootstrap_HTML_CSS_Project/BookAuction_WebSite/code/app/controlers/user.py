from flask import Blueprint, render_template, request, session, redirect, abort, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, SignUpForm
from app.models.user import User
from flask_login import logout_user, login_user, current_user
from app.functions import getTop5

user_blueprint = Blueprint('user', __name__, url_prefix='/user')


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # Error messages
    top5 = getTop5()
    message_01 = 'Invalid email or password.'
    message_02 = 'Please log in to access this page.'
    # Variables
    form = LoginForm()
    next = request.args.get('next')

    if form.validate_on_submit():
        email = request.values.get('email')
        password = request.values.get('password')
        user = User.login(email, password)
        # If password is incorrect or user does not exist in the database.
        if user == 0:
            return render_template('user/login.html', form=form, message=message_01, top5=top5)
        # Correct email and password
        else:
            session['book_id'] = None
            login_user(user)
            next = session['next']
            if next is None:
                return redirect(url_for('home.home'))
            else:
                session['next'] = None
                return redirect(next)
    else:
        if next is None:
            session['next'] = None
            return render_template('user/login.html', form=form, top5=top5)
        else:
            session['next'] = next
            return render_template('user/login.html', form=form, message=message_02, top5=top5)


@user_blueprint.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    top5 = getTop5()
    message_01 = 'User already exists'
    message_02 = 'User was successfully created. Click in the "Log in" button to access the page.'

    if form.validate_on_submit():
        name = request.values.get('name')
        email = request.values.get('email')
        password_hash = generate_password_hash(request.values.get('password'))
        phone = request.values.get('phone')
        address = request.values.get('address')
        user = User(name, email, password_hash, phone, address)

        # If email does not exists in the database
        if user.register() == 1:
            return render_template('user/sign_up.html', form=form, message=message_02, top5=top5)
        # If email already exists in the database
        else:
            return render_template('user/sign_up.html', form=form, message=message_01, top5=top5)
    else:
        return render_template('user/sign_up.html', form=form, message="", top5=top5)


@user_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('home.index'))
