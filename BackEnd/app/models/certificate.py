from app import db
from datetime import datetime


class Certificate(db.Model):
    __tablename__ = 'certificate'
    
    cert_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    cert_type = db.Column(db.String(100), nullable=False)
    issued_date = db.Column(db.DateTime, nullable=False)
    expiry_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='active', index=True)  # 'active', 'expired', 'revoked'
    cert_number = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='certificates')
    
    def to_dict(self):
        return {
            'cert_id': self.cert_id,
            'user_id': self.user_id,
            'cert_type': self.cert_type,
            'issued_date': self.issued_date.isoformat() if self.issued_date else None,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'status': self.status,
            'cert_number': self.cert_number
        }


class CertificationModule(db.Model):
    __tablename__ = 'certification_module'
    
    id = db.Column(db.Integer, primary_key=True)
    module_number = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    duration_minutes = db.Column(db.Integer)
    description = db.Column(db.Text)
    order_index = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user_progress = db.relationship('UserCertificationProgress', back_populates='module', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'module_number': self.module_number,
            'title': self.title,
            'duration_minutes': self.duration_minutes,
            'description': self.description,
            'order_index': self.order_index
        }


class UserCertificationProgress(db.Model):
    __tablename__ = 'user_certification_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    module_id = db.Column(db.Integer, db.ForeignKey('certification_module.id', ondelete='CASCADE'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    progress_percentage = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='certification_progress')
    module = db.relationship('CertificationModule', back_populates='user_progress')
    
    __table_args__ = (db.UniqueConstraint('user_id', 'module_id', name='unique_user_module'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'module_id': self.module_id,
            'completed': self.completed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'progress_percentage': self.progress_percentage
        }


