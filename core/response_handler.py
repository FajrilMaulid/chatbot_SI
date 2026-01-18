"""
Response Handler Module for Chatbot SI
---------------------------------------
Main orchestration logic for generating bot responses using multi-stage pipeline.
"""

import os
import hashlib
from dotenv import load_dotenv
from cachetools import TTLCache

from .database import save_chat_to_database
from .ml_model import find_best_matching_intent
from .groq_client import (
    is_groq_available,
    rephrase_response_naturally,
    combine_multi_intent_answers,
    GROQ_MODEL
)
from .filters import is_topic_relevant, detect_multi_intent

# Load environment variables
load_dotenv()

# Configuration
CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', '0.7'))
ENABLE_CACHING = os.getenv('ENABLE_CACHING', 'true').lower() == 'true'
CACHE_TTL = int(os.getenv('CACHE_TTL', '3600'))
FORCE_DATA_GROUNDED = os.getenv('FORCE_DATA_GROUNDED', 'true').lower() == 'true'
ENABLE_RESPONSE_REPHRASING = os.getenv('ENABLE_RESPONSE_REPHRASING', 'true').lower() == 'true'

# Response cache (TTL = 1 hour by default)
response_cache = TTLCache(maxsize=100, ttl=CACHE_TTL) if ENABLE_CACHING else None

def get_cache_key(text):
    """Generate cache key from text"""
    return hashlib.md5(text.lower().strip().encode()).hexdigest()

def answer_multi_intent(sub_questions, model, responses_dict, knowledge_base, conversation_history=None):
    """
    Answer multiple sub-questions and combine into one natural response.
    
    Args:
        sub_questions: List of sub-questions
        model: ML model
        responses_dict: Responses dictionary
        knowledge_base: Knowledge base
        conversation_history: Previous messages
    
    Returns:
        str: Combined natural response or None
    """
    if not sub_questions:
        return None
    
    print(f"[MULTI-INTENT] Detected {len(sub_questions)} sub-questions")
    
    # Collect answers for each sub-question
    qa_pairs = []
    
    for i, sub_q in enumerate(sub_questions, 1):
        print(f"  [{i}] Sub-question: '{sub_q}'")
        
        # Find best matching intent from data model
        intent, confidence, data_response, all_responses = find_best_matching_intent(
            sub_q, model, responses_dict, knowledge_base
        )
        
        if data_response:
            qa_pairs.append({
                'question': sub_q,
                'intent': intent,
                'answer': data_response,
                'confidence': confidence
            })
            print(f"      Intent: '{intent}' (confidence: {confidence:.2%})")
        else:
            print(f"      [WARN] No data found for intent: {intent}")
    
    if not qa_pairs:
        return None
    
    # Combine all answers using Groq
    combined_response = combine_multi_intent_answers(qa_pairs)
    print(f"[MULTI-INTENT] Combined response generated")
    return combined_response

def get_bot_response(user_input, model, responses_dict, knowledge_base, cursor, db_connection, 
                    conversation_history=None, groq_client=None):
    """
    Multi-Stage Data-Grounded Response System:
    Stage 0: Multi-Intent Detection - Check if question has multiple intents
    Stage 1: Topic Filtering - Check if question is SI-related
    Stage 2: Intent Matching - Find best match from data model
    Stage 3: Natural Rephrasing - Make response conversational
    
    Args:
        user_input: User's message
        model: Trained ML model
        responses_dict: Dictionary of responses
        knowledge_base: Knowledge base
        cursor: Database cursor
        db_connection: Database connection
        conversation_history: Previous messages
        groq_client: Groq client instance
    
    Returns:
        str: Bot's response
    """
    bot_response = None
    source = "unknown"
    
    # Check cache first
    if ENABLE_CACHING and response_cache is not None:
        cache_key = get_cache_key(user_input)
        if cache_key in response_cache:
            print("[CACHE HIT]")
            cached_response = response_cache[cache_key]
            if cursor and db_connection:
                save_chat_to_database(cursor, db_connection, user_input, cached_response['response'], cached_response['source'])
            return cached_response['response']
    
    print("-" * 50)
    print(f" Input: '{user_input}'")
    
    # STAGE 0: Multi-Intent Detection
    is_multi, sub_questions = detect_multi_intent(user_input, groq_client, GROQ_MODEL)
    
    if is_multi and sub_questions:
        print(f"[MULTI-INTENT] Compound question detected with {len(sub_questions)} sub-questions")
        
        # Answer multi-intent question
        combined_answer = answer_multi_intent(
            sub_questions, model, responses_dict, knowledge_base, conversation_history
        )
        
        if combined_answer:
            bot_response = combined_answer
            source = "multi-intent"
            print(f"[OK] Multi-intent response generated")
        else:
            # Fallback to single intent if multi-intent fails
            print(f"[WARN] Multi-intent failed, falling back to single intent")
            is_multi = False
    
    # STAGE 1-3: Single Intent Processing (only if not multi-intent)
    if not (is_multi and bot_response):
        # STAGE 1: Topic Filtering
        is_relevant, filter_reason = is_topic_relevant(user_input, groq_client, GROQ_MODEL)
        
        if not is_relevant:
            # Reject off-topic questions politely
            bot_response = f"Maaf, saya adalah chatbot khusus untuk Program Studi Sistem Informasi. Pertanyaan Anda sepertinya di luar topik yang bisa saya bantu. Saya hanya bisa menjawab pertanyaan seputar prodi SI, seperti mata kuliah, prospek kerja, dosen, biaya kuliah, dan informasi akademik lainnya. Ada yang bisa saya bantu tentang prodi SI?"
            source = "filtered-out"
            print(f"[FILTERED] Topic not relevant: {filter_reason}")
        else:
            print(f"[OK] Topic relevant: {filter_reason}")
            
            # STAGE 2: Find Best Intent from Data Model
            intent, confidence, data_response, all_responses = find_best_matching_intent(
                user_input, model, responses_dict, knowledge_base
            )
            
            if data_response is None:
                # No response found in data model
                bot_response = "Maaf, saya tidak memiliki informasi spesifik untuk pertanyaan itu. Bisa coba tanyakan dengan cara lain atau hubungi sekretariat prodi untuk informasi lebih lanjut."
                source = "no-data"
                print(f"[WARN] No data found for intent: {intent}")
            else:
                # STAGE 3: Rephrase Naturally (if enabled and conditions met)
                if FORCE_DATA_GROUNDED and ENABLE_RESPONSE_REPHRASING:
                    # Always use data model + rephrase for natural tone
                    print(f"[...] Rephrasing response naturally...")
                    bot_response = rephrase_response_naturally(
                        user_input, data_response, intent, all_responses, conversation_history
                    )
                    source = "data-grounded-rephrased"
                    print(f"[OK] Using data-grounded rephrased response")
                elif confidence > CONFIDENCE_THRESHOLD:
                    # High confidence - use data as-is
                    bot_response = data_response
                    source = "data-grounded"
                    print(f"[OK] Using data model directly (confidence: {confidence:.2%})")
                else:
                    # Low confidence - try to rephrase if possible, otherwise use fallback
                    if ENABLE_RESPONSE_REPHRASING and is_groq_available():
                        print(f"[WARN] Low confidence ({confidence:.2%}), using rephrasing...")
                        bot_response = rephrase_response_naturally(
                            user_input, data_response, intent, all_responses, conversation_history
                        )
                        source = "data-grounded-low-conf"
                    else:
                        # Use data response even with low confidence
                        bot_response = data_response
                        source = "data-grounded-low"
                        print(f"[WARN] Low confidence ({confidence:.2%}) but using data anyway")
    
    # Cache the response
    if ENABLE_CACHING and response_cache is not None and bot_response:
        cache_key = get_cache_key(user_input)
        response_cache[cache_key] = {
            'response': bot_response,
            'source': source
        }
    
    # Save to database
    if cursor and db_connection:
        save_chat_to_database(cursor, db_connection, user_input, bot_response, source)
    
    print(f" Source: {source}")
    print("-" * 50)
    
    return bot_response
