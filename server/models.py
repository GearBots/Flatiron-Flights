from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from datetime import datetime
db = SQLAlchemy()


class Flight(db.Model, SerializerMixin):
  __tablename__ = 'flights'
  id = db.Column(db.Integer, primary_key=True)
  db.Column('id', db.Integer, primary_key=True),
  db.Column('flight_number', db.String(100), unique=True, nullable=False),
  db.Column('origin', db.String(100), nullable=False),
  db.Column('destination', db.String(100), nullable=False),
  db.Column('departure_time', db.DateTime, nullable=False)
  
class itinerary(db.Model, SerializerMixin):
  __tablename__ = 'itineraries'
  db.Column('id', db.Integer, primary_key=True),
  db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
  db.Column('details', db.String(255), nullable=True),
  db.Column('created_at', db.DateTime, default=datetime())
  
class User(db.Model, SerializerMixin):
  __tablename__ = 'users'
  db.Column()