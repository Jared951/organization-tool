from flask import Flask, render_template, request, redirect, url_for
from model import User, Task, db, connect_to_db
from datetime import datetime

app = Flask(__name__)
connect_to_db(app)

@app.route('/')
def home():
    user_id = 1  # Replace with the logged-in user's ID
    user = User.query.get(user_id)
    tasks = user.tasks
    return render_template('home.html', tasks=tasks)

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        # Get data from the form
        name = request.form['name']
        company = request.form['company']
        due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d')
        due_time = datetime.strptime(request.form['due_time'], '%H:%M').time()
        notes = request.form['notes']

        # Create a new Task object and add it to the database
        user_id = 1  # Replace with the logged-in user's ID
        new_task = Task(name=name, company=company, due_date=due_date, due_time=due_time, notes=notes, user_id=user_id)
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('create_event.html')

@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
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
def delete_event(event_id):
    task = Task.query.get(event_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))

if __name__=="__main__":
    app.run(debug=True)