"""
Application Configuration for Chatbot SI
-----------------------------------------
Centralized configuration management.
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
    
    # Security validation
    @classmethod
    def validate_security(cls):
        """Validate security configurations"""
        if isinstance(cls.SECRET_KEY, str) and 'change-this' in cls.SECRET_KEY.lower():
            import warnings
            warnings.warn(
                "[WARNING] You are using a default SECRET_KEY! "
                "Generate a secure key with: python -c \"from utils.security import generate_secret_key; print(generate_secret_key())\"",
                UserWarning
            )
            return False
        return True
    
    # Session Configuration
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = os.getenv('FLASK_ENV') == 'production'
    
    # Rate Limiting Configuration
    RATELIMIT_STORAGE_URL = os.getenv('RATELIMIT_STORAGE_URL', 'memory://')
    RATELIMIT_DEFAULT = "200 per hour"
    
    # Environment
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV != 'production'
    
    # CORS Configuration
    # Comma-separated list of allowed origins for production
    # Example: https://yourdomain.com,https://www.yourdomain.com
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '').split(',') if os.getenv('ALLOWED_ORIGINS') else []
    CORS_ORIGINS = ALLOWED_ORIGINS if FLASK_ENV == 'production' else '*'
    
    # Database Configuration (handled in core.database)
    DATABASE_URL = os.getenv('DATABASE_URL')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'chatbot_si')
    
    # Chatbot Configuration
    CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', '0.7'))
    ENABLE_GROQ = os.getenv('ENABLE_GROQ', 'true').lower() == 'true'
    ENABLE_CACHING = os.getenv('ENABLE_CACHING', 'true').lower() == 'true'
    ENABLE_TOPIC_FILTERING = os.getenv('ENABLE_TOPIC_FILTERING', 'true').lower() == 'true'
    FORCE_DATA_GROUNDED = os.getenv('FORCE_DATA_GROUNDED', 'true').lower() == 'true'
    ENABLE_RESPONSE_REPHRASING = os.getenv('ENABLE_RESPONSE_REPHRASING', 'true').lower() == 'true'
    ENABLE_MULTI_INTENT = os.getenv('ENABLE_MULTI_INTENT', 'true').lower() == 'true'
    
    # Groq API Configuration
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')
    GROQ_TEMPERATURE = float(os.getenv('GROQ_TEMPERATURE', '0.7'))
    GROQ_MAX_TOKENS = int(os.getenv('GROQ_MAX_TOKENS', '1024'))
    
    @staticmethod
    def init_app(app):
        """Initialize application with this configuration"""
        pass
