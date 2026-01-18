"""
Admin API Routes Blueprint
---------------------------
Handles admin panel endpoints and authentication.
"""

from flask import Blueprint, request, jsonify, session, redirect, send_from_directory
from functools import wraps
from models import admin_api
from utils.validators import validate_username
from utils.security import get_client_ip
from utils.logger import log_login_attempt, log_logout, log_admin_action, log_unauthorized_access

# Create blueprint
admin_bp = Blueprint('admin', __name__)

# Shared database components (injected from app.py)
_cursor = None
_db_connection = None

def init_admin_routes(cursor, db_connection):
    """Initialize admin routes with database components"""
    global _cursor, _db_connection
    _cursor = cursor
    _db_connection = db_connection

def require_admin(f):
    """Decorator to protect admin routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            log_unauthorized_access(get_client_ip(request), request.endpoint)
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

# ==========================================
# ADMIN PAGE ROUTES
# ==========================================

@admin_bp.route('/admin')
@admin_bp.route('/admin/')
def admin_page():
    """Admin login page"""
    return send_from_directory('static', 'admin.html')

@admin_bp.route('/admin/dashboard')
@admin_bp.route('/admin/dashboard/')
def admin_dashboard():
    """Admin dashboard page (protected)"""
    if not session.get('admin_logged_in'):
        return redirect('/admin')
    return send_from_directory('static', 'admin-dashboard.html')

# Legacy routes (backward compatibility)
@admin_bp.route('/admin.html')
def admin_login_page_legacy():
    """Legacy admin login URL"""
    return redirect('/admin')

@admin_bp.route('/admin-dashboard.html')
def admin_dashboard_page_legacy():
    """Legacy dashboard URL"""
    return redirect('/admin/dashboard')

# ==========================================
# ADMIN API ENDPOINTS
# ==========================================

@admin_bp.route('/api/admin/login', methods=['POST'])
def admin_login():
    """Admin login endpoint with security"""
    client_ip = get_client_ip(request)
    
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        # Validate inputs
        if not username or not password:
            log_login_attempt(username or 'unknown', False, client_ip, 'Missing credentials')
            return jsonify({'error': 'Username and password required'}), 400
        
        # Validate username format
        is_valid, error_msg = validate_username(username)
        if not is_valid:
            log_login_attempt(username, False,client_ip, f'Invalid username format: {error_msg}')
            return jsonify({'error': 'Invalid username format'}), 400
        
        # Verify credentials
        user = admin_api.verify_admin_login(username, password, _cursor)
        
        if user:
            # Successful login
            session['admin_logged_in'] = True
            session['admin_user'] = user
            session.permanent = True
            
            # Update last login
            admin_api.update_last_login(user['id'], _cursor, _db_connection)
            
            # Log successful login
            log_login_attempt(username, True, client_ip)
            
            return jsonify({
                'status': 'success',
                'message': 'Login successful',
                'user': {'username': user['username']}
            })
        else:
            # Failed login
            log_login_attempt(username, False, client_ip, 'Invalid credentials')
            return jsonify({'error': 'Invalid credentials'}), 401
    
    except Exception as e:
        print(f"Error in admin login: {e}")
        import traceback
        traceback.print_exc()
        log_admin_action('system', 'LOGIN_ERROR', f"Error: {str(e)}", False)
        return jsonify({'error': 'Internal server error'}), 500

@admin_bp.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    """Admin logout endpoint"""
    username = session.get('admin_user', {}).get('username', 'unknown')
    log_logout(username, get_client_ip(request))
    session.clear()
    return jsonify({'status': 'success', 'message': 'Logged out'})

@admin_bp.route('/api/admin/check-auth', methods=['GET'])
def check_auth():
    """Check if admin is authenticated"""
    if session.get('admin_logged_in'):
        return jsonify({
            'authenticated': True,
            'user': session.get('admin_user', {})
        })
    return jsonify({'authenticated': False})

@admin_bp.route('/api/admin/stats', methods=['GET'])
@require_admin
def get_stats():
    """Get dashboard statistics"""
    try:
        stats = admin_api.get_stats(_cursor)
        return jsonify({'status': 'success', 'data': stats})
    except Exception as e:
        print(f"Error getting stats: {e}")
        return jsonify({'error': 'Failed to get stats'}), 500

@admin_bp.route('/api/admin/chat-logs', methods=['GET'])
@require_admin
def get_chat_logs():
    """Get chat logs with pagination"""
    try:
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        search = request.args.get('search', None)
        
        logs = admin_api.get_all_chat_logs(_cursor, limit, offset, search)
        return jsonify({'status': 'success', 'data': logs})
    except Exception as e:
        print(f"Error getting chat logs: {e}")
        return jsonify({'error': 'Failed to get chat logs'}), 500

@admin_bp.route('/api/admin/intents', methods=['GET'])
@require_admin
def get_intents():
    """Get all intents with patterns and responses"""
    try:
        intents = admin_api.get_all_intents_with_data(_cursor)
        return jsonify({'status': 'success', 'data': intents})
    except Exception as e:
        print(f"Error getting intents: {e}")
        return jsonify({'error': 'Failed to get intents'}), 500

@admin_bp.route('/api/admin/intents', methods=['POST'])
@require_admin
def create_intent():
    """Create new intent"""
    try:
        data = request.get_json()
        intent_name = data.get('intent_name')
        tag = data.get('tag')
        
        if not intent_name:
            return jsonify({'error': 'Intent name required'}), 400
        
        intent_id = admin_api.create_intent(_cursor, _db_connection, intent_name, tag)
        
        admin_user = session.get('admin_user', {}).get('username', 'unknown')
        log_admin_action(admin_user, 'CREATE_INTENT', f"Created intent: {intent_name}", True)
        
        return jsonify({'status': 'success', 'intent_id': intent_id})
    except Exception as e:
        print(f"Error creating intent: {e}")
        return jsonify({'error': 'Failed to create intent'}), 500

@admin_bp.route('/api/admin/intents/<int:intent_id>', methods=['PUT'])
@require_admin
def update_intent(intent_id):
    """Update intent"""
    try:
        data = request.get_json()
        intent_name = data.get('intent_name')
        tag = data.get('tag')
        
        success = admin_api.update_intent(_cursor, _db_connection, intent_id, intent_name, tag)
        
        admin_user = session.get('admin_user', {}).get('username', 'unknown')
        log_admin_action(admin_user, 'UPDATE_INTENT', f"Updated intent ID: {intent_id}", success)
        
        if success:
            return jsonify({'status': 'success'})
        return jsonify({'error': 'Intent not found'}), 404
    except Exception as e:
        print(f"Error updating intent: {e}")
        return jsonify({'error': 'Failed to update intent'}), 500

@admin_bp.route('/api/admin/intents/<int:intent_id>', methods=['DELETE'])
@require_admin
def delete_intent(intent_id):
    """Delete intent"""
    try:
        success = admin_api.delete_intent(_cursor, _db_connection, intent_id)
        
        admin_user = session.get('admin_user', {}).get('username', 'unknown')
        log_admin_action(admin_user, 'DELETE_INTENT', f"Deleted intent ID: {intent_id}", success)
        
        if success:
            return jsonify({'status': 'success'})
        return jsonify({'error': 'Intent not found'}), 404
    except Exception as e:
        print(f"Error deleting intent: {e}")
        return jsonify({'error': 'Failed to delete intent'}), 500

@admin_bp.route('/api/admin/intents/<int:intent_id>/patterns', methods=['POST'])
@require_admin
def add_pattern(intent_id):
    """Add pattern to intent"""
    try:
        data = request.get_json()
        pattern_text = data.get('pattern_text')
        
        if not pattern_text:
            return jsonify({'error': 'Pattern text required'}), 400
        
        pattern_id = admin_api.add_pattern(_cursor, _db_connection, intent_id, pattern_text)
        
        admin_user = session.get('admin_user', {}).get('username', 'unknown')
        log_admin_action(admin_user, 'ADD_PATTERN', f"Added pattern to intent ID: {intent_id}", True)
        
        return jsonify({'status': 'success', 'pattern_id': pattern_id})
    except Exception as e:
        print(f"Error adding pattern: {e}")
        return jsonify({'error': 'Failed to add pattern'}), 500

@admin_bp.route('/api/admin/patterns/<int:pattern_id>', methods=['DELETE'])
@require_admin
def delete_pattern(pattern_id):
    """Delete pattern"""
    try:
        success = admin_api.delete_pattern(_cursor, _db_connection, pattern_id)
        
        admin_user = session.get('admin_user', {}).get('username', 'unknown')
        log_admin_action(admin_user, 'DELETE_PATTERN', f"Deleted pattern ID: {pattern_id}", success)
        
        if success:
            return jsonify({'status': 'success'})
        return jsonify({'error': 'Pattern not found'}), 404
    except Exception as e:
        print(f"Error deleting pattern: {e}")
        return jsonify({'error': 'Failed to delete pattern'}), 500

@admin_bp.route('/api/admin/intents/<int:intent_id>/responses', methods=['POST'])
@require_admin
def add_response(intent_id):
    """Add response to intent"""
    try:
        data = request.get_json()
        response_text = data.get('response_text')
        
        if not response_text:
            return jsonify({'error': 'Response text required'}), 400
        
        response_id = admin_api.add_response(_cursor, _db_connection, intent_id, response_text)
        
        admin_user = session.get('admin_user', {}).get('username', 'unknown')
        log_admin_action(admin_user, 'ADD_RESPONSE', f"Added response to intent ID: {intent_id}", True)
        
        return jsonify({'status': 'success', 'response_id': response_id})
    except Exception as e:
        print(f"Error adding response: {e}")
        return jsonify({'error': 'Failed to add response'}), 500

@admin_bp.route('/api/admin/responses/<int:response_id>', methods=['DELETE'])
@require_admin
def delete_response(response_id):
    """Delete response"""
    try:
        success = admin_api.delete_response(_cursor, _db_connection, response_id)
        
        admin_user = session.get('admin_user', {}).get('username', 'unknown')
        log_admin_action(admin_user, 'DELETE_RESPONSE', f"Deleted response ID: {response_id}", success)
        
        if success:
            return jsonify({'status': 'success'})
        return jsonify({'error': 'Response not found'}), 404
    except Exception as e:
        print(f"Error deleting response: {e}")
        return jsonify({'error': 'Failed to delete response'}), 500
