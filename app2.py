# Task 2
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:J!strM3str@localhost/gym_db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    name = fields.Str(required=True)
    age = fields.Int(required=True)

    class Meta:
        fields = ('name', 'age', 'id')

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

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

@app.route('/members', methods=['GET'])
def get_members():
    members = Members.query.all()
    return members_schema.jsonify(members)

@app.route('/members', methods=['POST'])
def add_member():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages),400

    new_member = Members(
        name = member_data['name'],
        age = member_data['age']
        )
    db.session.add(new_member)
    db.session.commit()
    return jsonify({'message': 'New member added successfuly'}), 201
 
@app.route ('/members/<int:id>', methods=['PUT'])
def update_memeber(id):
    member = Members.query.get_or_404(id)
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages, 400)
    
    member.name = member_data['name']
    member.age = member_data['age']

    db.session.commit()
    return jsonify({'message': 'Member upated'}), 200

@app.route('members/<init:id', methods=['DELETE'])
def delete_member(id):
    member = Members.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    return jsonify({'message': 'Member removed'}), 200