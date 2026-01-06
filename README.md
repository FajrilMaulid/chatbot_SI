# 🤖 Chatbot SI dengan Groq API

Chatbot Program Studi Sistem Informasi dengan dukungan Groq API untuk respons yang lebih intelligent dan bervariasi.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Groq API Key (Optional but Recommended)

Groq API memberikan chatbot kemampuan untuk menjawab pertanyaan kompleks dengan lebih baik.

#### Cara Mendapatkan API Key:

1. Buka: https://console.groq.com
2. Sign up/Login (gratis!)
3. Create API Key
4. Copy API key (format: `gsk_...`)

#### Setup .env File:

1. Copy file `.env.example` ke `.env`:

   ```bash
   copy .env.example .env
   ```

2. Edit file `.env`, tambahkan API key:
   ```env
   GROQ_API_KEY=gsk_your_actual_api_key_here
   GROQ_MODEL=llama-3.3-70b-versatile
   CONFIDENCE_THRESHOLD=0.7
   ENABLE_GROQ=true
   ```

**📖 Detail lengkap:** Lihat [GROQ_SETUP.md](GROQ_SETUP.md)

### 3. Jalankan Server

```bash
python app.py
```

Buka browser: **http://localhost:5000**

## ✨ Fitur

### Hybrid Response System

- **Local ML Model** (Cepat ⚡)

  - Untuk pertanyaan FAQ umum
  - Response time: instant
  - Confidence > 70%

- **Groq API** (Intelligent 🧠)
  - Untuk pertanyaan kompleks/baru
  - Response yang natural dan bervariasi
  - Conversation context aware

### Features:

- ✅ **Smart Routing**: Otomatis pakai local atau API based on confidence
- ✅ **Response Caching**: Pertanyaan sama lebih cepat
- ✅ **Conversation Memory**: Bot ingat context percakapan
- ✅ **Fallback System**: Tetap jalan walau tanpa API
- ✅ **Session Management**: Conversation history per user

## 🎯 Cara Kerja

```
User Question
    ↓
Local ML Prediction (Confidence Score)
    ↓
Confidence > 70%?
    ↓ YES → Use Local Answer (Instant)
    ↓ NO  → Use Groq API (Intelligent)
         ↓
    Response + Cache
         ↓
    User
```

## 🔧 Configuration

Edit file `.env` untuk customize:

```env
# Groq API
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile    # Model selection
GROQ_TEMPERATURE=0.7                   # Creativity (0-1)
GROQ_MAX_TOKENS=1024                   # Response length

# Chatbot Behavior
CONFIDENCE_THRESHOLD=0.7               # Routing threshold
ENABLE_GROQ=true                       # Enable/disable API
ENABLE_CACHING=true                    # Cache responses
CACHE_TTL=3600                         # Cache lifetime (seconds)
```

## 📊 Testing

### Test Local ML (Fast):

- "apa itu sistem informasi?"
- "mata kuliah apa saja?"
- "prospek kerja SI"

### Test Groq API (Intelligent):

- "Jelaskan perbedaan detail SI dan Teknik Informatika"
- "Apa keunggulan lulusan SI untuk industri fintech?"
- "Bagaimana prospek karir data analyst untuk lulusan SI?"

### Test Conversation Context:

```
User: "Apa itu SI?"
Bot: [jawaban tentang SI]
User: "Berapa biaya kuliahnya?"
Bot: [paham "nya" = SI dari context]
```

## 🛠️ Troubleshooting

**Groq tidak aktif:**

- Cek `ENABLE_GROQ=true` di `.env`
- Cek API key valid
- Restart server

**Response lambat:**

- Caching akan mempercepat pertanyaan repeatedly
- Groq biasanya <1 detik

**Error database:**

- Pastikan MySQL running
- Database `chatbot_si` exists
- Table `chat_logs` exists

## 📁 Struktur Project

```
chatbot_si/
├── app.py                 # Flask server
├── chatbot_core.py        # ML + Groq logic
├── static/                # Frontend files
│   ├── index.html
│   ├── css/styles.css
│   └── js/app.js
├── data/
│   └── intents_ml.json   # Training data
├── .env                   # Config (git ignored)
├── .env.example           # Config template
├── requirements.txt       # Dependencies
├── GROQ_SETUP.md         # Setup guide
└── README.md             # This file
```

## 🎨 Frontend

Modern dark mode interface dengan:

- Glassmorphism effects
- Smooth animations
- SVG icons
- Responsive design

## ⚙️ API Endpoints

- `GET /` - Main chat interface
- `POST /api/chat` - Send message
- `POST /api/clear-history` - Clear conversation
- `GET /api/health` - Health check

## 📝 License

Educational project untuk Program Studi Sistem Informasi.

## 🆘 Support

Untuk bantuan setup Groq API, lihat [GROQ_SETUP.md](GROQ_SETUP.md)

---

**Made with ❤️ for Sistem Informasi Students**
