from app import db
from datetime import datetime

class PersonalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # Type of record (self, spouse, child, account)
    name = db.Column(db.String(128), nullable=True)  
    dob = db.Column(db.Date, nullable=True)
    ssn = db.Column(db.String(256), nullable=True)  # Will need encryption
    account_number = db.Column(db.String(256), nullable=True)  # Will need encryption
    account_type = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)