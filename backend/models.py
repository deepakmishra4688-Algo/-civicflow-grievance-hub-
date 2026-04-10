from backend.extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    complaints = db.relationship('Complaint', backref='citizen', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'


class Complaint(db.Model):
    __tablename__ = 'complaints'
    
    id = db.Column(db.Integer, primary_key=True)
    ref_id = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120))
    location = db.Column(db.String(255), nullable=False)
    language = db.Column(db.String(50), default='English')
    complaint_text = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(20), default='Normal')
    status = db.Column(db.String(50), default='New')
    attachments = db.Column(db.JSON, default=[])
    assigned_to = db.Column(db.String(120))
    resolution_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'ref_id': self.ref_id,
            'name': self.name,
            'phone': self.phone,
            'location': self.location,
            'language': self.language,
            'complaint_text': self.complaint_text,
            'category': self.category,
            'department': self.department,
            'priority': self.priority,
            'status': self.status,
            'attachments': self.attachments,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        return f'<Complaint {self.ref_id}>'
