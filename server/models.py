from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from datetime import datetime
db = SQLAlchemy()


class Flight(db.Model, SerializerMixin):
  __tablename__ = 'flights'
  id = db.Column(db.Integer, primary_key=True)
  flight_number = db.Column('flight_number', db.String(100), unique=True, nullable=False),
  origin = db.Column('origin', db.String(100), nullable=False),
  destination = db.Column('destination', db.String(100), nullable=False),
  departure_time = db.Column('departure_time', db.DateTime, nullable=False)
  
class itinerary(db.Model, SerializerMixin):
  __tablename__ = 'itineraries'
  id = db.Column('id', db.Integer, primary_key=True),
  user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
  details = db.Column('details', db.String(255), nullable=True),
  created_time = db.Column('created_at', db.DateTime, default=datetime())
  
class User(db.Model, SerializerMixin):
  __tablename__ = 'users'
  id = db.Column('id', db.Integer, primary_key=True),
  itinerary_id = db.Column('itinerary_id', db.Integer, db.ForeignKey('itinerary.id'), nullable=False),
  username = db.Column('username', db.String(50), nullable=False),
  password = db.Column('password', db.String(50), nullable=False),
  