# API package initialization
from .chat_routes import chat_bp, init_chat_routes
from .admin_routes import admin_bp, init_admin_routes

__all__ = ['chat_bp', 'admin_bp', 'init_chat_routes', 'init_admin_routes']
