"""
Validation Utilities for Chatbot SI
------------------------------------
Input validation and sanitization functions to prevent injection attacks.
"""

import re
from html import escape

# Validation patterns
USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_]{3,50}$')
INTENT_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9_\-]{3,100}$')
SAFE_TEXT_PATTERN = re.compile(r'^[a-zA-Z0-9\s\-_.,!?()]+$')

def validate_username(username):
    """
    Validate username format.
    
    Rules:
    - 3-50 characters
    - Alphanumeric and underscore only
    - No spaces or special characters
    
    Args:
        username: String to validate
    
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if not username:
        return False, "Username is required"
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    
    if len(username) > 50:
        return False, "Username must be less than 50 characters"
    
    if not USERNAME_PATTERN.match(username):
        return False, "Username can only contain letters, numbers, and underscores"
    
    return True, None

def validate_password(password):
    """
    Validate password format.
    
    Rules:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    
    Args:
        password: String to validate
    
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if len(password) > 128:
        return False, "Password is too long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    return True, None

def validate_intent_name(intent_name):
    """
    Validate intent name format.
    
    Args:
        intent_name: String to validate
    
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if not intent_name:
        return False, "Intent name is required"
    
    if len(intent_name) < 3:
        return False, "Intent name must be at least 3 characters"
    
    if len(intent_name) > 100:
        return False, "Intent name must be less than 100 characters"
    
    if not INTENT_NAME_PATTERN.match(intent_name):
        return False, "Intent name can only contain letters, numbers, hyphens, and underscores"
    
    return True, None

def validate_text_input(text, field_name="Text", min_length=1, max_length=5000):
    """
    Validate general text input.
    
    Args:
        text: String to validate
        field_name: Name of field for error messages
        min_length: Minimum length
        max_length: Maximum length
    
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if not text:
        return False, f"{field_name} is required"
    
    if len(text) < min_length:
        return False, f"{field_name} must be at least {min_length} characters"
    
    if len(text) > max_length:
        return False, f"{field_name} must be less than {max_length} characters"
    
    return True, None

def sanitize_html(text):
    """
    Sanitize HTML to prevent XSS attacks.
    
    Args:
        text: String to sanitize
    
    Returns:
        str: Sanitized text with HTML entities escaped
    """
    if not text:
        return ""
    
    return escape(str(text))

def sanitize_sql_pattern(text):
    """
    Basic SQL injection pattern detection (defense in depth).
    Note: We use parameterized queries, but this adds extra layer.
    
    Args:
        text: String to check
    
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Remove common SQL injection patterns
    dangerous_patterns = [
        r'(\bSELECT\b|\bUNION\b|\bINSERT\b|\bUPDATE\b|\bDELETE\b|\bDROP\b)',
        r'(--|\#|\/\*|\*\/)',
        r'(\bOR\b\s+\d+\s*=\s*\d+)',
        r'(\bAND\b\s+\d+\s*=\s*\d+)'
    ]
    
    cleaned = text
    for pattern in dangerous_patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    
    return cleaned.strip()

def validate_and_sanitize(text, field_name="Input", max_length=5000):
    """
    Comprehensive validation and sanitization.
    
    Args:
        text: String to validate and sanitize
        field_name: Name of field
        max_length: Maximum allowed length
    
    Returns:
        tuple: (sanitized_text: str or None, error_message: str or None)
    """
    # Validate
    is_valid, error = validate_text_input(text, field_name, max_length=max_length)
    if not is_valid:
        return None, error
    
    # Sanitize
    sanitized = sanitize_html(text)
    sanitized = sanitize_sql_pattern(sanitized)
    
    return sanitized, None

def validate_email(email):
    """
    Validate email format (basic check).
    
    Args:
        email: Email string to validate
    
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if not email:
        return False, "Email is required"
    
    # Basic email pattern
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    if not email_pattern.match(email):
        return False, "Invalid email format"
    
    if len(email) > 255:
        return False, "Email is too long"
    
    return True, None
