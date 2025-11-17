from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from app import db
from app.models.booking import Booking, Payment
from app.models.user import User
from app.models.product import Product
from app.models.robot import Robot

bp = Blueprint('bookings', __name__)


@bp.route('', methods=['GET'])
@jwt_required()
def get_bookings():
    """Get user bookings"""
    try:
        user_id = int(get_jwt_identity())  # Convert string to int
        user = User.query.get(user_id)
        
        query = Booking.query.filter_by(user_id=user_id)
        
        # Filter by status if provided
        status = request.args.get('status')
        if status:
            query = query.filter_by(status=status)
        
        bookings = query.order_by(Booking.created_at.desc()).all()
        
        return jsonify({
            'bookings': [booking.to_dict() for booking in bookings]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('', methods=['POST'])
@jwt_required()
def create_booking():
    """Create new booking (rental or purchase)"""
    try:
        user_id = int(get_jwt_identity())  # Convert string to int
        data = request.get_json()
        
        # Validation
        booking_type = data.get('booking_type')  # 'rental' or 'purchase'
        if booking_type not in ['rental', 'purchase']:
            return jsonify({'error': 'Invalid booking_type. Must be "rental" or "purchase"'}), 400
        
        start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
        
        # Calculate end_date and duration for rental
        if booking_type == 'rental':
            duration_days = data.get('duration_days', 1)
            end_date = start_date + timedelta(days=duration_days)
        else:
            duration_days = None
            end_date = None
        
        # Get product or robot
        product_id = data.get('product_id')
        robot_id = data.get('robot_id')
        
        if booking_type == 'purchase' and not product_id:
            return jsonify({'error': 'product_id is required for purchase'}), 400
        
        if booking_type == 'rental' and not robot_id:
            return jsonify({'error': 'robot_id is required for rental'}), 400
        
        # Calculate total cost
        if booking_type == 'purchase':
            product = Product.query.get_or_404(product_id)
            total_cost = float(product.price)
        else:
            # Rental pricing (simplified)
            robot = Robot.query.get_or_404(robot_id)
            price_per_day = 1500000  # Default rental price
            total_cost = price_per_day * duration_days
        
        # Create booking
        booking = Booking(
            user_id=user_id,
            robot_id=robot_id,
            product_id=product_id,
            booking_type=booking_type,
            start_date=start_date,
            end_date=end_date,
            duration_days=duration_days,
            location=data.get('location'),
            status='pending',
            total_cost=total_cost
        )
        
        db.session.add(booking)
        db.session.commit()
        
        return jsonify({
            'message': 'Booking created successfully',
            'booking': booking.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_booking(booking_id):
    """Get booking details"""
    try:
        user_id = int(get_jwt_identity())  # Convert string to int
        booking = Booking.query.get_or_404(booking_id)
        
        # Check ownership
        if booking.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify(booking.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:booking_id>/payment', methods=['POST'])
@jwt_required()
def create_payment(booking_id):
    """Create payment for booking"""
    try:
        user_id = int(get_jwt_identity())  # Convert string to int
        booking = Booking.query.get_or_404(booking_id)
        
        # Check ownership
        if booking.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        # Create payment
        payment = Payment(
            booking_id=booking_id,
            amount=booking.total_cost,
            method=data.get('method', 'credit-card'),
            status='completed',  # Simulated - always success
            paid_at=datetime.utcnow(),
            transaction_id=f'TXN{booking_id}{int(datetime.utcnow().timestamp())}'
        )
        
        # Update booking status
        booking.status = 'confirmed'
        
        db.session.add(payment)
        db.session.commit()
        
        return jsonify({
            'message': 'Payment successful',
            'payment': payment.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


