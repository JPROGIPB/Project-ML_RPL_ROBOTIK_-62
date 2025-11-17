from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from app import db
from app.models.robot import Robot
from app.models.mission import Mission, OperationLog
from app.models.waste import Waste
from app.models.user import User
from app.models.booking import Booking
from app.utils.auth import role_required

bp = Blueprint('dashboard', __name__)


@bp.route('/overview', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_overview():
    """Get dashboard overview"""
    try:
        user_id = int(get_jwt_identity())  # Convert string to int
        user = User.query.get(user_id)
        
        # Get robots count
        robots_query = Robot.query
        if user.role and user.role.role_name == 'customer':
            robots_query = robots_query.filter_by(owner_id=user_id)
        
        robots_total = robots_query.count()
        robots_active = robots_query.filter_by(status='active').count()
        
        # Get today's stats
        today = datetime.utcnow().date()
        today_missions = Mission.query.filter(
            db.func.date(Mission.start_time) == today
        ).all()
        
        area_cleaned_today = sum(float(m.area_covered or 0) for m in today_missions)
        waste_collected_today = sum(float(m.waste_collected or 0) for m in today_missions)
        
        # Get recent activity
        recent_logs = OperationLog.query.order_by(
            OperationLog.timestamp.desc()
        ).limit(5).all()
        
        activity = []
        for log in recent_logs:
            robot = Robot.query.get(log.robot_id)
            activity.append({
                'id': log.log_id,
                'time': log.timestamp.strftime('%H:%M') if log.timestamp else None,
                'activity': f'Robot {robot.robot_name if robot else "Unknown"} - {log.action_type}',
                'status': 'success' if 'success' in log.action_type.lower() else 'info'
            })
        
        return jsonify({
            'robots_active': robots_active,
            'robots_total': robots_total,
            'area_cleaned_today': round(area_cleaned_today, 2),
            'waste_collected_today': round(waste_collected_today, 2),
            'energy_efficiency': 87.5,  # Simulated
            'water_quality_avg': 7.4,  # Simulated
            'recent_activity': activity
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/robots/status', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_robots_status():
    """Get all robots status"""
    try:
        user_id = int(get_jwt_identity())  # Convert string to int
        user = User.query.get(user_id)
        
        query = Robot.query
        if user.role and user.role.role_name == 'customer':
            query = query.filter_by(owner_id=user_id)
        
        robots = query.all()
        
        result = []
        for robot in robots:
            # Get latest mission for area_cleaned
            latest_mission = Mission.query.filter_by(robot_id=robot.robot_id)\
                .order_by(Mission.start_time.desc()).first()
            
            result.append({
                'robot_id': robot.robot_id,
                'name': robot.robot_name,
                'status': robot.status,
                'battery': robot.battery_lvl,
                'area_cleaned': float(latest_mission.area_covered) if latest_mission and latest_mission.area_covered else 0,
                'current_mission': {
                    'id': latest_mission.mission_id,
                    'name': latest_mission.name
                } if latest_mission else None
            })
        
        return jsonify({
            'robots': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/analytics/performance', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_performance_analytics():
    """Get performance analytics"""
    try:
        # Get last 24 hours data (simulated)
        performance_data = [
            {'time': '00:00', 'area': 0.2, 'energy': 95},
            {'time': '04:00', 'area': 1.4, 'energy': 82},
            {'time': '08:00', 'area': 2.8, 'energy': 68},
            {'time': '12:00', 'area': 4.2, 'energy': 54},
            {'time': '16:00', 'area': 5.6, 'energy': 40},
            {'time': '20:00', 'area': 6.8, 'energy': 28},
            {'time': '24:00', 'area': 8.2, 'energy': 15}
        ]
        
        return jsonify({
            'performance_data': performance_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/activity-log', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_activity_log():
    """Get activity log"""
    try:
        limit = request.args.get('limit', 20, type=int)

        logs = OperationLog.query.order_by(
            OperationLog.timestamp.desc()
        ).limit(limit).all()

        activity = []
        for log in logs:
            robot = Robot.query.get(log.robot_id)
            activity.append({
                'id': log.log_id,
                'time': log.timestamp.strftime('%H:%M') if log.timestamp else None,
                'activity': f'Robot {robot.robot_name if robot else "Unknown"} - {log.action_type}',
                'status': 'success' if 'success' in log.action_type.lower() else 'info'
            })

        return jsonify({
            'activity': activity
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/bookings', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_bookings():
    """Get all bookings (admin only)"""
    try:
        user_id = int(get_jwt_identity())  # Convert string to int
        limit = request.args.get('limit', 50, type=int)

        # Get all bookings for admin (not filtered by user)
        bookings = Booking.query.order_by(
            Booking.created_at.desc()
        ).limit(limit).all()

        return jsonify({
            'bookings': [booking.to_dict() for booking in bookings]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


