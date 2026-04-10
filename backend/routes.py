from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_mail import Message
import uuid

from backend.extensions import db, mail
from backend.classifier import classify_complaint
from backend.models import Complaint, User

complaints_bp = Blueprint('complaints', __name__, url_prefix='/api/complaints')

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@complaints_bp.route('/submit', methods=['POST'])
def submit_complaint():
    """Submit a new complaint"""
    try:
        data = request.get_json()
        
        # Classify the complaint
        classification = classify_complaint(data.get('complaint_text', ''))
        
        # Generate reference ID
        ref_id = f"CMP-{uuid.uuid4().hex[:8].upper()}"
        
        # Determine or create anonymous user if no user_id is provided
        user_id = data.get('user_id')
        if user_id is None:
            anonymous = User.query.filter_by(email='anonymous@civicflow.local').first()
            if not anonymous:
                anonymous = User(
                    email='anonymous@civicflow.local',
                    phone='0000000000',
                    password_hash='anonymous',
                    is_admin=False
                )
                db.session.add(anonymous)
                db.session.flush()
            user_id = anonymous.id

        # Create complaint record
        complaint = Complaint(
            ref_id=ref_id,
            user_id=user_id,
            name=data.get('name'),
            phone=data.get('phone'),
            email=data.get('email'),
            location=data.get('location'),
            language=data.get('language', 'English'),
            complaint_text=data.get('complaint_text'),
            category=classification['category'],
            department=classification['department'],
            priority=classification['priority'],
            status='New',
            attachments=data.get('attachments', [])
        )
        
        db.session.add(complaint)
        db.session.commit()
        
        # Send confirmation email
        try:
            send_confirmation_email(complaint)
        except:
            pass
        
        return jsonify({
            'success': True,
            'ref_id': ref_id,
            'category': classification['category'],
            'department': classification['department'],
            'priority': classification['priority']
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@complaints_bp.route('/<int:complaint_id>', methods=['GET'])
def get_complaint(complaint_id):
    """Get complaint details"""
    complaint = Complaint.query.get_or_404(complaint_id)
    return jsonify(complaint.to_dict()), 200


@complaints_bp.route('/<ref_id>', methods=['GET'])
def get_complaint_by_ref(ref_id):
    """Get complaint by reference ID"""
    complaint = Complaint.query.filter_by(ref_id=ref_id).first_or_404()
    return jsonify(complaint.to_dict()), 200


@complaints_bp.route('/<int:complaint_id>', methods=['PUT'])
def update_complaint(complaint_id):
    """Update complaint status or notes"""
    try:
        complaint = Complaint.query.get_or_404(complaint_id)
        data = request.get_json()
        
        if 'status' in data:
            complaint.status = data['status']
        if 'resolution_notes' in data:
            complaint.resolution_notes = data['resolution_notes']
        if 'assigned_to' in data:
            complaint.assigned_to = data['assigned_to']
        
        if complaint.status == 'Resolved':
            complaint.resolved_at = datetime.utcnow()
        
        complaint.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(complaint.to_dict()), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@complaints_bp.route('/search', methods=['GET'])
def search_complaints():
    """Search complaints by various filters"""
    category = request.args.get('category')
    status = request.args.get('status')
    priority = request.args.get('priority')
    location = request.args.get('location')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Complaint.query
    
    if category:
        query = query.filter_by(category=category)
    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    if location:
        query = query.filter(Complaint.location.ilike(f'%{location}%'))
    
    paginated = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page,
        'complaints': [c.to_dict() for c in paginated.items]
    }), 200


def send_confirmation_email(complaint):
    """Send confirmation email to citizen"""
    try:
        recipients = [complaint.email] if complaint.email else []
        if not recipients:
            return

        msg = Message(
            subject=f'Grievance Registered: {complaint.ref_id}',
            recipients=recipients,
            body=f'''
Dear {complaint.name},

Your grievance has been registered with Reference ID: {complaint.ref_id}

Category: {complaint.category}
Department: {complaint.department}
Priority: {complaint.priority}
Status: New

You can track your complaint status using the reference ID.

Thank you for using CivicFlow Grievance Hub.
            '''
        )
        mail.send(msg)
    except:
        pass


# Auth Routes
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
            password_hash=data.get('password'),
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


# Admin Routes
@admin_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """Admin dashboard statistics"""
    try:
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
            'total_complaints': total,
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
