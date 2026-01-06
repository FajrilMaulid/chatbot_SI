import mysql.connector
import json
import random
import numpy as np
import os
import hashlib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from dotenv import load_dotenv
from groq import Groq
from cachetools import TTLCache

# Load environment variables
load_dotenv()

# Groq Configuration
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')
GROQ_TEMPERATURE = float(os.getenv('GROQ_TEMPERATURE', '0.7'))
GROQ_MAX_TOKENS = int(os.getenv('GROQ_MAX_TOKENS', '1024'))
CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', '0.7'))
ENABLE_GROQ = os.getenv('ENABLE_GROQ', 'true').lower() == 'true'
ENABLE_CACHING = os.getenv('ENABLE_CACHING', 'true').lower() == 'true'
CACHE_TTL = int(os.getenv('CACHE_TTL', '3600'))

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

# Response cache (TTL = 1 hour by default)
response_cache = TTLCache(maxsize=100, ttl=CACHE_TTL) if ENABLE_CACHING else None

# Setup Koneksi DB & Load JSON
def init_db_connection():
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="chatbot_si"
        )
        print("[OK] Koneksi Database Berhasil")
        return db_connection
    except mysql.connector.Error as err:
        print(f"[ERROR] Database Error: {err}")
        return None

def load_chat_data_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            chat_data = json.load(file)
        return chat_data
    except FileNotFoundError:
        print(f"[ERROR] Error: File '{file_path}' tidak ditemukan.")
        return None
    except json.JSONDecodeError:
        print(f"[ERROR] Error: Format JSON di '{file_path}' salah.")
        return None

# Fungsi untuk melatih model ML
def train_chatbot_model(data):
    """
    Melatih model ML untuk klasifikasi intent.
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

# Menyimpan data ke database
def save_chat_to_database(cursor, db_connection, user_input, bot_response, source="local"):
    try:
        sql = "INSERT INTO chat_logs (user_input, bot_response) VALUES (%s, %s)"
        value = (user_input, f"[{source}] {bot_response}")
        cursor.execute(sql, value)
        db_connection.commit()
    except mysql.connector.Error as err:
        print(f"[ERROR] Database Error: {err}")
    except Exception as e:
        print(f"[ERROR] Error: {e}")

def get_cache_key(text):
    """Generate cache key from text"""
    return hashlib.md5(text.lower().strip().encode()).hexdigest()

def get_groq_response(user_input, knowledge_base, conversation_history=None):
    """
    Get response from Groq API with context
    """
    if not groq_client:
        return None
    
    try:
        # Build knowledge base summary
        kb_summary = "Informasi tentang Program Studi Sistem Informasi:\n"
        for kb in knowledge_base[:10]:  # Limit to 10 most relevant
            kb_summary += f"- Topic: {kb['intent']}\n"
            kb_summary += f"  Contoh pertanyaan: {', '.join(kb['patterns'])}\n"
            if kb['responses']:
                kb_summary += f"  Info: {kb['responses'][0]}\n"
        
        # Build conversation context
        context = ""
        if conversation_history and len(conversation_history) > 0:
            context = "\n\nPercakapan sebelumnya:\n"
            for msg in conversation_history[-3:]:  # Last 3 messages
                context += f"User: {msg['user']}\n"
                context += f"Bot: {msg['bot']}\n"
        
        # System prompt
        system_prompt = f"""Kamu adalah chatbot resmi Program Studi Sistem Informasi yang ramah dan informatif.

Tugasmu adalah membantu mahasiswa dan calon mahasiswa dengan informasi seputar:
- Mata kuliah dan kurikulum
- Prospek kerja dan karir lulusan
- Dosen, staff, dan kaprodi
- Akreditasi dan fasilitas
- Biaya kuliah dan pendaftaran
- Visi, misi, dan program studi

Panduan menjawab:
1. Jawab dengan ramah, informatif, dan profesional
2. Gunakan bahasa Indonesia yang baik
3. Jika tidak yakin, katakan dengan jujur dan sarankan kontak resmi
4. Berikan jawaban yang relevan dan tidak bertele-tele
5. Gunakan informasi dari knowledge base jika tersedia

{kb_summary}
{context}

Berikan jawaban yang natural, informatif, dan membantu."""

        # Call Groq API
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            model=GROQ_MODEL,
            temperature=GROQ_TEMPERATURE,
            max_tokens=GROQ_MAX_TOKENS,
        )
        
        response = chat_completion.choices[0].message.content
        return response
        
    except Exception as e:
        print(f"[ERROR] Groq API Error: {e}")
        return None

def get_bot_response(user_input, model, responses_dict, knowledge_base, cursor, db_connection, conversation_history=None):
    """
    Hybrid response: Local ML + Groq API
    """
    bot_response = None
    source = "local"
    
    # Check cache first
    if ENABLE_CACHING and response_cache is not None:
        cache_key = get_cache_key(user_input)
        if cache_key in response_cache:
            print("[CACHE HIT]")
            cached_response = response_cache[cache_key]
            if cursor and db_connection:
                save_chat_to_database(cursor, db_connection, user_input, cached_response['response'], cached_response['source'])
            return cached_response['response']
    
    # 1. Hardcoded responses for specific keywords
    if 'marah' in user_input.lower() or 'kesal' in user_input.lower() or 'ngamuk' in user_input.lower():
        bot_response = "Maaf jika ada yang membuat Anda marah. Saya di sini untuk membantu. Ada yang bisa saya lakukan?"

    elif 'kontak' in user_input.lower() or 'email' in user_input.lower() or 'telepon' in user_input.lower():
        bot_response = "Anda bisa menghubungi sekretariat prodi SI di email: [si@universitas.ac.id] atau telepon: [(021) 123456]."

    elif 'kantor' in user_input.lower() or 'gedung' in user_input.lower():
        bot_response = "Kantor Program Studi (Sekretariat) SI berada di [Gedung X, Lantai Y, Ruang Z]."

    elif 'website' in user_input.lower() or 'web' in user_input.lower() or 'link' in user_input.lower():
        bot_response = "Anda bisa menemukan semua informasi resmi di website kami: [https://si.universitas.ac.id]"

    elif 'bantuan' in user_input.lower() or 'help' in user_input.lower() or 'kamu bisa apa' in user_input.lower():
        bot_response = "Saya bisa membantu menjawab pertanyaan umum seputar:\n- Mata Kuliah\n- Prospek Kerja\n- Dosen & Kaprodi\n- Akreditasi\n- Biaya Kuliah\n- Dan informasi lainnya tentang prodi SI"
    
    else:
        # 2. Try local ML model first
        user_input_low = user_input.lower()
        probabilities = model.predict_proba([user_input_low])[0]
        max_prob = np.max(probabilities)
        
        intent_index = np.argmax(probabilities)
        intent = model.classes_[intent_index]
        
        print("-" * 50)
        print(f" Input: '{user_input_low}'")
        print(f" Prediksi: '{intent}' | Confidence: {max_prob:.2%}")
        
        if max_prob > CONFIDENCE_THRESHOLD:
            # High confidence - use local ML
            bot_response = random.choice(responses_dict[intent])
            source = "local-ml"
            print(f"[OK] Using LOCAL ML (confidence: {max_prob:.2%})")
        else:
            # Low confidence - try Groq API
            print(f"[WARN] Low confidence ({max_prob:.2%}), routing to Groq API...")
            
            if ENABLE_GROQ and groq_client:
                groq_response = get_groq_response(user_input, knowledge_base, conversation_history)
                if groq_response:
                    bot_response = groq_response
                    source = "groq-api"
                    print(f"[OK] Using GROQ API")
                else:
                    # Fallback to local
                    bot_response = "Maaf, saya tidak dapat memproses pertanyaan Anda saat ini. Bisa diulangi dengan kata-kata yang lebih spesifik?"
                    source = "fallback"
                    print(f"[WARN] Groq failed, using fallback")
            else:
                # No Groq or disabled
                if max_prob > 0.3:  # Lower threshold fallback
                    bot_response = random.choice(responses_dict[intent])
                    source = "local-ml-low"
                else:
                    bot_response = "Maaf, saya tidak mengerti maksud Anda. Bisa diulangi dengan kata-kata lain?"
                    source = "fallback"
                print(f"[WARN] Groq not available, using local fallback")
    
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
    
    return bot_response

# Inisialisasi chatbot
def initialize_chatbot():
    """
    Fungsi untuk menginisialisasi chatbot: koneksi DB dan training model
    Returns: (db_connection, cursor, model, responses_dict, knowledge_base)
    """
    print("\n" + "=" * 50)
    print("Initializing Chatbot SI...")
    print("=" * 50)
    
    # Koneksi database
    db_connection = init_db_connection()
    cursor = None
    
    if db_connection is not None:
        cursor = db_connection.cursor()
    
    # Load dan train model
    chat_data = load_chat_data_from_json('data/intents_ml.json')
    
    if chat_data:
        model, responses_dict, knowledge_base = train_chatbot_model(chat_data)
    else:
        model, responses_dict, knowledge_base = None, None, None
    
    # Periksa apakah model berhasil di-train
    if model is None:
        print("[ERROR] Chatbot tidak dapat diinisialisasi.")
        return None, None, None, None, None
    
    print("=" * 50)
    print("[OK] Chatbot initialization complete!")
    print(f"[OK] Local ML: Ready")
    print(f"[OK] Groq API: {'Enabled' if ENABLE_GROQ and groq_client else 'Disabled'}")
    print(f"[OK] Caching: {'Enabled' if ENABLE_CACHING else 'Disabled'}")
    print(f"[OK] Confidence Threshold: {CONFIDENCE_THRESHOLD:.0%}")
    print("=" * 50 + "\n")
    
    return db_connection, cursor, model, responses_dict, knowledge_base
