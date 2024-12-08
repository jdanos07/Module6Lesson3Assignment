# Task 1
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:J!strM3str@localhost/gym_db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

@app.route('/')
def home():
    return "Fitness Center Database"

class Members(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.String(2), nullable=False)
    workouts = db.relationship('Workouts', backref='members')

class Workouts(db.Model):
    __tablename___ = 'workoutsessions'
    workout_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    date = db.Column(db.String(11), nullable=False)
    duration_minutes = db.Column(db.String(5), nullable=False)
    calories_burned = db.Column(db.String(5), nullable=False)

with app.app_context():
    db.create_all()
if __name__ == '__main__':
    app.run(debug=True)