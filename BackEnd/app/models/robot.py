from app import db
from datetime import datetime
import json


class Robot(db.Model):
    __tablename__ = 'robot'
    
    robot_id = db.Column(db.Integer, primary_key=True)
    robot_name = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(100))
    model_type = db.Column(db.String(100))  # 'CleanBot', 'Vision AI', etc.
    status = db.Column(db.String(50), default='offline', index=True)  # 'active', 'charging', 'maintenance', 'offline'
    battery_lvl = db.Column(db.Integer, default=100)
    location = db.Column(db.String(255))
    current_position = db.Column(db.JSON)  # {latitude, longitude, depth}
    firmware_version = db.Column(db.String(50))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), index=True)
    last_maint = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = db.relationship('User', foreign_keys=[owner_id])
    bookings = db.relationship('Booking', back_populates='robot', cascade='all, delete-orphan')
    missions = db.relationship('Mission', back_populates='robot', cascade='all, delete-orphan')
    sensor_data = db.relationship('SensorData', back_populates='robot', cascade='all, delete-orphan')
    ml_decisions = db.relationship('MLDecision', back_populates='robot', cascade='all, delete-orphan')
    operation_logs = db.relationship('OperationLog', back_populates='robot', cascade='all, delete-orphan')
    maintenance_records = db.relationship('Maintenance', back_populates='robot', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'robot_id': self.robot_id,
            'robot_name': self.robot_name,
            'model': self.model,
            'model_type': self.model_type,
            'status': self.status,
            'battery_lvl': self.battery_lvl,
            'location': self.location,
            'current_position': self.current_position if isinstance(self.current_position, dict) else json.loads(self.current_position) if self.current_position else None,
            'firmware_version': self.firmware_version,
            'owner_id': self.owner_id,
            'last_maint': self.last_maint.isoformat() if self.last_maint else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


