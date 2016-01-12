from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from noozjunkie_webapp import app, db, lm, bcrypt
from .forms import LoginForm
from .models import User
import datetime

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        user = User.query.filter_by(username=form.username.data).first()
        print(user.get_id())
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                user.authenticated = True
                user.lastseen = datetime.datetime.utcnow()
                db.session.add(user)
                db.session.commit()
                remember_me = False
                if 'remember_me' in session:
                    remember_me = session['remember_me']
                    session.pop('remember_me', None)
                print(lm.id_attribute)
                login_user(user, remember = remember_me)
                return redirect(url_for("index"))
    form.password.data = ""
    return render_template("login.html", form=form)

@app.route('/logout', methods=["GET"])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template("index.html")

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    return User.query.get(id)
