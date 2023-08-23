from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from model import User, Task, db, connect_to_db
from datetime import datetime
from forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
connect_to_db(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        hashed_password = generate_password_hash(password, method='sha256')
        
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()  

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    user = current_user
    tasks = user.tasks
    return render_template('home.html', tasks=tasks)

@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    if request.method == 'POST':
        # Get data from the form
        name = request.form['name']
        company = request.form['company']
        due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d')
        due_time = datetime.strptime(request.form['due_time'], '%H:%M').time()
        notes = request.form['notes']

        # Validate form data (add your validation logic here)
        if not name or not company or not due_date or not due_time:
            flash('Please fill in all required fields.', 'danger')
            return redirect(url_for('create_event'))

        try:
            # Create a new Task object and add it to the database
            user_id = current_user.id  # Use the logged-in user's ID
            new_task = Task(name=name, company=company, due_date=due_date, due_time=due_time, notes=notes, user_id=user_id)
            db.session.add(new_task)
            db.session.commit()
            flash('New task created successfully!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the task. Please try again later.', 'danger')
            print(f"Error: {e}")

    return render_template('create_event.html')


@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    task = Task.query.get(event_id)
    if request.method == 'POST':
        # Update event data based on form input
        task.name = request.form['name']
        task.company = request.form['company']
        task.due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d')
        task.due_time = datetime.strptime(request.form['due_time'], '%H:%M').time()
        task.notes = request.form['notes']
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('edit_event.html', task=task)

@app.route('/delete_event/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    task = Task.query.get(event_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)