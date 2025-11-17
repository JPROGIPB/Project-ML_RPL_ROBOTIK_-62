from app import db
from datetime import datetime
import json


class Waste(db.Model):
    __tablename__ = 'waste'
    
    waste_id = db.Column(db.Integer, primary_key=True)
    mission_id = db.Column(db.Integer, db.ForeignKey('mission.mission_id', ondelete='CASCADE'), nullable=False, index=True)
    waste_type = db.Column(db.String(100), nullable=False, index=True)
    weight = db.Column(db.Numeric(10, 2), nullable=False)
    location = db.Column(db.JSON)  # {latitude, longitude, depth}
    detected_at = db.Column(db.DateTime, nullable=False)
    collected = db.Column(db.Boolean, default=False)
    collected_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    mission = db.relationship('Mission', back_populates='wastes')
    
    def to_dict(self):
        return {
            'waste_id': self.waste_id,
            'mission_id': self.mission_id,
            'waste_type': self.waste_type,
            'weight': float(self.weight) if self.weight else 0,
            'location': self.location if isinstance(self.location, dict) else json.loads(self.location) if self.location else None,
            'detected_at': self.detected_at.isoformat() if self.detected_at else None,
            'collected': self.collected,
            'collected_at': self.collected_at.isoformat() if self.collected_at else None
        }


