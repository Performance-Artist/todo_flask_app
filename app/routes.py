from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Todo
from app.forms import LoginForm, RegisterForm, TodoForm
from flask import current_app as app

@app.route('/')
@login_required
def index():
    form = TodoForm()
    todos = Todo.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', todos=todos, form=form)

@app.route('/add', methods=['POST'])
@login_required
def add():
    form = TodoForm()
    if form.validate_on_submit():
        todo = Todo(text=form.text.data, user=current_user)
        db.session.add(todo)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/toggle/<int:todo_id>')
@login_required
def toggle(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if todo.user_id == current_user.id:
        todo.done = not todo.done
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
@login_required
def delete(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if todo.user_id == current_user.id:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Неправильное имя пользователя или пароль')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация успешна!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
