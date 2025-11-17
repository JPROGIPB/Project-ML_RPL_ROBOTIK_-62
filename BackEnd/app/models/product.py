from app import db
from datetime import datetime
import json


class Product(db.Model):
    __tablename__ = 'product'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=False, index=True)  # 'Robot', 'Aksesori', 'Spare Part'
    price = db.Column(db.Numeric(15, 2), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    features = db.Column(db.JSON)  # JSON array of features
    is_available = db.Column(db.Boolean, default=True, index=True)
    stock_quantity = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', back_populates='product', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': float(self.price) if self.price else 0,
            'description': self.description,
            'image_url': self.image_url,
            'features': self.features if isinstance(self.features, list) else json.loads(self.features) if self.features else [],
            'is_available': self.is_available,
            'stock_quantity': self.stock_quantity
        }


