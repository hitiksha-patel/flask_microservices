from datetime import datetime
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Personal Information
    firstname = db.Column(db.String(80), nullable=False)
    middlename = db.Column(db.String(80), nullable=True)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=True)
    profilepic = db.Column(db.String(255), nullable=True)  # Store URL or filename for the profile picture
    
    # Dates and Age Information
    birthdate = db.Column(db.Date, nullable=True)
    age = db.Column(db.Integer, nullable=True)  # Optional; can be derived from birthdate
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<User {self.firstname} {self.lastname}>'
