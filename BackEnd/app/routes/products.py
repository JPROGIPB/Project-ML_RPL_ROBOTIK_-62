from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.product import Product

bp = Blueprint('products', __name__)


@bp.route('', methods=['GET'])
def get_products():
    """Get product catalog"""
    try:
        category = request.args.get('category')
        query = Product.query.filter_by(is_available=True)
        
        if category:
            query = query.filter_by(category=category)
        
        products = query.all()
        
        return jsonify({
            'products': [product.to_dict() for product in products]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get product details"""
    try:
        product = Product.query.get_or_404(product_id)
        return jsonify(product.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


