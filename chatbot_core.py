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

# New Feature Flags
ENABLE_TOPIC_FILTERING = os.getenv('ENABLE_TOPIC_FILTERING', 'true').lower() == 'true'
TOPIC_FILTER_STRICT_MODE = os.getenv('TOPIC_FILTER_STRICT_MODE', 'true').lower() == 'true'
FORCE_DATA_GROUNDED = os.getenv('FORCE_DATA_GROUNDED', 'true').lower() == 'true'
ENABLE_RESPONSE_REPHRASING = os.getenv('ENABLE_RESPONSE_REPHRASING', 'true').lower() == 'true'

# Multi-Intent Configuration
ENABLE_MULTI_INTENT = os.getenv('ENABLE_MULTI_INTENT', 'true').lower() == 'true'
MULTI_INTENT_MAX_QUESTIONS = int(os.getenv('MULTI_INTENT_MAX_QUESTIONS', '5'))

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
    """
    Initialize database connection.
    Supports both Railway DATABASE_URL and local .env configuration.
    """
    try:
        # Check if Railway DATABASE_URL is available
        database_url = os.getenv('DATABASE_URL')
        
        if database_url:
            # Parse Railway DATABASE_URL format: mysql://user:password@host:port/database
            import re
            match = re.match(r'mysql://(.+):(.+)@(.+):(\d+)/(.+)', database_url)
            if match:
                user, password, host, port, database = match.groups()
                print(f"[...] Connecting to Railway MySQL: {host}")
                db_connection = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database,
                    port=int(port)
                )
                print("[OK] Railway Database Connected")
                return db_connection
        
        # Fallback to local/manual environment variables
        print("[...] Using local database configuration")
        db_connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', ''),
            database=os.getenv('MYSQL_DATABASE', 'chatbot_si')
        )
        print("[OK] Local Database Connected")
        return db_connection
        
    except mysql.connector.Error as err:
        print(f"[ERROR] Database Error: {err}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
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

def is_topic_relevant(user_input):
    """
    Check if user question is relevant to Sistem Informasi program.
    Returns: (is_relevant: bool, reason: str)
    """
    if not ENABLE_TOPIC_FILTERING:
        return True, "filtering disabled"
    
    if not groq_client:
        # Fallback: accept all if Groq not available
        return True, "groq unavailable"
    
    try:
        # Define SI-related topics
        si_topics = [
            "Program Studi Sistem Informasi",
            "Mata kuliah SI",
            "Prospek kerja lulusan SI",
            "Dosen dan staff SI",
            "Akreditasi prodi SI",
            "Biaya kuliah SI",
            "Pendaftaran SI",
            "Kurikulum dan pembelajaran",
            "Fasilitas dan laboratorium",
            "Himpunan mahasiswa (HIMASIFOR)",
            "Karir di bidang teknologi informasi",
            "Perbedaan SI dengan prodi IT lainnya",
            "Institut Pendidikan Indonesia (IPI)",
            "Universitas/Kampus IPI Garut",
            "Lokasi kampus di Garut"
        ]
        
        system_prompt = f"""Kamu adalah filter topik untuk chatbot Program Studi Sistem Informasi Institut Pendidikan Indonesia (IPI) Garut.

Tugasmu: Tentukan apakah pertanyaan user RELEVAN dengan topik-topik berikut:
{chr(10).join([f"- {topic}" for topic in si_topics])}

Kriteria RELEVAN:
- Pertanyaan tentang kuliah, pendidikan, atau akademik di prodi SI
- Pertanyaan tentang teknologi informasi dalam konteks pendidikan/karir
- Pertanyaan umum tentang prodi (dosen, fasilitas, biaya, dll)
- Pertanyaan tentang IPI (Institut Pendidikan Indonesia) atau kampus
- Pertanyaan tentang lokasi kampus di Garut
- Sapaan atau percakapan pembuka (halo, hai, terima kasih)

Kriteria TIDAK RELEVAN:
- Pertanyaan umum yang tidak ada hubungannya dengan SI, IPI, atau pendidikan
- Pertanyaan tentang topik lain (politik, olahraga, hiburan, cuaca, dll)
- Pertanyaan pribadi yang tidak berhubungan dengan prodi atau kampus
- Permintaan untuk melakukan hal di luar konteks informasi SI/IPI

Jawab HANYA dengan format:
RELEVAN: [alasan singkat]
atau
TIDAK RELEVAN: [alasan singkat]

Contoh:
- "apa itu sistem informasi?" → RELEVAN: pertanyaan tentang definisi prodi SI
- "apa itu IPI?" → RELEVAN: pertanyaan tentang universitas tempat prodi SI berada
- "IPI di mana?" → RELEVAN: pertanyaan tentang lokasi kampus
- "siapa presiden indonesia?" → TIDAK RELEVAN: pertanyaan politik, bukan tentang SI/IPI
- "belajar python di si?" → RELEVAN: pertanyaan tentang mata kuliah SI
- "resep nasi goreng" → TIDAK RELEVAN: pertanyaan kuliner, tidak ada hubungan dengan SI/IPI
- "di garut dimana?" → RELEVAN: pertanyaan tentang lokasi kampus IPI"""
        
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            model=GROQ_MODEL,
            temperature=0.3,  # Lower temperature for more consistent filtering
            max_tokens=100,
        )
        
        result = response.choices[0].message.content.strip()
        
        if result.startswith("RELEVAN"):
            reason = result.replace("RELEVAN:", "").strip()
            return True, reason
        elif result.startswith("TIDAK RELEVAN"):
            reason = result.replace("TIDAK RELEVAN:", "").strip()
            return False, reason
        else:
            # Fallback if response format unexpected
            return True, "uncertain format"
            
    except Exception as e:
        print(f"[ERROR] Topic filtering error: {e}")
        # Fallback: accept if filtering fails
        return True, "filtering error"

def find_best_matching_intent(user_input, model, responses_dict, knowledge_base):
    """
    Find best matching intent from data model.
    Returns: (intent, confidence, response_from_data, all_responses)
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

def rephrase_response_naturally(user_input, data_response, intent, all_responses, conversation_history=None):
    """
    Rephrase the data model response to be more natural while staying grounded.
    """
    if not ENABLE_RESPONSE_REPHRASING or not groq_client:
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

def detect_multi_intent(user_input):
    """
    Detect if user question contains multiple intents and extract sub-questions.
    Returns: (is_multi_intent: bool, sub_questions: list)
    """
    if not ENABLE_MULTI_INTENT or not groq_client:
        return False, []
    
    try:
        system_prompt = """Kamu adalah detector pertanyaan majemuk untuk chatbot SI IPI Garut.

Tugasmu: Deteksi apakah pertanyaan user mengandung MULTIPLE INTENTS (lebih dari satu pertanyaan dalam satu kalimat).

Jika YA (multi-intent), ekstrak menjadi sub-pertanyaan yang lebih spesifik.
Jika TIDAK (single intent), return SINGLE.

Format output:
MULTIPLE:
1. [sub-pertanyaan 1]
2. [sub-pertanyaan 2]
3. [sub-pertanyaan 3]
...

atau

SINGLE

Contoh:

Input: "apa itu sistem informasi ipi garut dan siapa kaprodi nya"
Output:
MULTIPLE:
1. apa itu sistem informasi?
2. apa itu ipi garut?
3. siapa kaprodi sistem informasi?

Input: "biaya kuliah berapa dan dimana lokasi kampus?"
Output:
MULTIPLE:
1. biaya kuliah si berapa?
2. dimana lokasi kampus ipi?

Input: "apa itu sistem informasi?"
Output:
SINGLE

Input: "prospek kerja lulusan si apa saja dan berapa lama kuliah?"
Output:
MULTIPLE:
1. prospek kerja lulusan si apa saja?
2. berapa lama kuliah si?

Penting:
- Ekstrak pertanyaan yang jelas dan spesifik
- Jangan duplikasi konten yang sama
- Maksimal 5 sub-pertanyaan
- Pertahankan konteks SI/IPI jika relevan"""
        
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            model=GROQ_MODEL,
            temperature=0.3,
            max_tokens=300,
        )
        
        result = response.choices[0].message.content.strip()
        
        if result.startswith("SINGLE"):
            return False, []
        elif result.startswith("MULTIPLE:"):
            lines = result.split('\n')[1:]  # Skip "MULTIPLE:" line
            sub_questions = []
            for line in lines:
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-')):
                    # Remove numbering (e.g., "1. ", "- ")
                    question = line.split('.', 1)[-1].strip() if '.' in line else line.lstrip('-').strip()
                    if question:
                        sub_questions.append(question)
            
            # Limit to max questions
            sub_questions = sub_questions[:MULTI_INTENT_MAX_QUESTIONS]
            
            if sub_questions:
                return True, sub_questions
        
        return False, []
        
    except Exception as e:
        print(f"[ERROR] Multi-intent detection error: {e}")
        return False, []

def answer_multi_intent(sub_questions, model, responses_dict, knowledge_base, conversation_history=None):
    """
    Answer multiple sub-questions and combine into one natural response.
    Returns: Combined natural response
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
    Multi-Stage Data-Grounded Response System:
    Stage 0: Multi-Intent Detection - Check if question has multiple intents
    Stage 1: Topic Filtering - Check if question is SI-related
    Stage 2: Intent Matching - Find best match from data model
    Stage 3: Natural Rephrasing - Make response conversational
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
    is_multi, sub_questions = detect_multi_intent(user_input)
    
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
        is_relevant, filter_reason = is_topic_relevant(user_input)
        
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
                    if ENABLE_RESPONSE_REPHRASING and groq_client:
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
    print(f"[OK] Topic Filtering: {'Enabled' if ENABLE_TOPIC_FILTERING else 'Disabled'}")
    print(f"[OK] Data-Grounded Mode: {'Forced' if FORCE_DATA_GROUNDED else 'Optional'}")
    print(f"[OK] Response Rephrasing: {'Enabled' if ENABLE_RESPONSE_REPHRASING else 'Disabled'}")
    print(f"[OK] Confidence Threshold: {CONFIDENCE_THRESHOLD:.0%}")
    print("=" * 50 + "\n")
    
    return db_connection, cursor, model, responses_dict, knowledge_base
