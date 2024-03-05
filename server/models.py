from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates, relationship
from extensions import db

class Flight(db.Model, SerializerMixin):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(100), unique=True, nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    # Removed users relationship

    @validates('flight_number', 'origin', 'destination', 'departure_time')
    def validate_flight(self, key, value):
        if not value:
            raise ValueError(f"Flight must have a {key}.")
        return value

class Itinerary(db.Model, SerializerMixin):
    __tablename__ = 'itineraries'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), nullable=False)  # Ensure this column exists
    details = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = relationship('User', back_populates='itineraries')
    flight = relationship('Flight')  # Add this relationship

    @validates('user_id', 'created_at')
    def validate_itinerary(self, key, value):
        if not value:
            raise ValueError(f"Itinerary must have a {key}.")
        return value

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Ensure adequate length for hashed passwords
    itineraries = relationship('Itinerary', back_populates='user')
