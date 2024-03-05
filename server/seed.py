from extensions import db
from app import app
from models import Flight, Itinerary, User
from datetime import datetime
from bcrypt import bcrypt

def seed_data():
    # Delete existing data
    db.session.query(Flight).delete()
    db.session.query(Itinerary).delete()
    db.session.query(User).delete()

    # Add new records
    hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
    user1 = User(username="John Doe", password=hashed_password)
    user2 = User(username="Jane Smith", password=hashed_password)

    flight1 = Flight(flight_number="FL123", origin="City A", destination="City B", departure_time=datetime.strptime("2023-04-01 10:00:00", "%Y-%m-%d %H:%M:%S"))
    flight2 = Flight(flight_number="FL456", origin="City C", destination="City D", departure_time=datetime.strptime("2023-04-02 15:00:00", "%Y-%m-%d %H:%M:%S"))

    # It's important to add and commit users and flights before creating itineraries to ensure they have IDs.
    db.session.add_all([user1, user2, flight1, flight2])
    db.session.commit()

    # Now, use the actual instances of users and flights to create itineraries
    itinerary1 = Itinerary(user_id=user1.id, flight_id=flight1.id)
    itinerary2 = Itinerary(user_id=user2.id, flight_id=flight2.id)

    db.session.add_all([itinerary1, itinerary2])
    db.session.commit()

    print("Database seeded!")

if __name__ == "__main__":
    with app.app_context():
        seed_data()
