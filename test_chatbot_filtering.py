"""
Test script untuk memverifikasi chatbot yang telah ditingkatkan
- Topic Filtering: Menolak pertanyaan di luar topik SI
- Data-Grounded: Semua jawaban berdasarkan intents_ml.json
- Natural Rephrasing: Jawaban lebih conversational
"""

from chatbot_core import initialize_chatbot, get_bot_response
import time

def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")

def test_question(question, db_connection, cursor, model, responses_dict, knowledge_base, expected_behavior):
    print(f"[?] Pertanyaan: \"{question}\"")
    print(f"[i] Ekspektasi: {expected_behavior}")
    print()
    
    response = get_bot_response(
        question, 
        model, 
        responses_dict, 
        knowledge_base, 
        cursor, 
        db_connection
    )
    
    print(f"\n[*] Jawaban Bot:")
    print(f"   {response}")
    print("\n" + "-" * 60 + "\n")
    time.sleep(1)  # Small delay for readability

def main():
    print("\n=== CHATBOT SI - TEST SUITE ===")
    print("Testing: Topic Filtering + Data-Grounded Responses")
    
    # Initialize chatbot
    db_connection, cursor, model, responses_dict, knowledge_base = initialize_chatbot()
    
    if model is None:
        print("[ERROR] Chatbot initialization failed!")
        return
    
    # ========== TEST 1: SI-Related Questions (Should be answered) ==========
    print_section("TEST 1: Pertanyaan Relevan SI (Harus Dijawab)")
    
    si_questions = [
        ("halo", "Sapaan - harus dijawab dengan ramah"),
        ("apa itu sistem informasi?", "Definisi SI - jawaban dari data model"),
        ("biaya kuliah si berapa?", "Info biaya - jawaban dari data model"),
        ("lulusan si kerja jadi apa?", "Prospek kerja - jawaban dari data model"),
        ("siapa kaprodi si?", "Info kaprodi - jawaban dari data model"),
        ("belajar coding di si?", "Info mata kuliah - jawaban dari data model"),
    ]
    
    for question, expectation in si_questions:
        test_question(
            question, 
            db_connection, 
            cursor, 
            model, 
            responses_dict, 
            knowledge_base,
            expectation
        )
    
    # ========== TEST 2: Off-Topic Questions (Should be rejected) ==========
    print_section("TEST 2: Pertanyaan Di Luar Topik (Harus Ditolak)")
    
    offtopic_questions = [
        ("siapa presiden indonesia?", "Pertanyaan politik - harus ditolak"),
        ("cuaca hari ini bagaimana?", "Pertanyaan cuaca - harus ditolak"),
        ("resep nasi goreng", "Pertanyaan kuliner - harus ditolak"),
        ("cara buat website dengan react?", "Pertanyaan teknis umum - harus ditolak (bukan konteks SI)"),
        ("siapa juara piala dunia 2022?", "Pertanyaan olahraga - harus ditolak"),
    ]
    
    for question, expectation in offtopic_questions:
        test_question(
            question, 
            db_connection, 
            cursor, 
            model, 
            responses_dict, 
            knowledge_base,
            expectation
        )
    
    # ========== TEST 3: Borderline Questions (Context dependent) ==========
    print_section("TEST 3: Pertanyaan Borderline (Tergantung Konteks)")
    
    borderline_questions = [
        ("belajar python?", "Borderline - harus dijawab dalam konteks SI jika ada di data"),
        ("ada mata kuliah database?", "Borderline - harus dijawab dalam konteks SI"),
    ]
    
    for question, expectation in borderline_questions:
        test_question(
            question, 
            db_connection, 
            cursor, 
            model, 
            responses_dict, 
            knowledge_base,
            expectation
        )
    
    # Close connections
    if cursor:
        cursor.close()
    if db_connection:
        db_connection.close()
    
    print_section("TEST SELESAI")
    print("[OK] Silakan review hasil di atas untuk memverifikasi:")
    print("   1. Pertanyaan SI dijawab dengan baik dan natural")
    print("   2. Pertanyaan off-topic ditolak dengan sopan")
    print("   3. Semua jawaban berdasarkan data model")
    print()

if __name__ == "__main__":
    main()
