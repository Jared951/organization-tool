from flask import Flask, render_template, redirect, url_for, flash, current_app, request, jsonify
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from model import db, connect_to_db, User, Task
from forms import RegistrationForm, LoginForm
from datetime import datetime
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
connect_to_db(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login' #type: ignore

@login_manager.user_loader
def load_user(user_id): #type: ignore
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        new_user = User(email=email, password=password)  # Pass both email and password
        new_user.set_password(password)  # Set the hashed password using set_password method
        
        with current_app.app_context():
            db.session.add(new_user)
            db.session.commit()

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):  # Use check_password method
            flash('Logged in successfully!', 'success')
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')
    
    return render_template('login.html', form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    return render_template('home.html')

@app.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    task_name = request.form['task_name']
    company = request.form['company']
    due_date = request.form['due_date']
    due_time = request.form['due_time']
    notes = request.form['notes']

    # Create a Task object associated with the current user
    task = Task(name=task_name, company=company, due_date=due_date, due_time=due_time, notes=notes, user_id=current_user.id) 
        
    with app.app_context():
        db.session.add(task)
        db.session.commit()

        flash('Task added successfully!', 'success')
        return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)