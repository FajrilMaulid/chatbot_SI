"""
Security Utilities for Chatbot SI
----------------------------------
Password strength validation, sanitization, and other security functions.
"""

import re
import hashlib
import os
import secrets
from werkzeug.security import generate_password_hash, check_password_hash

def generate_secret_key(length=32):
    """
    Generate a cryptographically secure random SECRET_KEY for Flask.
    
    Args:
        length: Length of the key in bytes (default 32 = 64 hex characters)
    
    Returns:
        str: Cryptographically secure random hex string
    
    Example:
        >>> key = generate_secret_key()
        >>> len(key)
        64
    """
    return secrets.token_hex(length)

def check_password_strength(password):
    """
    Check password strength and return score with feedback.
    
    Args:
        password: Password string to check
    
    Returns:
        dict: {
            'score': int (0-5),
            'strength': str ('very_weak', 'weak', 'fair', 'good', 'strong'),
            'feedback': list of improvement suggestions
        }
    """
    score = 0
    feedback = []
    
    # Length check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters")
    
    if len(password) >= 12:
        score += 1
    
    # Uppercase check
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Include uppercase letters")
    
    # Lowercase check
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Include lowercase letters")
    
    # Digit check
    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("Include numbers")
    
    # Special character check
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
        feedback = [f for f in feedback if f != "Include special characters"]
    else:
        if score >= 3:  # Only suggest if other criteria met
            feedback.append("Include special characters for extra strength")
    
    # Check for common patterns
    common_patterns = ['123456', 'password', 'qwerty', 'abc123', '111111']
    if any(pattern in password.lower() for pattern in common_patterns):
        score = max(0, score - 2)
        feedback.append("Avoid common patterns")
    
    # Determine strength
    strength_map = {
        0: 'very_weak',
        1: 'very_weak',
        2: 'weak',
        3: 'fair',
        4: 'good',
        5: 'strong',
        6: 'strong'
    }
    
    strength = strength_map.get(score, 'very_weak')
    
    return {
        'score': min(score, 5),
        'strength': strength,
        'feedback': feedback
    }

def hash_password(password):
    """
    Hash password using werkzeug's secure method.
    
    Args:
        password: Plain text password
    
    Returns:
        str: Hashed password
    """
    return generate_password_hash(password, method='pbkdf2:sha256')

def verify_password(password, password_hash):
    """
    Verify password against hash.
    
    Args:
        password: Plain text password
        password_hash: Hashed password to compare against
    
    Returns:
        bool: True if password matches
    """
    return check_password_hash(password_hash, password)

def generate_token(length=32):
    """
    Generate a random token for CSRF or session management.
    
    Args:
        length: Token length
    
    Returns:
        str: Hexadecimal token
    """
    return secrets.token_hex(length)

def sanitize_filename(filename):
    """
    Sanitize filename to prevent directory traversal.
    
    Args:
        filename: Original filename
    
    Returns:
        str: Sanitized filename
    """
    # Remove directory components
    filename = os.path.basename(filename)
    
    # Remove dangerous characters
    filename = re.sub(r'[^\w\s\-.]', '', filename)
    
    # Limit length
    if len(filename) > 255:
        filename = filename[:255]
    
    return filename

def is_safe_redirect_url(url, allowed_hosts=None):
    """
    Check if URL is safe for redirect (prevent open redirect vulnerability).
    
    Args:
        url: URL to check
        allowed_hosts: List of allowed hostnames
    
    Returns:
        bool: True if URL is safe
    """
    if not url:
        return False
    
    # Only allow relative URLs or URLs to allowed hosts
    if url.startswith('/'):
        return True
    
    if allowed_hosts:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc in allowed_hosts
    
    return False

def get_client_ip(request):
    """
    Get client IP address from request, considering proxies.
    
    Args:
        request: Flask request object
    
    Returns:
        str: Client IP address
    """
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        # Behind proxy
        ip = request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
    else:
        ip = request.environ.get('REMOTE_ADDR', 'Unknown')
    
    return ip
