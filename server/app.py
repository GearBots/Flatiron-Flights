from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from flask_migrate import Migrate
from extensions import db  # Import db from extensions.py
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
import logging
# Ensure models are imported after db to avoid uninitialized db usage
from models import Flight, Itinerary, User

load_dotenv()  # Load environment variables from .env file
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

bcrypt = Bcrypt(app)
db.init_app(app)
migrate = Migrate(app, db)

CORS(app)

logging.basicConfig(level=logging.DEBUG)

@app.route('/flights', methods=['GET'])
def get_flights():
    flights = Flight.query.all()
    return jsonify([flight.serialize() for flight in flights])


@app.route('/flights', methods=['POST'])
def create_flight():
    data = request.get_json()
    flight = Flight(**data)
    db.session.add(flight)
    db.session.commit()
    return jsonify(flight.serialize()), 201


@app.route('/flights/<int:id>', methods=['GET'])
def get_flight(id):
    flight = Flight.query.get_or_404(id)
    return jsonify(flight.serialize())


@app.route('/flights/<int:id>', methods=['PUT'])
def update_flight(id):
    flight = Flight.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(flight, key, value)
    db.session.commit()
    return jsonify(flight.serialize())


@app.route('/flights/<int:id>', methods=['DELETE'])
def delete_flight(id):
    flight = Flight.query.get_or_404(id)
    db.session.delete(flight)
    db.session.commit()
    return jsonify({}), 204


@app.route('/itineraries', methods=['GET'])
def get_itineraries():
    itineraries = Itinerary.query.all()
    return jsonify([itinerary.serialize() for itinerary in itineraries])


@app.route('/itineraries', methods=['POST'])
def create_itinerary():
    data = request.get_json()
    itinerary = Itinerary(**data)
    db.session.add(itinerary)
    db.session.commit()
    return jsonify(itinerary.serialize()), 201


@app.route('/itineraries/<int:id>', methods=['GET'])
def get_itinerary(id):
    itinerary = Itinerary.query.get_or_404(id)
    return jsonify(itinerary.serialize())


@app.route('/itineraries/<int:id>', methods=['PUT'])
def update_itinerary(id):
    itinerary = Itinerary.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(itinerary, key, value)
    db.session.commit()
    return jsonify(itinerary.serialize())


@app.route('/itineraries/<int:id>', methods=['DELETE'])
def delete_itinerary(id):
    itinerary = Itinerary.query.get_or_404(id)
    db.session.delete(itinerary)
    db.session.commit()
    return jsonify({}), 204


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users])


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if 'username' not in data or 'password' not in data:
        abort(400, description="Missing username or password")
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    data['password'] = hashed_password
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 201


@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.serialize())


@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return jsonify(user.serialize())


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({}), 204


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


if __name__ == "__main__":
    app.run(debug=True)