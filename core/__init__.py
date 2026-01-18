"""
Core Module Initialization for Chatbot SI
------------------------------------------
Initializes chatbot components and exports main functions.
"""

import os
from .database import init_db_connection, load_chat_data_from_json
from .ml_model import train_chatbot_model
from .response_handler import get_bot_response
from .groq_client import groq_client

def initialize_chatbot():
    """
    Initialize chatbot: connect to database and train ML model.
    
    Returns:
        tuple: (db_connection, cursor, model, responses_dict, knowledge_base)
    """
    print("\n" + "=" * 50)
    print("Initializing Chatbot SI...")
    print("=" * 50)
    
    # Connect to database
    db_connection = init_db_connection()
    cursor = None
    
    if db_connection is not None:
        cursor = db_connection.cursor()
    
    # Load and train model
    chat_data = load_chat_data_from_json('data/intents_ml.json')
    
    if chat_data:
        model, responses_dict, knowledge_base = train_chatbot_model(chat_data)
    else:
        model, responses_dict, knowledge_base = None, None, None
    
    # Check if model successfully trained
    if model is None:
        print("[ERROR] Chatbot tidak dapat diinisialisasi.")
        return None, None, None, None, None
    
    # Configuration summary
    print("=" * 50)
    print("[OK] Chatbot initialization complete!")
    print(f"[OK] Local ML: Ready")
    print(f"[OK] Groq API: {'Enabled' if groq_client else 'Disabled'}")
    print(f"[OK] Caching: {os.getenv('ENABLE_CACHING', 'true')}")
    print(f"[OK] Topic Filtering: {os.getenv('ENABLE_TOPIC_FILTERING', 'true')}")
    print(f"[OK] Data-Grounded Mode: {os.getenv('FORCE_DATA_GROUNDED', 'true')}")
    print(f"[OK] Response Rephrasing: {os.getenv('ENABLE_RESPONSE_REPHRASING', 'true')}")
    print(f"[OK] Confidence Threshold: {os.getenv('CONFIDENCE_THRESHOLD', '0.7')}")
    print("=" * 50 + "\n")
    
    return db_connection, cursor, model, responses_dict, knowledge_base

# Export main functions
__all__ = [
    'initialize_chatbot',
    'get_bot_response',
    'groq_client'
]
