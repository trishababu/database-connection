# app.py (Flask application)
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:Exuvz9v0mhFF1mnQsEtMQ4OmQ0ehEtaP@dpg-civsou15rnuqala0jlb0-a.oregon-postgres.render.com/saline'
db = SQLAlchemy(app)

# Models for the "device" and "variable" tables (same as before)
class Device(db.Model):
    DEVICEID = db.Column(db.Integer, primary_key=True)
    DEVICENAME = db.Column(db.String(50), nullable=False)
    DESCRIPTION = db.Column(db.String(200), nullable=True)

class Variable(db.Model):
    DEVICEID = db.Column(db.Integer, primary_key=True)
    DPM = db.Column(db.String(50), nullable=True)
    BATTERY = db.Column(db.String(50), nullable=True)
    CONSUMEDCAPACITY = db.Column(db.Float, nullable=True)
    REMAININGCAPACITY = db.Column(db.Float, nullable=True)
    TEMPERATURE = db.Column(db.Float, nullable=True)
    HUMIDITY = db.Column(db.Float, nullable=True)

# Create the necessary Flask routes
@app.route('/device/<int:device_id>', methods=['GET'])
def get_device_variables(device_id):
    variables = Variable.query.filter_by(DEVICEID=device_id).first()
    
    if variables is not None:
        response = {
            'DPM': variables.DPM,
            'BATTERY': variables.BATTERY,
            'CONSUMEDCAPACITY': variables.CONSUMEDCAPACITY,
            'REMAININGCAPACITY': variables.REMAININGCAPACITY,
            'TEMPERATURE': variables.TEMPERATURE,
            'HUMIDITY': variables.HUMIDITY
        }
        return jsonify(response)
    else:
        return jsonify({'error': 'Device ID not found'}), 404
@app.route('/variable', methods=['POST'])
def add_variable():
    data = request.get_json()
    name = data.get('name')
    unit = data.get('var')
    description = data.get('desc')

    if not name or not unit or not description:
        return jsonify({'error': 'All fields are required.'}), 400

    variable = Variable(name=name, unit=unit, description=description)

    try:
        db.session.add(variable)
        db.session.commit()
        return jsonify({'message': 'Variable added successfully.'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while adding the variable.'}), 500


if __name__ == '__main__':
    app.run(debug=True)
