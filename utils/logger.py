"""
Security Logger for Chatbot SI
-------------------------------
Logging utility for security events and admin actions.
"""

import logging
import os
from datetime import datetime
from functools import wraps

# Ensure logs directory exists
LOGS_DIR = 'logs'
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Configure loggers
def setup_logger(name, log_file, level=logging.INFO):
    """Setup a logger with file handler"""
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    handler = logging.FileHandler(log_file, encoding='utf-8')
    handler.setFormatter(formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger

# Security logger
security_logger = setup_logger('security', os.path.join(LOGS_DIR, 'security.log'))

# Admin actions logger
admin_logger = setup_logger('admin', os.path.join(LOGS_DIR, 'admin_actions.log'))

# Application logger
app_logger = setup_logger('app', os.path.join(LOGS_DIR, 'app.log'))

def log_login_attempt(username, success, ip_address=None, reason=None):
    """
    Log login attempt.
    
    Args:
        username: Username attempting login
        success: Boolean indicating if login was successful
        ip_address: IP address of requester
        reason: Failure reason if applicable
    """
    status = "SUCCESS" if success else "FAILED"
    message = f"Login {status} - User: {username}"
    
    if ip_address:
        message += f" - IP: {ip_address}"
    
    if not success and reason:
        message += f" - Reason: {reason}"
    
    if success:
        security_logger.info(message)
    else:
        security_logger.warning(message)

def log_logout(username, ip_address=None):
    """Log logout event"""
    message = f"Logout - User: {username}"
    if ip_address:
        message += f" - IP: {ip_address}"
    security_logger.info(message)

def log_admin_action(admin_username, action, details, success=True):
    """
    Log admin action.
    
    Args:
        admin_username: Admin performing action
        action: Action being performed (e.g., 'CREATE_INTENT', 'DELETE_PATTERN')
        details: Action details
        success: Whether action succeeded
    """
    status = "SUCCESS" if success else "FAILED"
    message = f"{action} - {status} - Admin: {admin_username} - Details: {details}"
    
    if success:
        admin_logger.info(message)
    else:
        admin_logger.error(message)

def log_security_event(event_type, details, severity='WARNING'):
    """
    Log security event.
    
    Args:
        event_type: Type of security event
        details: Event details
        severity: Log level (INFO, WARNING, ERROR, CRITICAL)
    """
    message = f"{event_type} - {details}"
    
    if severity == 'INFO':
        security_logger.info(message)
    elif severity == 'WARNING':
        security_logger.warning(message)
    elif severity == 'ERROR':
        security_logger.error(message)
    elif severity == 'CRITICAL':
        security_logger.critical(message)

def log_rate_limit_exceeded(ip_address, endpoint):
    """Log rate limit exceeded event"""
    log_security_event(
        'RATE_LIMIT_EXCEEDED',
        f"IP: {ip_address} - Endpoint: {endpoint}",
        severity='WARNING'
    )

def log_invalid_input(field, value, ip_address=None):
    """Log invalid input attempt"""
    details = f"Field: {field} - Value: {value[:50]}..."  # Truncate value
    if ip_address:
        details += f" - IP: {ip_address}"
    log_security_event('INVALID_INPUT', details, severity='WARNING')

def log_unauthorized_access(ip_address, endpoint):
    """Log unauthorized access attempt"""
    log_security_event(
        'UNAUTHORIZED_ACCESS',
        f"IP: {ip_address} - Endpoint: {endpoint}",
        severity='WARNING'
    )

# Decorator for logging function calls
def log_function_call(logger=app_logger):
    """
    Decorator to log function calls.
    
    Usage:
        @log_function_call()
        def my_function():
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Calling {func.__name__}")
            try:
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} completed successfully")
                return result
            except Exception as e:
                logger.error(f"{func.__name__} failed: {str(e)}")
                raise
        return wrapper
    return decorator
