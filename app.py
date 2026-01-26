"""
Chatbot SI - Main Application
------------------------------
Flask application with modular architecture.
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import os

# Import configuration
from config import Config

# Import core chatbot
from core import initialize_chatbot

# Import API blueprints
from api import chat_bp, admin_bp, init_chat_routes, init_admin_routes

# Import security utilities
from utils.logger import log_rate_limit_exceeded
from utils.security import get_client_ip

# ==========================================
# APP INITIALIZATION
# ==========================================

app = Flask(__name__, static_folder='static')
app.config.from_object(Config)

# Validate security configuration
Config.validate_security()

# Enable CORS with environment-aware configuration
if Config.CORS_ORIGINS == '*':
    # Development: Allow all origins
    CORS(app)
    print("[WARNING] CORS: Allowing all origins (development mode)")
else:
    # Production: Restrict to allowed origins
    CORS(app, origins=Config.CORS_ORIGINS)
    print(f"[OK] CORS: Restricted to {len(Config.CORS_ORIGINS)} allowed origin(s)")


# Security Headers (Talisman) - Only in production
if Config.FLASK_ENV == 'production':
    Talisman(app, 
             force_https=True,
             strict_transport_security=True,
             content_security_policy={
                 'default-src': "'self'",
                 'script-src': ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
                 'style-src': ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
                 'font-src': ["'self'", "https://fonts.gstatic.com"],
             })

# Rate Limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[Config.RATELIMIT_DEFAULT],
    storage_uri=Config.RATELIMIT_STORAGE_URL,
)

# Apply rate limits to blueprints
limiter.limit("30 per minute")(chat_bp.route('/api/chat', methods=['POST']))
limiter.limit("5 per 15 minutes")(admin_bp.route('/api/admin/login', methods=['POST']))

# Custom rate limit error handler
@app.errorhandler(429)
def ratelimit_handler(e):
    from flask import request, jsonify
    log_rate_limit_exceeded(get_client_ip(request), request.endpoint)
    return jsonify({
        'error': 'Rate limit exceeded. Please try again later.',
        'status': 'error'
    }), 429

# ==========================================
# CHATBOT INITIALIZATION
# ==========================================

print("="*60)
print("Initializing chatbot...")
print("="*60)

db_connection, cursor, model, responses_dict, knowledge_base = initialize_chatbot()

# Validate all critical components
initialization_failed = False
error_messages = []

if db_connection is None:
    error_messages.append("❌ Database connection failed")
    initialization_failed = True
else:
    print("✅ Database connection: OK")

if cursor is None:
    error_messages.append("❌ Database cursor failed")
    initialization_failed = True
else:
    print("✅ Database cursor: OK")

if model is None:
    error_messages.append("❌ ML model failed to load")
    initialization_failed = True
else:
    print("✅ ML model: OK")

if not responses_dict:
    error_messages.append("⚠️  Responses dictionary is empty")
    print("⚠️  Responses dictionary: EMPTY (warning)")

if not knowledge_base:
    error_messages.append("⚠️  Knowledge base is empty")
    print("⚠️  Knowledge base: EMPTY (warning)")

if initialization_failed:
    print("\n" + "="*60)
    print("INITIALIZATION FAILED")
    print("="*60)
    for msg in error_messages:
        print(msg)
    print("\n💡 TROUBLESHOOTING STEPS:")
    print("1. Check database credentials in .env file")
    print("2. Verify MySQL server is running")
    print("3. Ensure database 'chatbot_si' exists")
    print("4. Run: python scripts/migration_script.py")
    print("5. Check logs/app.log for details")
    print("="*60)
    exit(1)

print("="*60)
print("✅ Chatbot initialized successfully!")
print("="*60)

# Initialize blueprints with chatbot components
init_chat_routes(model, responses_dict, knowledge_base, cursor, db_connection)
init_admin_routes(cursor, db_connection)

# ==========================================
# REGISTER BLUEPRINTS
# ==========================================

app.register_blueprint(chat_bp)
app.register_blueprint(admin_bp)

# ==========================================
# MAIN ROUTES
# ==========================================

@app.route('/')
def index():
    """Serve main chatbot page"""
    return send_from_directory('static', 'index.html')

# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = Config.DEBUG
    
    print(f"\n{'='*50}")
    print(f"Starting Chatbot SI on port {port}")
    print(f"Debug mode: {debug}")
    print(f"Environment: {Config.FLASK_ENV}")
    print(f"{'='*50}\n")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
