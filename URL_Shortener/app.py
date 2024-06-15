#!/usr/bin/python3
""" Url shortener app """
from flask import Flask, request, render_template, url_for, redirect, session, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Url, Visit
from uuid import uuid4
import bcrypt
import string
import random


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'

engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

orm_session = Session()


@app.route('/', methods=['GET', 'POST'], strict_slashes=False)
def index():
    if 'username' in session:
        username = session.get('username')

        user = orm_session.query(User).filter(User.username==username).first()

        if request.method == 'POST':
            url = request.form.get('url')

            characters = string.ascii_letters + string.digits
            short_url = ''.join(random.choice(characters) for _ in range(6))
            short_url = request.root_url + short_url
            user_url = Url(url=url, short_url=short_url)

            user.urls.append(user_url)
            orm_session.add(user)
            orm_session.commit()
            orm_session.close()
            return redirect(url_for('index'))

        urls = user.urls
        return render_template('index.html', urls=urls)
    else:
        return redirect(url_for('login'))

@app.route('/<short_url>')
def redirect_url(short_url):
    url = orm_session.query(Url).filter(Url.short_url==request.url).first()
    if url:
        visit = Visit(ip_address=request.remote_addr)

        url.visits.append(visit)
        orm_session.add(url)
        orm_session.commit()
        return redirect(url.url)
    else:
        return 'Not found', 404


@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = orm_session.query(User).filter(User.username==username).first()
        orm_session.close()
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user.password):
                session['username'] = user.username

                flash('You were successfully logged in')
                return redirect(url_for('index'))
        return render_template('login.html', error='Incorrect username or password')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)

    flash('Logged out successfully')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')

        if password == confirm:
            user = orm_session.query(User).filter(User.username==username).first()
            if user:
                flash('User already exist')
                return redirect(url_for('login'))
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user = User(id=str(uuid4()), username=username, email=email, password=hashed_password)
            orm_session.add(user)
            orm_session.commit()
            orm_session.close()
            session['username'] = username

            flash('Registered successfully')
            return redirect(url_for('index'))
        return render_template('register.html', error='Passwords do not match')
    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session.get('username')
        user = orm_session.query(User).filter(User.username==username).first()
        urls = orm_session.query(Url).filter(Url.user_id==user.id).all()

        urls = urls
        return render_template('dashboard.html', urls=urls)
    return redirect(url_for('login'))


@app.route('/delete/<int:url_id>')
def delete(url_id):
    if 'username' in session:
        url = orm_session.query(Url).filter(Url.id==url_id).first()
        if url:
            orm_session.delete(url)
            orm_session.commit()

            flash('deleted successfully')
            return redirect(url_for('index'))
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
