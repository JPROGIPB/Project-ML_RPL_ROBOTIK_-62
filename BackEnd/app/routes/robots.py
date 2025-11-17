from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.robot import Robot
from app.models.user import User
from app.models.mission import SensorData
from app.utils.auth import role_required

bp = Blueprint('robots', __name__)


@bp.route('', methods=['GET'])
@jwt_required()
def get_robots():
    """Get list of robots"""
    try:
        user_id = int(get_jwt_identity())  # Convert string to int
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Check if request is for rental (available robots)
        for_rental = request.args.get('for_rental', 'false').lower() == 'true'

        query = Robot.query

        if for_rental:
            # For rental: show robots without owner (available for rent)
            query = query.filter(
                (Robot.owner_id == None) | (Robot.owner_id == user_id)
            )
        else:
            # Normal mode: filter by role
            # Customer hanya bisa lihat robot yang mereka own
            # Admin dan Operator bisa lihat semua robots
            if user.role and user.role.role_name == 'customer':
                query = query.filter_by(owner_id=user_id)

        robots = query.all()

        return jsonify({
            'robots': [robot.to_dict() for robot in robots]
        }), 200

    except Exception as e:
        print(f"Error in get_robots: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:robot_id>', methods=['GET'])
@jwt_required()
def get_robot(robot_id):
    """Get robot details"""
    try:
        robot = Robot.query.get_or_404(robot_id)
        return jsonify(robot.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:robot_id>/status', methods=['GET'])
@jwt_required()
def get_robot_status(robot_id):
    """Get real-time robot status"""
    try:
        robot = Robot.query.get_or_404(robot_id)
        
        # Get latest sensor data
        latest_sensor = SensorData.query.filter_by(robot_id=robot_id)\
            .order_by(SensorData.timestamp.desc()).first()
        
        status = {
            'robot_id': robot.robot_id,
            'connected': robot.status == 'active',
            'battery': robot.battery_lvl,
            'position': robot.current_position or {},
            'sensors': {
                'temperature': float(latest_sensor.temperature) if latest_sensor and latest_sensor.temperature else None,
                'ph': float(latest_sensor.ph) if latest_sensor and latest_sensor.ph else None,
                'water_quality': float(latest_sensor.water_quality) if latest_sensor and latest_sensor.water_quality else None
            } if latest_sensor else {},
            'speed': float(latest_sensor.speed) if latest_sensor and latest_sensor.speed else 0,
            'status': robot.status,
            'timestamp': robot.updated_at.isoformat() if robot.updated_at else None
        }
        
        return jsonify(status), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:robot_id>/control/start', methods=['POST'])
@jwt_required()
@role_required('admin', 'operator')
def start_robot(robot_id):
    """Start robot simulation"""
    try:
        robot = Robot.query.get_or_404(robot_id)
        
        if robot.status == 'active':
            return jsonify({'error': 'Robot is already active'}), 400
        
        robot.status = 'active'
        db.session.commit()
        
        return jsonify({
            'message': 'Robot started successfully',
            'robot_id': robot.robot_id,
            'status': robot.status
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:robot_id>/control/stop', methods=['POST'])
@jwt_required()
@role_required('admin', 'operator')
def stop_robot(robot_id):
    """Stop robot simulation"""
    try:
        robot = Robot.query.get_or_404(robot_id)
        
        robot.status = 'offline'
        db.session.commit()
        
        return jsonify({
            'message': 'Robot stopped successfully',
            'robot_id': robot.robot_id,
            'status': robot.status
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:robot_id>/control/manual', methods=['POST'])
@jwt_required()
@role_required('admin', 'operator')
def manual_control(robot_id):
    """Manual control command (simulated)"""
    try:
        data = request.get_json()
        robot = Robot.query.get_or_404(robot_id)
        
        if robot.status != 'active':
            return jsonify({'error': 'Robot is not active'}), 400
        
        # Simulate command execution
        action = data.get('action')
        direction = data.get('direction')
        speed = data.get('speed', 0)
        
        # Update robot state (simulated)
        if action == 'move' and speed:
            robot.battery_lvl = max(0, robot.battery_lvl - 1)  # Simulate battery drain
        
        db.session.commit()
        
        return jsonify({
            'message': 'Command executed',
            'robot_id': robot.robot_id,
            'command_id': f'cmd_{robot_id}_{int(__import__("time").time())}'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:robot_id>/control/mode', methods=['PUT'])
@jwt_required()
@role_required('admin', 'operator')
def switch_mode(robot_id):
    """Switch control mode (manual/auto)"""
    try:
        data = request.get_json()
        mode = data.get('mode')
        
        if mode not in ['manual', 'auto']:
            return jsonify({'error': 'Invalid mode. Must be "manual" or "auto"'}), 400
        
        robot = Robot.query.get_or_404(robot_id)
        
        # Store mode in robot model or separate table (simplified here)
        # For now, we'll just return success
        
        return jsonify({
            'message': f'Mode switched to {mode}',
            'robot_id': robot.robot_id,
            'mode': mode
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

