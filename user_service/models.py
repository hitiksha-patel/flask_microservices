from datetime import datetime
from . import db, bcrypt

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
    age = db.Column(db.Integer, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Constructor
    def __init__(self, email, password):
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Password verification method
    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    # Representation method
    def __repr__(self):
        return f'<User {self.firstname} {self.lastname}>'
