from flask import Flask, render_template, redirect, url_for, request, make_response, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import bcrypt, uuid, json, random

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
    time = db.Column(db.String())
    value = db.Column(db.String())

    def __init__(self, time, value):
        self.time = time
        self.value = value

    def __repr__(self):
        return '<data %r>' % self.id


def database_save_data(time, value):
    db.session.add(Data(time, value))
    db.session.commit()


@app.route('/')
def index():
    return render_template('client.html')


@app.route('/add/<time>/<int:value>')
def add(time, value):
    data = json.loads(Misc.query.filter(Misc.id == 1).first().value)
    data[str(time)] = value
    data = json.dumps(data)
    Misc.query.filter(Misc.id == 1).first().value = data
    db.session.commit()
    response = json.loads(Misc.query.filter(Misc.id == 1).first().value)
    return jsonify(**response)


@app.route('/add_value/<int:value>')
def add_value(value):
    data = json.loads(Misc.query.filter(Misc.id == 1).first().value)
    data[len(data) + 1] = value
    data = json.dumps(data)
    Misc.query.filter(Misc.id == 1).first().value = data
    db.session.commit()
    response = json.loads(Misc.query.filter(Misc.id == 1).first().value)
    return jsonify(**response)


@app.route('/jsondata')
def json_data():
    data = json.loads(Misc.query.filter(Misc.id == 1).first().value)
    arrays = []
    for key, value in data.items():
        arrays.append([int(key), value])
    response = {
        "label": "Duality Alpha",
        "data": arrays
    }
    return jsonify(**response)


@app.route('/wipe')
def wipe():
    data = {
        '1': 1
    }
    Misc.query.filter(Misc.id == 1).first().value = json.dumps(data)
    db.session.commit()
    return "wiped"


app.run(debug=True, host='0.0.0.0', port=8000)