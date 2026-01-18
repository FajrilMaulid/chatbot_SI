"""
Groq Client Module for Chatbot SI
----------------------------------
Handles Groq API integration for natural language generation.
"""

import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Groq Configuration
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')
GROQ_TEMPERATURE = float(os.getenv('GROQ_TEMPERATURE', '0.7'))
GROQ_MAX_TOKENS = int(os.getenv('GROQ_MAX_TOKENS', '1024'))
ENABLE_GROQ = os.getenv('ENABLE_GROQ', 'true').lower() == 'true'

# Initialize Groq client
groq_client = None
if ENABLE_GROQ and GROQ_API_KEY:
    try:
        groq_client = Groq(api_key=GROQ_API_KEY)
        print(f"[OK] Groq API initialized successfully")
        print(f"[OK] Model: {GROQ_MODEL}")
    except Exception as e:
        print(f"[WARN] Groq initialization failed: {e}")
        print("[WARN] Chatbot will work with local ML only")

def is_groq_available():
    """Check if Groq client is available"""
    return groq_client is not None

def rephrase_response_naturally(user_input, data_response, intent, all_responses, conversation_history=None):
    """
    Rephrase the data model response to be more natural while staying grounded.
    
    Args:
        user_input: User's question
        data_response: Original response from data
        intent: Detected intent
        all_responses: All possible responses for this intent
        conversation_history: Previous conversation messages
    
    Returns:
        str: Rephrased natural response or original if rephrasing fails
    """
    if not groq_client:
        return data_response
    
    try:
        # Build conversation context
        context = ""
        if conversation_history and len(conversation_history) > 0:
            context = "\n\nPercakapan sebelumnya:\n"
            for msg in conversation_history[-2:]:
                context += f"User: {msg['user']}\nBot: {msg['bot']}\n"
        
        system_prompt = f"""Kamu adalah chatbot resmi Program Studi Sistem Informasi.

Tugasmu: Berikan jawaban yang natural dan conversational untuk pertanyaan user, TAPI kamu HARUS tetap berdasarkan pada informasi yang sudah disediakan.

**ATURAN KETAT:**
1. Gunakan informasi dari "Jawaban Referensi" sebagai sumber kebenaran utama
2. Kamu boleh mengubah struktur kalimat agar lebih natural dan tidak kaku
3. JANGAN menambahkan informasi yang tidak ada di "Jawaban Referensi"
4. JANGAN mengarang atau membuat asumsi
5. Jika ada placeholder seperti [Nama Dosen], [Link Website], tetap gunakan placeholder tersebut
6. Jawab dengan bahasa yang ramah, informatif, dan profesional
7. Sesuaikan tone dengan konteks percakapan sebelumnya (jika ada)

**Jawaban Referensi:**
{data_response}

**Alternatif jawaban lain untuk topik '{intent}' (gunakan sebagai referensi tambahan jika relevan):**
{chr(10).join([f"- {resp}" for resp in all_responses[:3]])}
{context}

Sekarang, berikan jawaban yang natural untuk pertanyaan user, tapi tetap grounded pada informasi di atas."""
        
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            model=GROQ_MODEL,
            temperature=GROQ_TEMPERATURE,
            max_tokens=GROQ_MAX_TOKENS,
        )
        
        natural_response = response.choices[0].message.content.strip()
        return natural_response
        
    except Exception as e:
        print(f"[ERROR] Rephrasing error: {e}")
        # Fallback to original data response
        return data_response

def combine_multi_intent_answers(qa_pairs):
    """
    Combine multiple Q&A pairs into one natural response using Groq.
    
    Args:
        qa_pairs: List of {'question', 'answer', 'intent', 'confidence'} dicts
    
    Returns:
        str: Combined natural response or concatenated fallback
    """
    if not groq_client or not qa_pairs:
        # Fallback: just concatenate answers
        return " ".join([qa['answer'] for qa in qa_pairs])
    
    try:
        # Build Q&A context
        qa_context = ""
        for i, qa in enumerate(qa_pairs, 1):
            qa_context += f"\nPertanyaan {i}: {qa['question']}\n"
            qa_context += f"Jawaban {i}: {qa['answer']}\n"
        
        system_prompt = f"""Kamu adalah chatbot SI IPI Garut yang sedang menjawab pertanyaan majemuk.

User mengajukan beberapa pertanyaan sekaligus. Kamu sudah mendapatkan jawaban untuk setiap sub-pertanyaan dari knowledge base.

Tugasmu: Gabungkan semua jawaban menjadi SATU paragraf yang natural dan mengalir dengan baik.

**ATURAN KETAT:**
1. Gunakan SEMUA informasi dari jawaban yang disediakan
2. JANGAN menambahkan informasi yang tidak ada di jawaban
3. JANGAN melewatkan jawaban apapun
4. Gabungkan dengan smooth menggunakan kata penghubung yang tepat
5. Buat response yang terdengar seperti satu kesatuan, bukan list
6. Pertahankan tone profesional dan informatif

{qa_context}

Gabungkan semua jawaban di atas menjadi satu response yang natural."""
        
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Tolong gabungkan jawaban-jawaban tersebut."}
            ],
            model=GROQ_MODEL,
            temperature=GROQ_TEMPERATURE,
            max_tokens=GROQ_MAX_TOKENS,
        )
        
        combined_response = response.choices[0].message.content.strip()
        print(f"[MULTI-INTENT] Combined response generated")
        return combined_response
        
    except Exception as e:
        print(f"[ERROR] Multi-intent combination error: {e}")
        # Fallback: just concatenate answers
        fallback = " ".join([qa['answer'] for qa in qa_pairs])
        return fallback
