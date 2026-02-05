# Setup Guide: Groq API Key

Panduan lengkap untuk mendapatkan dan setup Groq API key (GRATIS).

## 🚀 Langkah 1: Daftar Akun Groq

1. Buka website Groq: **https://console.groq.com**
2. Klik tombol **"Sign Up"** atau **"Get Started"**
3. Daftar menggunakan:
   - Email + Password, atau
   - Google Account (lebih cepat)
4. Verifikasi email jika diminta

## 🔑 Langkah 2: Generate API Key

1. Setelah login, masuk ke **Console/Dashboard**
2. Di sidebar kiri, klik **"API Keys"**
3. Klik tombol **"Create API Key"**
4. Beri nama untuk key Anda (contoh: "Chatbot SI Development")
5. Klik **"Create"**
6. **PENTING:** Copy API key yang muncul dan simpan dengan aman!
   - API key hanya ditampilkan sekali
   - Format: `gsk_...` (panjang ~56 karakter)

## 📝 Langkah 3: Setup Environment File

1. Di folder project Anda (`d:\File Web\chatbot_si - Copy`), buat file baru bernama `.env`

2. Buka file `.env` dengan text editor

3. Tambahkan baris berikut (ganti dengan API key Anda):

```env
GROQ_API_KEY=gsk_your_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
CONFIDENCE_THRESHOLD=0.7
ENABLE_GROQ=true
```

4. **Contoh isi file `.env`:**

```env
GROQ_API_KEY=gsk_abcdef1234567890abcdef1234567890abcdef1234567890ab
GROQ_MODEL=llama-3.3-70b-versatile
CONFIDENCE_THRESHOLD=0.7
ENABLE_GROQ=true
```

5. Save file `.env`

## ⚠️ PENTING: Security

> [!CAUTION] > **Jangan commit file `.env` ke Git/GitHub!**

File `.env` sudah otomatis masuk ke `.gitignore`, tapi pastikan:

- JANGAN share API key ke orang lain
- JANGAN upload ke public repository
- JANGAN hardcode di source code

## ✅ Langkah 4: Verifikasi Setup

Setelah file `.env` dibuat, jalankan chatbot:

```bash
python app.py
```

Pada console, Anda akan melihat:

```
Groq API initialized successfully
✓ Model: llama-3.3-70b-versatile
```

Jika ada error, cek:

- API key benar (56 karakter dimulai dengan `gsk_`)
- File `.env` di folder yang benar
- Tidak ada spasi extra di file `.env`

## 💡 Model Options

Groq menyediakan beberapa model gratis:

| Model                     | Speed      | Intelligence | Use Case                          |
| ------------------------- | ---------- | ------------ | --------------------------------- |
| `llama-3.3-70b-versatile` | ⚡⚡⚡     | 🧠🧠🧠🧠     | **Recommended** - Balance terbaik |
| `llama-3.1-8b-instant`    | ⚡⚡⚡⚡⚡ | 🧠🧠🧠       | Super cepat, simple questions     |
| `mixtral-8x7b-32768`      | ⚡⚡⚡⚡   | 🧠🧠🧠🧠     | Long context                      |

Untuk mengubah model, edit `.env`:

```env
GROQ_MODEL=llama-3.1-8b-instant
```

## 🎯 Testing API Key

Setelah setup, test dengan pertanyaan kompleks di chatbot:

**Contoh pertanyaan untuk test Groq:**

- "Jelaskan perbedaan detail antara SI dengan Teknik Informatik"
- "Apa keunggulan lulusan SI dibanding jurusan lain untuk industri fintech?"
- "Bagaimana prospek karir data analyst untuk lulusan SI?"

Jika Groq aktif, jawaban akan lebih detail dan natural.

## 📊 Monitoring Usage

1. Login ke **https://console.groq.com**
2. Check **"Usage"** atau **"Billing"** tab
3. Monitor:
   - Request count
   - Token usage
   - Rate limits

**Groq Free Tier:**

- ✅ 14,400 requests/day
- ✅ 30 requests/minute
- ✅ Unlimited untuk development

## 🔧 Troubleshooting

### Error: "Invalid API Key"

- Cek API key di console.groq.com
- Pastikan copy paste tanpa spasi
- Generate API key baru jika perlu

### Error: "Rate Limit Exceeded"

- Tunggu 1 menit
- Groq limit: 30 req/min
- Caching akan mengurangi API calls

### Chatbot tidak pakai Groq

- Cek `ENABLE_GROQ=true` di `.env`
- Restart server (`python app.py`)
- Cek console logs untuk error

## 📚 Resources

- **Groq Console:** https://console.groq.com
- **Groq Documentation:** https://console.groq.com/docs
- **Groq Models:** https://console.groq.com/docs/models

---

**Setelah setup selesai, chatbot Anda siap dengan Groq AI! 🎉**
