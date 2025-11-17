from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models.user import User
from app.models.certificate import Certificate, CertificationModule, UserCertificationProgress

bp = Blueprint('certification', __name__)


@bp.route('/modules', methods=['GET'])
def get_modules():
    """Get all certification modules"""
    try:
        modules = CertificationModule.query.order_by(CertificationModule.order_index).all()
        
        return jsonify({
            'modules': [module.to_dict() for module in modules]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/progress', methods=['GET'])
@jwt_required()
def get_progress():
    """Get user certification progress"""
    try:
        user_id = int(get_jwt_identity())  # Convert string to int
        print(f"Getting progress for user_id: {user_id}")

        progress = UserCertificationProgress.query.filter_by(user_id=user_id).all()
        modules = CertificationModule.query.order_by(CertificationModule.order_index).all()

        print(f"Found {len(progress)} progress records and {len(modules)} modules")
        
        # Create progress map
        progress_map = {p.module_id: p for p in progress}
        
        # Calculate overall progress
        total_progress = 0
        completed_modules = 0
        
        result = []
        for module in modules:
            module_progress = progress_map.get(module.id)
            if module_progress:
                total_progress += module_progress.progress_percentage
                if module_progress.completed:
                    completed_modules += 1
                result.append({
                    **module.to_dict(),
                    'completed': module_progress.completed,
                    'progress_percentage': module_progress.progress_percentage
                })
            else:
                result.append({
                    **module.to_dict(),
                    'completed': False,
                    'progress_percentage': 0
                })
        
        overall_progress = total_progress // len(modules) if modules else 0
        
        response_data = {
            'modules': result,
            'overall_progress': overall_progress,
            'completed_modules': completed_modules,
            'total_modules': len(modules),
            'is_certified': overall_progress == 100
        }

        print(f"Returning progress data: overall={overall_progress}%, completed={completed_modules}/{len(modules)}")

        return jsonify(response_data), 200

    except Exception as e:
        print(f"Error in get_progress: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@bp.route('/progress/<int:module_id>', methods=['POST'])
@jwt_required()
def update_progress(module_id):
    """Update certification module progress"""
    try:
        user_id = int(get_jwt_identity())  # Convert string to int
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        # Check if module exists
        module = CertificationModule.query.get(module_id)
        if not module:
            return jsonify({'error': f'Module {module_id} not found'}), 404

        # Get and validate progress_percentage
        progress_percentage = data.get('progress_percentage')
        if progress_percentage is None:
            return jsonify({'error': 'progress_percentage is required'}), 400

        try:
            progress_percentage = int(progress_percentage)
        except (ValueError, TypeError):
            return jsonify({'error': 'progress_percentage must be a number'}), 400

        # Validate range
        if progress_percentage < 0 or progress_percentage > 100:
            return jsonify({'error': 'progress_percentage must be between 0 and 100'}), 400

        completed = bool(data.get('completed', False))
        
        # Get or create progress
        progress = UserCertificationProgress.query.filter_by(
            user_id=user_id,
            module_id=module_id
        ).first()
        
        if not progress:
            progress = UserCertificationProgress(
                user_id=user_id,
                module_id=module_id,
                progress_percentage=progress_percentage,
                completed=completed
            )
            db.session.add(progress)
        else:
            progress.progress_percentage = progress_percentage
            progress.completed = completed
            if completed and not progress.completed_at:
                progress.completed_at = datetime.utcnow()
        
        db.session.commit()
        
        # Check if all modules completed
        user = User.query.get(user_id)
        all_progress = UserCertificationProgress.query.filter_by(user_id=user_id).all()
        all_completed = all(
            p.completed for p in all_progress
            if p.module_id in [m.id for m in CertificationModule.query.all()]
        )
        
        if all_completed and not user.is_certified:
            user.is_certified = True
            # Create certificate
            cert = Certificate(
                user_id=user_id,
                cert_type='Operator Certification',
                issued_date=datetime.utcnow(),
                status='active',
                cert_number=f'SEAL-{user_id}-{int(datetime.utcnow().timestamp())}'
            )
            db.session.add(cert)
            db.session.commit()
        
        return jsonify({
            'message': 'Progress updated',
            'progress': progress.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/complete', methods=['POST'])
@jwt_required()
def complete_certification():
    """Complete certification (simulate completion)"""
    try:
        user_id = int(get_jwt_identity())  # Convert string to int
        user = User.query.get(user_id)
        
        # Get all modules
        modules = CertificationModule.query.order_by(CertificationModule.order_index).all()
        
        # Mark all as completed
        for module in modules:
            progress = UserCertificationProgress.query.filter_by(
                user_id=user_id,
                module_id=module.id
            ).first()
            
            if not progress:
                progress = UserCertificationProgress(
                    user_id=user_id,
                    module_id=module.id,
                    progress_percentage=100,
                    completed=True,
                    completed_at=datetime.utcnow()
                )
                db.session.add(progress)
            else:
                progress.progress_percentage = 100
                progress.completed = True
                if not progress.completed_at:
                    progress.completed_at = datetime.utcnow()
        
        # Update user
        user.is_certified = True
        
        # Create certificate
        cert = Certificate(
            user_id=user_id,
            cert_type='Operator Certification',
            issued_date=datetime.utcnow(),
            status='active',
            cert_number=f'SEAL-{user_id}-{int(datetime.utcnow().timestamp())}'
        )
        db.session.add(cert)
        db.session.commit()
        
        return jsonify({
            'message': 'Certification completed',
            'certificate': cert.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

