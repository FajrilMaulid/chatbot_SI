"""
Test multi-intent question handling
"""

from chatbot_core import initialize_chatbot, get_bot_response

def test_multi_intent():
    print("\n=== Testing Multi-Intent Question Handling ===\n")
    
    # Initialize
    db_connection, cursor, model, responses_dict, knowledge_base = initialize_chatbot()
    
    if model is None:
        print("[ERROR] Initialization failed!")
        return
    
    # Test cases
    test_cases = [
        # Multi-intent questions
        ("apa itu sistem informasi ipi garut dan siapa kaprodi nya", "MULTI-INTENT: SI definition + IPI + Kaprodi"),
        ("biaya kuliah berapa dan dimana lokasi kampus?", "MULTI-INTENT: Biaya + Lokasi"),
        ("prospek kerja apa saja dan berapa lama kuliah?", "MULTI-INTENT: Prospek + Lama studi"),
        
        # Single intent (should work as before)
        ("apa itu sistem informasi?", "SINGLE: SI definition"),
        ("siapa kaprodi?", "SINGLE: Kaprodi"),
    ]
    
    for question, description in test_cases:
        print(f"\n{'='*70}")
        print(f"[?] Pertanyaan: \"{question}\"")
        print(f"[i] Expected: {description}")
        print(f"{'='*70}\n")
        
        response = get_bot_response(
            question, 
            model, 
            responses_dict, 
            knowledge_base, 
            cursor, 
            db_connection
        )
        
        print(f"\n[*] Jawaban:")
        print(f"    {response}")
        print("\n" + "="*70 + "\n")
        
        import time
        time.sleep(2)  # Delay for readability
    
    # Close connections
    if cursor:
        cursor.close()
    if db_connection:
        db_connection.close()
    
    print("\n[OK] Multi-intent test completed!\n")

if __name__ == "__main__":
    test_multi_intent()
