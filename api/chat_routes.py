"""
Chat API Routes Blueprint
--------------------------
Handles chatbot conversation endpoints.
"""

from flask import Blueprint, request, jsonify, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from core import get_bot_response, groq_client

# Create blueprint
chat_bp = Blueprint('chat', __name__)

# Shared chatbot components (will be injected from app.py)
_model = None
_responses_dict = None
_knowledge_base = None
_cursor = None
_db_connection = None

def init_chat_routes(model, responses_dict, knowledge_base, cursor, db_connection):
    """Initialize chat routes with chatbot components"""
    global _model, _responses_dict, _knowledge_base, _cursor, _db_connection
    _model = model
    _responses_dict = responses_dict
    _knowledge_base = knowledge_base
    _cursor = cursor
    _db_connection = db_connection

@chat_bp.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint.
    Receives user message and returns bot response with conversation history support.
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({
                'error': 'Message is required',
                'status': 'error'
            }), 400
        
        # Get conversation history from session
        conversation_history = session.get('conversation_history', [])
        
        # Get bot response using chatbot core
        bot_response = get_bot_response(
            user_message,
            _model,
            _responses_dict,
            _knowledge_base,
            _cursor,
            _db_connection,
            conversation_history=conversation_history,
            groq_client=groq_client
        )
        
        # Update conversation history
        conversation_history.append({
            'user': user_message,
            'bot': bot_response
        })
        
        # Keep only last 10 messages
        if len(conversation_history) > 10:
            conversation_history = conversation_history[-10:]
        
        session['conversation_history'] = conversation_history
        session.modified = True
        
        return jsonify({
            'response': bot_response,
            'status': 'success'
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Internal server error',
            'status': 'error'
        }), 500

@chat_bp.route('/api/clear-history', methods=['POST'])
def clear_history():
    """Clear conversation history"""
    try:
        session['conversation_history'] = []
        session.modified = True
        return jsonify({
            'status': 'success',
            'message': 'Conversation history cleared'
        })
    except Exception as e:
        print(f"Error clearing history: {e}")
        return jsonify({
            'error': 'Failed to clear history',
            'status': 'error'
        }), 500

@chat_bp.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'chatbot': 'ready',
        'groq': 'enabled' if groq_client else 'disabled',
        'session': 'active' if 'conversation_history' in session else 'new'
    })
