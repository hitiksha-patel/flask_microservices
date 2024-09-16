from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Personal Information
    firstname = db.Column(db.String(80), nullable=True)
    middlename = db.Column(db.String(80), nullable=True)
    lastname = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    address = db.Column(db.String(200), nullable=True)
    profilepic = db.Column(db.String(255), nullable=True)
    password_hash = db.Column(db.Text, nullable=False)
    
    # Dates and Age Information
    birthdate = db.Column(db.Date, nullable=True)
    age = db.Column(db.Integer, nullable=True)  # Optional; can be derived from birthdate
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the given password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.firstname} {self.lastname}>'
