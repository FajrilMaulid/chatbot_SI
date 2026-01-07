from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
from chatbot_core import initialize_chatbot, get_bot_response
import os
from datetime import timedelta

app = Flask(__name__, static_folder='static')
app.secret_key = os.urandom(24)  # For session management
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

CORS(app)  # Enable CORS untuk development

# Inisialisasi chatbot saat aplikasi dimulai
print("Menginisialisasi chatbot...")
db_connection, cursor, model, responses_dict, knowledge_base = initialize_chatbot()

if model is None:
    print("ERROR: Gagal menginisialisasi chatbot. Periksa file JSON dan database.")
    exit(1)

print("Chatbot berhasil diinisialisasi!")

@app.route('/')
def index():
    """Serve halaman utama"""
    return send_from_directory('static', 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Endpoint API untuk menerima pesan dari user dan mengembalikan response bot
    Supports conversation history via session
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({
                'error': 'Message is required'
            }), 400
        
        # Get or initialize conversation history from session
        if 'conversation_history' not in session:
            session['conversation_history'] = []
        
        conversation_history = session['conversation_history']
        
        # Dapatkan response dari chatbot with conversation context
        bot_response = get_bot_response(
            user_message, 
            model, 
            responses_dict,
            knowledge_base,
            cursor, 
            db_connection,
            conversation_history
        )
        
        # Update conversation history (keep last 10 exchanges)
        conversation_history.append({
            'user': user_message,
            'bot': bot_response
        })
        
        # Keep only last 10 exchanges to prevent session overflow
        if len(conversation_history) > 10:
            conversation_history = conversation_history[-10:]
        
        session['conversation_history'] = conversation_history
        session.modified = True  # Mark session as modified
        
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

@app.route('/api/clear-history', methods=['POST'])
def clear_history():
    """
    Clear conversation history
    """
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

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    groq_status = "enabled" if os.getenv('ENABLE_GROQ', 'true').lower() == 'true' else "disabled"
    
    return jsonify({
        'status': 'healthy',
        'chatbot': 'ready',
        'groq': groq_status,
        'session': 'active' if 'conversation_history' in session else 'new'
    })

if __name__ == '__main__':
    # Get port from environment (for Railway, Render, etc.) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Check if running in production
    is_production = os.environ.get('FLASK_ENV', 'development') == 'production'
    
    print("\n" + "="*50)
    print("Chatbot SI Server")
    print("="*50)
    if is_production:
        print(f"Environment: PRODUCTION")
        print(f"Server running on port: {port}")
    else:
        print(f"Environment: DEVELOPMENT")
        print(f"Server berjalan di: http://localhost:{port}")
        print("Tekan Ctrl+C untuk menghentikan server")
    print("="*50 + "\n")
    
    app.run(
        debug=not is_production,  # Disable debug in production
        host='0.0.0.0', 
        port=port
    )

