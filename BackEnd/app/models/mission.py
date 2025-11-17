from app import db
from datetime import datetime
import json


class Mission(db.Model):
    __tablename__ = 'mission'
    
    mission_id = db.Column(db.Integer, primary_key=True)
    robot_id = db.Column(db.Integer, db.ForeignKey('robot.robot_id', ondelete='CASCADE'), nullable=False, index=True)
    operator_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), index=True)
    ai_model_id = db.Column(db.Integer, db.ForeignKey('ai_model.model_id'))
    name = db.Column(db.String(255))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    area_coords = db.Column(db.JSON)  # JSONB untuk fleksibilitas
    status = db.Column(db.String(50), default='planned', index=True)  # 'planned', 'active', 'completed', 'cancelled'
    area_covered = db.Column(db.Numeric(10, 2), default=0)  # km²
    waste_collected = db.Column(db.Numeric(10, 2), default=0)  # kg
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    robot = db.relationship('Robot', back_populates='missions')
    operator = db.relationship('User', foreign_keys=[operator_id])
    ai_model = db.relationship('AIModel', foreign_keys=[ai_model_id])
    operation_logs = db.relationship('OperationLog', back_populates='mission', cascade='all, delete-orphan')
    sensor_data = db.relationship('SensorData', back_populates='mission', cascade='all, delete-orphan')
    ml_decisions = db.relationship('MLDecision', back_populates='mission', cascade='all, delete-orphan')
    wastes = db.relationship('Waste', back_populates='mission', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'mission_id': self.mission_id,
            'robot_id': self.robot_id,
            'operator_id': self.operator_id,
            'ai_model_id': self.ai_model_id,
            'name': self.name,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'area_coords': self.area_coords if isinstance(self.area_coords, dict) else json.loads(self.area_coords) if self.area_coords else None,
            'status': self.status,
            'area_covered': float(self.area_covered) if self.area_covered else 0,
            'waste_collected': float(self.waste_collected) if self.waste_collected else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class OperationLog(db.Model):
    __tablename__ = 'operation_log'
    
    log_id = db.Column(db.Integer, primary_key=True)
    mission_id = db.Column(db.Integer, db.ForeignKey('mission.mission_id', ondelete='CASCADE'), index=True)
    robot_id = db.Column(db.Integer, db.ForeignKey('robot.robot_id', ondelete='CASCADE'), index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    action_type = db.Column(db.String(100), nullable=False)
    parameters = db.Column(db.JSON)
    results = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    mission = db.relationship('Mission', back_populates='operation_logs')
    robot = db.relationship('Robot', back_populates='operation_logs')
    
    def to_dict(self):
        return {
            'log_id': self.log_id,
            'mission_id': self.mission_id,
            'robot_id': self.robot_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'action_type': self.action_type,
            'parameters': self.parameters if isinstance(self.parameters, dict) else json.loads(self.parameters) if self.parameters else None,
            'results': self.results if isinstance(self.results, dict) else json.loads(self.results) if self.results else None
        }


class SensorData(db.Model):
    __tablename__ = 'sensor_data'
    
    id = db.Column(db.Integer, primary_key=True)
    robot_id = db.Column(db.Integer, db.ForeignKey('robot.robot_id', ondelete='CASCADE'), nullable=False, index=True)
    mission_id = db.Column(db.Integer, db.ForeignKey('mission.mission_id'), index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # GPS Data
    latitude = db.Column(db.Numeric(10, 8))
    longitude = db.Column(db.Numeric(11, 8))
    depth = db.Column(db.Numeric(5, 2))
    
    # Environmental
    temperature = db.Column(db.Numeric(5, 2))
    ph = db.Column(db.Numeric(4, 2))
    water_quality = db.Column(db.Numeric(5, 2))
    
    # Robot State
    battery_level = db.Column(db.Integer)
    speed = db.Column(db.Numeric(5, 2))
    
    # Camera & LIDAR
    camera_data = db.Column(db.JSON)
    lidar_data = db.Column(db.JSON)
    
    # Waste Detection
    waste_detected = db.Column(db.JSON)
    
    # Relationships
    robot = db.relationship('Robot', back_populates='sensor_data')
    mission = db.relationship('Mission', back_populates='sensor_data')
    ml_decisions = db.relationship('MLDecision', back_populates='sensor_data', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'robot_id': self.robot_id,
            'mission_id': self.mission_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'latitude': float(self.latitude) if self.latitude else None,
            'longitude': float(self.longitude) if self.longitude else None,
            'depth': float(self.depth) if self.depth else None,
            'temperature': float(self.temperature) if self.temperature else None,
            'ph': float(self.ph) if self.ph else None,
            'water_quality': float(self.water_quality) if self.water_quality else None,
            'battery_level': self.battery_level,
            'speed': float(self.speed) if self.speed else None,
            'camera_data': self.camera_data,
            'lidar_data': self.lidar_data,
            'waste_detected': self.waste_detected
        }


class MLDecision(db.Model):
    __tablename__ = 'ml_decision'
    
    id = db.Column(db.Integer, primary_key=True)
    robot_id = db.Column(db.Integer, db.ForeignKey('robot.robot_id', ondelete='CASCADE'), nullable=False, index=True)
    mission_id = db.Column(db.Integer, db.ForeignKey('mission.mission_id'), index=True)
    sensor_data_id = db.Column(db.Integer, db.ForeignKey('sensor_data.id'))
    ai_model_id = db.Column(db.Integer, db.ForeignKey('ai_model.model_id'), index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Action Output
    velocity = db.Column(db.Numeric(5, 2))
    turn_direction = db.Column(db.Numeric(6, 2))
    waste_collector_status = db.Column(db.String(50))
    navigation_mode = db.Column(db.String(50))
    target_position = db.Column(db.JSON)
    
    # ML Metadata
    confidence_score = db.Column(db.Numeric(5, 4))
    reward_value = db.Column(db.Numeric(10, 4))
    
    # Relationships
    robot = db.relationship('Robot', back_populates='ml_decisions')
    mission = db.relationship('Mission', back_populates='ml_decisions')
    sensor_data = db.relationship('SensorData', back_populates='ml_decisions')
    ai_model = db.relationship('AIModel', foreign_keys=[ai_model_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'robot_id': self.robot_id,
            'mission_id': self.mission_id,
            'sensor_data_id': self.sensor_data_id,
            'ai_model_id': self.ai_model_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'velocity': float(self.velocity) if self.velocity else None,
            'turn_direction': float(self.turn_direction) if self.turn_direction else None,
            'waste_collector_status': self.waste_collector_status,
            'navigation_mode': self.navigation_mode,
            'target_position': self.target_position,
            'confidence_score': float(self.confidence_score) if self.confidence_score else None,
            'reward_value': float(self.reward_value) if self.reward_value else None
        }


class Maintenance(db.Model):
    __tablename__ = 'maintenance'
    
    maint_id = db.Column(db.Integer, primary_key=True)
    robot_id = db.Column(db.Integer, db.ForeignKey('robot.robot_id', ondelete='CASCADE'), nullable=False, index=True)
    tech_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), index=True)
    maint_type = db.Column(db.String(100), nullable=False)
    schedule_dt = db.Column(db.DateTime)
    completed_dt = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='scheduled', index=True)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    robot = db.relationship('Robot', back_populates='maintenance_records')
    technician = db.relationship('User', foreign_keys=[tech_id])
    
    def to_dict(self):
        return {
            'maint_id': self.maint_id,
            'robot_id': self.robot_id,
            'tech_id': self.tech_id,
            'maint_type': self.maint_type,
            'schedule_dt': self.schedule_dt.isoformat() if self.schedule_dt else None,
            'completed_dt': self.completed_dt.isoformat() if self.completed_dt else None,
            'status': self.status,
            'notes': self.notes
        }


