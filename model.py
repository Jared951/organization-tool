import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255))

    tasks = db.relationship("Task", backref="user", lazy=True)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def check_password(self, password):
        return self.password == password 

class Task(db.Model):

    __tablename__ = "task"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=False)
    due_date = db.Column(db.Date) 
    due_datetime = db.Column(db.DateTime)
    notes = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, name, company, due_date, due_datetime, notes):
        self.name = name
        self.company = company
        self.due_date = due_date
        self.due_datetime = due_datetime
        self.notes = notes

def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app # type: ignore
    db.init_app(app)

if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist yet
    
    print("Connected to db...")