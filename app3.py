# Task 3
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:J!strM3str@localhost/gym_db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class WorkoutSchema(ma.Schema):
    date = fields.String(required=True)
    duration_minutes = fields.String(required=True)
    calories_burned = fields.String(required=True)

    class Meta:
        fields = ('duration_minutes', 'date', 'member_id', 'workout_id', 'calories_burned')


workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

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

@app.route('/')
def home():
    return "Fitness Center Database"

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workouts.query.all()
    return workouts_schema.jsonify(workouts)

@app.route('/workouts', methods=['POST'])
def add_workout():
    try:
        workout_data = workout_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages),400

    new_workout = Workouts(
        calories_burned = workout_data['calories_burned'],
        duration_minutes = workout_data['duration_minutes'],
        date = workout_data['date']
        )
    db.session.add(new_workout)
    db.session.commit()
    return jsonify({'message': 'New member added successfuly'}), 201
 
@app.route ('/workouts/<int:id>/<int:id>', methods=['PUT'])
def update_workout(member_id, workout_id):
    workout = Workouts.query.get_or_404(member_id, workout_id)
    try:
        workout_data = workout_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages, 400)
    
    workout.calories_burned = workout_data['calories_burned']
    workout.duration_minutes = workout_data['duration_minutes']
    workout.date = workout_data['date']

    db.session.commit()
    return jsonify({'message': 'Workout upated'}), 200

@app.route('workouts/<init:id/<int:id>', methods=['DELETE'])
def delete_workout(member_id, workout_id):
    workout = Members.query.get_or_404(member_id, workout_id)
    db.session.delete(workout)
    db.session.commit()
    return jsonify({'message': 'Workout removed'}), 200