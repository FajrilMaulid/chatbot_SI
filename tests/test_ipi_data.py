"""
Quick test untuk memverifikasi data model IPI Garut
"""

from chatbot_core import initialize_chatbot, get_bot_response

def test_ipi_questions():
    print("\n=== Testing IPI Garut Data Model ===\n")
    
    # Initialize
    db_connection, cursor, model, responses_dict, knowledge_base = initialize_chatbot()
    
    if model is None:
        print("[ERROR] Initialization failed!")
        return
    
    # Test questions
    test_cases = [
        "halo",
        "apa itu ipi?",
        "ipi di mana?",
        "lokasi kampus ipi",
        "biaya kuliah si berapa?",
        "cara daftar ke prodi si?",
        "kantor prodi si dimana?"
    ]
    
    for question in test_cases:
        print(f"\n[?] Pertanyaan: \"{question}\"")
        response = get_bot_response(
            question, 
            model, 
            responses_dict, 
            knowledge_base, 
            cursor, 
            db_connection
        )
        print(f"[*] Jawaban:")
        print(f"    {response}")
        print("-" * 70)
    
    # Close connections
    if cursor:
        cursor.close()
    if db_connection:
        db_connection.close()
    
    print("\n[OK] Test completed!\n")

if __name__ == "__main__":
    test_ipi_questions()
