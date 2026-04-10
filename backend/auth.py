from flask import Blueprint, request, jsonify
from app import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        if User.query.filter_by(email=data.get('email')).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        user = User(
            email=data.get('email'),
            phone=data.get('phone'),
            password_hash=generate_password_hash(data.get('password')),
            is_admin=False
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user_id': user.id
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data.get('email')).first()
        
        if not user or not check_password_hash(user.password_hash, data.get('password')):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        return jsonify({
            'success': True,
            'user_id': user.id,
            'email': user.email,
            'is_admin': user.is_admin
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """Admin dashboard statistics"""
    try:
        from models import Complaint
        
        total = Complaint.query.count()
        high_priority = Complaint.query.filter_by(priority='High').count()
        new = Complaint.query.filter_by(status='New').count()
        in_progress = Complaint.query.filter_by(status='In Progress').count()
        resolved = Complaint.query.filter_by(status='Resolved').count()
        
        categories = {}
        for complaint in Complaint.query.all():
            categories[complaint.category] = categories.get(complaint.category, 0) + 1
        
        return jsonify({
            'total': total,
            'high_priority': high_priority,
            'new': new,
            'in_progress': in_progress,
            'resolved': resolved,
            'categories': categories
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/complaints', methods=['GET'])
def get_all_complaints():
    """Get all complaints with filters"""
    from models import Complaint
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    priority = request.args.get('priority')
    
    query = Complaint.query
    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    
    paginated = query.order_by(Complaint.created_at.desc()).paginate(page=page, per_page=per_page)
    
    return jsonify({
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page,
        'complaints': [c.to_dict() for c in paginated.items]
    }), 200


@admin_bp.route('/complaints/<int:complaint_id>/assign', methods=['PUT'])
def assign_complaint(complaint_id):
    """Assign complaint to staff member"""
    try:
        from models import Complaint
        complaint = Complaint.query.get_or_404(complaint_id)
        data = request.get_json()
        
        complaint.assigned_to = data.get('assigned_to')
        complaint.status = 'In Progress'
        complaint.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify(complaint.to_dict()), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
