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
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
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

@app.route('/get_events')
def get_events():
    if not current_user.is_authenticated:
        return jsonify([])

    user_id = current_user.id
    events = Task.query.filter_by(user_id=user_id).all()

    event_list = []
    for event in events:
        event_list.append({
            'title': event.name,
            'start': datetime.combine(event.due_date, event.due_time).isoformat(),
            'extendedProps': {
                'company': event.company,
                'notes': event.notes
            }
        })
    return jsonify(event_list)

if __name__ == "__main__":
    app.run(debug=True)