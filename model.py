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
    due_time = db.Column(db.Time)
    notes = db.Column(db.String(255))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, name, company, due_date, due_time, notes, user_id):
        self.name = name
        self.company = company
        self.due_date = due_date
        self.due_time = due_time
        self.notes = notes
        self.user_id = user_id

def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app # type: ignore
    db.init_app(app)

if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to db...")