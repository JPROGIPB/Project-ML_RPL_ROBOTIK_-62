from app import db
from datetime import datetime


class Permission(db.Model):
    __tablename__ = 'permission'
    
    perm_id = db.Column(db.Integer, primary_key=True)
    perm_name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    roles = db.relationship('RolePermission', back_populates='permission', cascade='all, delete-orphan')


class Role(db.Model):
    __tablename__ = 'role'
    
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    users = db.relationship('User', back_populates='role')
    permissions = db.relationship('RolePermission', back_populates='role', cascade='all, delete-orphan')


class RolePermission(db.Model):
    __tablename__ = 'role_permission'
    
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id', ondelete='CASCADE'), primary_key=True)
    perm_id = db.Column(db.Integer, db.ForeignKey('permission.perm_id', ondelete='CASCADE'), primary_key=True)
    
    # Relationships
    role = db.relationship('Role', back_populates='permissions')
    permission = db.relationship('Permission', back_populates='roles')


class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)  # Hashed password
    full_name = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), index=True)
    is_certified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    role = db.relationship('Role', back_populates='users')
    certificates = db.relationship('Certificate', back_populates='user', cascade='all, delete-orphan')
    certification_progress = db.relationship('UserCertificationProgress', back_populates='user', cascade='all, delete-orphan')
    bookings = db.relationship('Booking', back_populates='user', cascade='all, delete-orphan')
    missions = db.relationship('Mission', back_populates='operator', foreign_keys='Mission.operator_id')
    feedbacks = db.relationship('Feedback', back_populates='user', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role.role_name if self.role else None,
            'is_certified': self.is_certified,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


