from app import db
from datetime import datetime


class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    feedback_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.booking_id', ondelete='CASCADE'), nullable=False, index=True)
    rating = db.Column(db.Integer)  # 1-5
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='feedbacks')
    booking = db.relationship('Booking', back_populates='feedbacks')
    
    def to_dict(self):
        return {
            'feedback_id': self.feedback_id,
            'user_id': self.user_id,
            'booking_id': self.booking_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


