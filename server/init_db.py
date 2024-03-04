from app import app, db
from models import User, Itinerary, Flight


# Ensure you import db from your app or models file, depending on where it's initialized


def initialize_database():
    with app.app_context():
        # Create tables
        db.create_all()
        # Optionally, add initial data


if __name__ == "__main__":
    initialize_database()
    print("Database initialized!")
