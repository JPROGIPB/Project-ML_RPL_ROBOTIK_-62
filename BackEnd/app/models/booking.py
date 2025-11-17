from app import db
from datetime import datetime


class Booking(db.Model):
    __tablename__ = 'booking'
    
    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    robot_id = db.Column(db.Integer, db.ForeignKey('robot.robot_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    booking_type = db.Column(db.String(50), nullable=False, index=True)  # 'rental' or 'purchase'
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)  # NULL untuk purchase
    duration_days = db.Column(db.Integer)  # untuk rental
    location = db.Column(db.String(255))
    status = db.Column(db.String(50), default='pending', index=True)  # 'pending', 'confirmed', 'active', 'completed', 'cancelled'
    total_cost = db.Column(db.Numeric(15, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='bookings')
    robot = db.relationship('Robot', back_populates='bookings')
    product = db.relationship('Product', back_populates='bookings')
    payments = db.relationship('Payment', back_populates='booking', cascade='all, delete-orphan')
    feedbacks = db.relationship('Feedback', back_populates='booking', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'booking_id': self.booking_id,
            'user_id': self.user_id,
            'robot_id': self.robot_id,
            'product_id': self.product_id,
            'booking_type': self.booking_type,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'duration_days': self.duration_days,
            'location': self.location,
            'status': self.status,
            'total_cost': float(self.total_cost) if self.total_cost else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Payment(db.Model):
    __tablename__ = 'payment'
    
    payment_id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.booking_id', ondelete='CASCADE'), nullable=False, index=True)
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    method = db.Column(db.String(50), nullable=False)  # 'credit-card', 'e-wallet', 'bank-transfer'
    status = db.Column(db.String(50), default='pending', index=True)  # 'pending', 'completed', 'failed', 'refunded'
    paid_at = db.Column(db.DateTime)
    transaction_id = db.Column(db.String(255), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    booking = db.relationship('Booking', back_populates='payments')
    
    def to_dict(self):
        return {
            'payment_id': self.payment_id,
            'booking_id': self.booking_id,
            'amount': float(self.amount) if self.amount else 0,
            'method': self.method,
            'status': self.status,
            'paid_at': self.paid_at.isoformat() if self.paid_at else None,
            'transaction_id': self.transaction_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }



