from flask import Flask
from werkzeug.security import generate_password_hash
import model

app = Flask(__name__)

model.connect_to_db(app)

with app.app_context():
    model.db.create_all()

    new_user_1 = model.User(email="jondoe@test.com", password=generate_password_hash("test"))
    new_user_2 = model.User(email="janedoe@test.com", password=generate_password_hash("test"))

    model.db.session.add_all([new_user_1, new_user_2])
    model.db.session.commit()
    print("Successfully added test users")

    new_task = model.Task(
        name="Create Prints",
        company="Maverick",
        due_date="2023-08-16", 
        due_time="03:30 PM",    
        notes="Print store sign",
        user_id=1
    )
    model.db.session.add(new_task)
    model.db.session.commit()
    print("Successfully added test task")
