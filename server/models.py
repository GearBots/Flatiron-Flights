from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from datetime import datetime
from sqlalchemy import MetaData

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Flight(db.Model, SerializerMixin):
  __tablename__ = 'flights'
  id = db.Column(db.Integer, primary_key=True)
  flight_number = db.Column('flight_number', db.String(100), unique=True, nullable=False)
  origin = db.Column('origin', db.String(100), nullable=False)
  destination = db.Column('destination', db.String(100), nullable=False)
  departure_time = db.Column('departure_time', db.DateTime, nullable=False)
  
  users = db.relationship('User', back_populates='flights')
  
  serialize_rules = ('-users.flights',)
  
  @validates('flight_number','origin','destination','departure_time')
  def validates_flight(self,key,value):
    if not value:
      raise ValueError("Flight must have a flight_number, origin, destination, and departure_time.")
    return value
class Itinerary(db.Model, SerializerMixin):
  __tablename__ = 'itineraries'
  id = db.Column('id', db.Integer, primary_key=True)
  user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
  details = db.Column('details', db.String(255), nullable=True)
  created_time = db.Column('created_at', db.DateTime, default=datetime())
  
  users = db.relationship('User', back_populates='itineraries')
  
  serialize_rules = ('-users.itineraries',)
  
  @validates('user_id', 'created_time')
  def validates_Itinerary(self, key, value):
    if not value:
      raise ValueError("Itinerary must have a user id and a created time")
    return value
  
class User(db.Model, SerializerMixin):
  __tablename__ = 'users'
  id = db.Column('id', db.Integer, primary_key=True)
  itinerary_id = db.Column('itinerary_id', db.Integer, db.ForeignKey('itinerary.id'), nullable=False)
  username = db.Column('username', db.String(50), nullable=False)
  password = db.Column('password', db.String(50), nullable=False)
  
  flights = db.relationship('Flight', back_populates='users')
  itineraries = db.relationship('Itinerary', back_populates='users')
  
  serialize_rules = ('-flights.users', '-itineraries.users')
  
  @validates('itinerary_id', 'username', 'password')
  def validates_user(self,key,value):
    if not value:
      raise ValueError("User must have itinerary id, username, and password.")
    return value
  