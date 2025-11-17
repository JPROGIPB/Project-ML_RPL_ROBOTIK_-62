from app import db
from datetime import datetime
import json


class AIModel(db.Model):
    __tablename__ = 'ai_model'
    
    model_id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(255), nullable=False)
    version = db.Column(db.String(50), nullable=False)
    accuracy = db.Column(db.Numeric(5, 4))
    trained_at = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='active', index=True)  # 'active', 'deprecated', 'training'
    model_path = db.Column(db.String(500))
    hyperparameters = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    missions = db.relationship('Mission', back_populates='ai_model', foreign_keys='Mission.ai_model_id')
    ml_decisions = db.relationship('MLDecision', back_populates='ai_model', foreign_keys='MLDecision.ai_model_id')
    training_data = db.relationship('TrainingData', back_populates='model', cascade='all, delete-orphan')
    
    __table_args__ = (db.UniqueConstraint('model_name', 'version', name='unique_model_version'),)
    
    def to_dict(self):
        return {
            'model_id': self.model_id,
            'model_name': self.model_name,
            'version': self.version,
            'accuracy': float(self.accuracy) if self.accuracy else None,
            'trained_at': self.trained_at.isoformat() if self.trained_at else None,
            'status': self.status,
            'model_path': self.model_path,
            'hyperparameters': self.hyperparameters if isinstance(self.hyperparameters, dict) else json.loads(self.hyperparameters) if self.hyperparameters else None
        }


class TrainingData(db.Model):
    __tablename__ = 'training_data'
    
    data_id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('ai_model.model_id', ondelete='CASCADE'), nullable=False, index=True)
    input_data = db.Column(db.JSON, nullable=False)
    output_data = db.Column(db.JSON)
    reward = db.Column(db.Numeric(10, 4))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    model = db.relationship('AIModel', back_populates='training_data')
    
    def to_dict(self):
        return {
            'data_id': self.data_id,
            'model_id': self.model_id,
            'input_data': self.input_data,
            'output_data': self.output_data,
            'reward': float(self.reward) if self.reward else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


