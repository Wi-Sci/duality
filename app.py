from flask import Flask, render_template, redirect, url_for, request, make_response, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import bcrypt, uuid, json, random, time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Misc(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    value = db.Column(db.String())

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '<id %r>' % self.id


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    sensor_id = db.Column(db.Integer)
    time = db.Column(db.Integer)
    value = db.Column(db.Integer)

    def __init__(self, sensor_id, time, value):
        self.sensor_id = sensor_id
        self.time = time
        self.value = value

    def __repr__(self):
        return '<data %r>' % self.id


@app.route('/')
def index():
    return render_template('client.html')


@app.route('/add', methods=['POST'])
def add_message():
    content = request.get_json(silent=True)
    last_entry = Data.query.filter(Data.sensor_id == content["ID"]["sensor_id"]).order_by(Data.id.desc()).first()
    db.session.add(Data(content["ID"]["sensor_id"], last_entry.time + 1, content["Payload"]))
    db.session.commit()
    return "meow"


@app.route('/jsondata/<sensor_id>')
def json_data(sensor_id):
    arrays = []
    for r in Data.query.filter(Data.sensor_id == sensor_id).all():
        arrays.append([r.time, r.value])
    response = {
        "label": "Distance Sensor 1",
        "data": arrays
    }
    return jsonify(**response)


@app.route('/differentSensors')
def different_sensors():
    query = db.session.query(Data.sensor_id.distinct().label("sensor_id"))
    sensors = [row.sensor_id for row in query.all()]
    response = {

    }
    for sensor_id in sensors:
        response[str(sensor_id)] = sensor_id
    return jsonify(**response)


app.run(debug=True, host='0.0.0.0', port=8000)