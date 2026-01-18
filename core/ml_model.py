"""
ML Model Module for Chatbot SI
-------------------------------
Handles machine learning model training and intent prediction.
"""

import numpy as np
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline

def train_chatbot_model(data):
    """
    Train ML model for intent classification.
    
    Args:
        data: Dictionary containing intents data from JSON
    
    Returns:
        tuple: (model, responses_dict, knowledge_base) or (None, None, None) if failed
    """
    if 'intents' not in data:
        print("[ERROR] Format JSON salah. Harusnya memiliki key 'intents'.")
        return None, None, None

    X_train = []
    y_train = []
    responses_dict = {}
    knowledge_base = []

    print("[...] Mulai training model...")
    for intent_data in data['intents']:
        intent_name = intent_data['intent']

        if intent_name not in responses_dict:
            responses_dict[intent_name] = intent_data['responses']
            # Build knowledge base summary for Groq
            knowledge_base.append({
                'intent': intent_name,
                'patterns': intent_data['patterns'][:3],  # Sample patterns
                'responses': intent_data['responses'][:1]  # Sample response
            })

        for pattern in intent_data['patterns']:
            X_train.append(pattern.lower())
            y_train.append(intent_name)

    if not X_train:
        print("[ERROR] Tidak ada data training ditemukan di file JSON.")
        return None, None, None

    model = make_pipeline(TfidfVectorizer(), SVC(kernel='linear', probability=True))
    model.fit(X_train, y_train)

    print("[OK] Training model selesai.")
    return model, responses_dict, knowledge_base

def find_best_matching_intent(user_input, model, responses_dict, knowledge_base):
    """
    Find best matching intent from data model.
    
    Args:
        user_input: User's question
        model: Trained ML model
        responses_dict: Dictionary of responses per intent
        knowledge_base: Knowledge base for context
    
    Returns:
        tuple: (intent, confidence, response_from_data, all_responses)
    """
    user_input_low = user_input.lower()
    
    # Get ML prediction
    probabilities = model.predict_proba([user_input_low])[0]
    max_prob = np.max(probabilities)
    intent_index = np.argmax(probabilities)
    intent = model.classes_[intent_index]
    
    # Get all possible responses for this intent
    all_responses = responses_dict.get(intent, [])
    
    # Pick one response randomly
    if all_responses:
        response_from_data = random.choice(all_responses)
    else:
        response_from_data = None
    
    print(f" Intent: '{intent}' | Confidence: {max_prob:.2%}")
    
    return intent, max_prob, response_from_data, all_responses
