import streamlit as st
import mysql.connector
import json
import pandas as pd
import time
import random
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline

# Setup Koneksi DB & Load JSON
@st.cache_resource
def init_db_connection():
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="chatbot_si"
        )
        print("Koneksi Database Berhasil")
        return db_connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        st.error(f"Gagal terhubung ke database: {err}")
        return None

db_connection = init_db_connection()

if db_connection is not None:
    cursor = db_connection.cursor()
else:
    st.stop()

@st.cache_data
def load_chat_data_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            chat_data = json.load(file)
        return chat_data
    except FileNotFoundError:
        st.error(f"Error: File '{file_path}' tidak ditemukan.")
        return None
    except json.JSONDecodeError:
        st.error(f"Error: Format JSON di '{file_path}' salah.")
        return None

# Fungsi untuk melatih model ML
@st.cache_resource
def train_chatbot_model(data):
    """
    Melatih model ML untuk klasifikasi intent.
    Menggantikan initialize_chatbot() yang lama.
    """
    if 'intents' not in data:
        st.error("Format JSON salah. Harusnya memiliki key 'intents'.")
        return None, None

    X_train = [] # List untuk semua patterns (kalimat)
    y_train = [] # List untuk semua intent (label)
    responses_dict = {} # Dictionary untuk menyimpan jawaban

    print("Mulai training model...")
    for intent_data in data['intents']:
        intent_name = intent_data['intent']

        if intent_name not in responses_dict:
            responses_dict[intent_name] = intent_data['responses']

        for pattern in intent_data['patterns']:
            X_train.append(pattern.lower())
            y_train.append(intent_name)

    if not X_train:
        st.error("Tidak ada data training ditemukan di file JSON.")
        return None, None

    # Membuat pipeline ML:
    # 1. TfidfVectorizer: Mengubah teks (keywords) menjadi angka (vektor)
    # 2. SVC: Model classifier (SVM) untuk memprediksi intent
    model = make_pipeline(TfidfVectorizer(), SVC(kernel='linear', probability=True))

    model.fit(X_train, y_train)

    print("Training model selesai.")
    # Kembalikan model yang sudah di-train dan dictionary jawaban
    return model, responses_dict

# Menyimpan data ke database
def save_chat_to_database(user_input, bot_response):
    try:
        sql = "INSERT INTO chat_logs (user_input, bot_response) VALUES (%s, %s)"
        value = (user_input, bot_response)
        cursor.execute(sql, value)
        db_connection.commit()
    except mysql.connector.Error as err:
        print(f"Error Database: {err}")
        st.warning(f"Gagal menyimpan log chat ke database: {err}")
    except Exception as e:
        print(f"Error: {e}")
        st.warning(f"Gagal menyimpan log chat: {e}")

# Arahkan ke file JSON
chat_data = load_chat_data_from_json('data/intents_ml.json')

# Fungsi training
if chat_data:
    model, responses_dict = train_chatbot_model(chat_data)
else:
    model, responses_dict = None, None

# Periksa apakah model berhasil di-train
if model is None:
    st.error("Chatbot tidak dapat diinisialisasi. Aplikasi berhenti.")
    st.stop()

# 2. FUNGSI LOGIKA CHAT

# Tentukan batas kepercayaan (confidence threshold)
CONFIDENCE_THRESHOLD = 0.2 # Artinya, model harus 20% yakin

def get_bot_response(user_input):
    """
    Mendapatkan respons bot menggunakan model ML yang sudah di-train.
    """
    bot_response = None

    # 1. Logika 'marah' (opsional, bisa dipertahankan)
    if 'marah' in user_input.lower() or 'kesal' in user_input.lower() or 'ngamuk' in user_input.lower():
        bot_response = "Maaf jika ada yang membuat Anda marah. Saya di sini untuk membantu. Ada yang bisa saya Lakukan?"

    elif 'kontak' in user_input.lower() or 'email' in user_input.lower() or 'telepon' in user_input.lower():
        bot_response = "Anda bisa menghubungi sekretariat prodi SI di email: [si@universitas.ac.id] atau telepon: [(021) 123456]."

    elif 'kantor' in user_input.lower() or 'gedung' in user_input.lower():
        bot_response = "Kantor Program Studi (Sekretariat) SI berada di [Gedung X, Lantai Y, Ruang Z]."

    elif 'website' in user_input.lower() or 'web' in user_input.lower() or 'link' in user_input.lower():
        bot_response = "Anda bisa menemukan semua informasi resmi di website kami: [https://si.universitas.ac.id]"

    elif 'bantuan' in user_input.lower() or 'help' in user_input.lower() or 'kamu bisa apa' in user_input.lower():
        bot_response = "Saya bisa membantu menjawab pertanyaan umum seputar:\n- Mata Kuliah\n- Prospek Kerja\n- Dosen & Kaprodi\n- Akreditasi\n- Biaya Kuliah"
    
    else:
        # 2. Prediksi menggunakan model ML
        user_input_low = user_input.lower()

        # Dapatkan probabilitas (keyakinan) dari setiap intent
        probabilities = model.predict_proba([user_input_low])[0]

        # Dapatkan probabilitas tertinggi
        max_prob = np.max(probabilities)

        # --- TAMBAHKAN 4 BARIS INI UNTUK DEBUGGING ---
        intent_index = np.argmax(probabilities)
        intent = model.classes_[intent_index]
        print("-" * 30)
        print(f"Input: '{user_input_low}' | Prediksi: '{intent}' | Keyakinan: {max_prob:.2f}")
        # --- AKHIR DARI KODE DEBUGGING ---

        if max_prob > CONFIDENCE_THRESHOLD:
            # Jika keyakinan di atas batas, dapatkan intent-nya
            intent = model.classes_[np.argmax(probabilities)]

            # Ambil jawaban acak dari intent tersebut
            bot_response = random.choice(responses_dict[intent])
        else:
            # Jika model tidak yakin, berikan jawaban default
            bot_response = "Maaf, saya tidak mengerti maksud Anda. Bisa diulangi dengan kata-kata lain?"

    # Simpan ke database (Logika ini tetap sama)
    save_chat_to_database(user_input, bot_response)

    return bot_response

# 3. ANTARMUKA (UI) STREAMLIT

st.set_page_config(page_title="Chatbot SI", page_icon="🤖")
st.title("🤖 Chatbot Sistem Informasi")
st.caption("Selamat datang! Tanyakan apa saja seputar prodi Sistem Informasi.")

# Inisialisasi riwayat chat di session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hai, ada yang bisa saya bantu?"}
    ]

# Tampilkan riwayat chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Terima input dari pengguna (Form input akan menempel di bawah)
if prompt := st.chat_input("Ketik pertanyaan Anda di sini..."):

    # 1. Tampilkan pesan pengguna di UI
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Tambahkan pengguna ke riwayat
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 3. Dapatkan dan tampilkan respons bot
    with st.chat_message("assistant"):
        with st.spinner("Bot sedang mengetik..."):
            time.sleep(0.5)
            response = get_bot_response(prompt) # Memanggil fungsi get_bot_response yang baru
            st.markdown(response)

    # 4. Tambahkan respons bot ke riwayat
    st.session_state.messages.append({"role": "assistant", "content": response})