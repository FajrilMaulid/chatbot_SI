# 🤝 Berkontribusi pada Chatbot SI

Terima kasih telah mempertimbangkan untuk berkontribusi pada Chatbot SI! Orang-orang seperti Anda yang membuat chatbot ini menjadi lebih baik untuk semua orang.

## 📋 Daftar Isi

- [Kode Etik](#kode-etik)
- [Bagaimana Saya Bisa Berkontribusi?](#bagaimana-saya-bisa-berkontribusi)
- [Setup Development](#setup-development)
- [Proses Pull Request](#proses-pull-request)
- [Standar Coding](#standar-coding)
- [Struktur Project](#struktur-project)

## 📜 Kode Etik

Project ini dan setiap orang yang berpartisipasi di dalamnya diatur oleh rasa hormat dan profesionalisme. Dengan berpartisipasi, Anda diharapkan untuk menjunjung tinggi kode etik ini.

## 🎯 Bagaimana Saya Bisa Berkontribusi?

### Melaporkan Bug

Sebelum membuat laporan bug, silakan cek issues yang sudah ada. Ketika membuat laporan bug, sertakan sebanyak mungkin detail:

**Template Laporan Bug:**

```markdown
**Deskripsi bug**
Deskripsi yang jelas tentang apa bug-nya.

**Cara Mereproduksi**
Langkah-langkah untuk mereproduksi perilaku:

1. Pergi ke '...'
2. Klik pada '....'
3. Lihat error

**Perilaku yang diharapkan**
Apa yang Anda harapkan terjadi.

**Screenshot**
Jika applicable, tambahkan screenshot.

**Environment:**

- OS: [mis. Windows 11]
- Versi Python: [mis. 3.11]
- Versi MySQL: [mis. 8.0]
```

### Menyarankan Peningkatan

Saran peningkatan dilacak sebagai GitHub issues. Ketika membuat saran peningkatan, sertakan:

- **Judul dan deskripsi yang jelas**
- **Perilaku saat ini vs. perilaku yang diusulkan**
- **Mengapa peningkatan ini akan berguna**
- **Pendekatan implementasi yang mungkin**

### Pull Requests

1. **Fork repo** dan buat branch Anda dari `main`
2. **Buat perubahan Anda** mengikuti standar coding kami
3. **Test perubahan Anda** secara menyeluruh
4. **Update dokumentasi** jika diperlukan
5. **Submit pull request**

## 🔧 Setup Development

### 1. Fork dan Clone

```bash
# Fork repository di GitHub, kemudian:
git clone https://github.com/USERNAME-ANDA/chatbot_SI.git
cd chatbot_SI
```

### 2. Buat Branch

```bash
# Buat feature branch
git checkout -b feature/nama-fitur-anda

# Atau bugfix branch
git checkout -b fix/deskripsi-bug
```

### 3. Setup Development Environment

```bash
# Buat virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8
```

### 4. Setup Database

```bash
# Buat test database
mysql -u root -p -e "CREATE DATABASE chatbot_si_dev;"

# Copy file env
cp .config/.env.example .env

# Update .env dengan development database
MYSQL_DATABASE=chatbot_si_dev

# Jalankan migration
python scripts/migration_script.py
```

### 5. Jalankan Tests

```bash
# Jalankan semua tests
pytest tests/

# Jalankan dengan coverage
pytest --cov=. tests/

# Jalankan test spesifik
pytest tests/test_chatbot_filtering.py
```

## 🔄 Proses Pull Request

### Sebelum Submit

- [ ] Code mengikuti panduan style project
- [ ] Semua tests lolos
- [ ] Tests baru ditambahkan untuk fitur baru
- [ ] Dokumentasi diupdate
- [ ] Tidak ada merge conflicts
- [ ] Commit messages jelas

### Format Judul PR

```
type(scope): deskripsi singkat

Contoh:
feat(chatbot): tambah analisis sentimen
fix(admin): perbaiki masalah login timeout
docs(readme): update panduan instalasi
style(ui): tingkatkan responsive design
refactor(core): optimasi query database
test(filters): tambah tests topic filtering
```

### Template Deskripsi PR

```markdown
## Deskripsi

Deskripsi singkat tentang perubahan yang dibuat.

## Jenis Perubahan

- [ ] Bug fix
- [ ] Fitur baru
- [ ] Breaking change
- [ ] Update dokumentasi

## Testing

Jelaskan bagaimana Anda menguji perubahan Anda.

## Screenshot

Jika applicable, tambahkan screenshot.

## Checklist

- [ ] Code mengikuti panduan style
- [ ] Self-review code
- [ ] Komentar pada code yang kompleks
- [ ] Update dokumentasi
- [ ] Tidak ada warning baru
- [ ] Tambah tests
- [ ] Semua tests lolos
```

## 💻 Standar Coding

### Panduan Style Python

Kami mengikuti [PEP 8](https://pep8.org/) dengan beberapa modifikasi:

```python
# Baik: Nama variabel yang jelas
def calculate_response_confidence(intent_score, topic_score):
    return (intent_score + topic_score) / 2

# Buruk: Nama variabel tidak jelas
def calc(x, y):
    return (x + y) / 2
```

### Organisasi File

```python
# Urutan import:
# 1. Standard library
import os
import sys
from datetime import datetime

# 2. Third-party
import flask
from flask import Flask, request
import mysql.connector

# 3. Local imports
from core.database import Database
from models.admin_api import AdminAPI
```

### Formatting Code

```bash
# Gunakan Black untuk formatting (panjang baris 88)
black .

# Gunakan flake8 untuk linting
flake8 .
```

### Konvensi Penamaan

- **Files:** `lowercase_with_underscores.py`
- **Classes:** `PascalCase`
- **Functions:** `snake_case`
- **Constants:** `UPPER_CASE`
- **Variables:** `snake_case`

### Dokumentasi

```python
def process_compound_question(question: str, intents: list) -> dict:
    """
    Proses pertanyaan majemuk yang mengandung beberapa intents.

    Args:
        question (str): Pertanyaan majemuk dari user
        intents (list): List intents yang terdeteksi dengan confidence scores

    Returns:
        dict: Response gabungan dengan metadata

    Example:
        >>> process_compound_question(
        ...     "Apa itu SI dan berapa biayanya?",
        ...     [{'tag': 'definisi_si'}, {'tag': 'biaya'}]
        ... )
        {'response': '...', 'intents': [...]}
    """
    # Implementasi
    pass
```

### Komentar

```python
# Baik: Jelaskan MENGAPA, bukan APA
# Hitung rata-rata tertimbang untuk memprioritaskan response terbaru
weighted_score = (recent_score * 0.7) + (overall_score * 0.3)

# Buruk: Hanya mendeskripsikan apa yang code lakukan
# Kalikan recent_score dengan 0.7 dan tambahkan ke overall_score kali 0.3
weighted_score = (recent_score * 0.7) + (overall_score * 0.3)
```

## 📂 Struktur Project

Memahami struktur project membantu Anda berkontribusi secara efektif:

```
chatbot_SI/
├── api/              # Flask route handlers
│   ├── chat_routes.py
│   └── admin_routes.py
├── core/             # Core chatbot logic
│   ├── database.py
│   ├── ml_model.py
│   ├── groq_client.py
│   ├── filters.py
│   └── response_handler.py
├── models/           # Database models
├── utils/            # Utility functions
├── static/           # Frontend files
├── tests/            # Test files
└── docs/             # Dokumentasi
```

### Dimana Membuat Perubahan

**Menambah fitur baru:**

- Logic chatbot → `core/`
- API endpoints → `api/`
- Model database → `models/`
- Frontend → `static/`

**Memperbaiki bugs:**

- Cek logs di `logs/` terlebih dahulu
- File terkait berdasarkan error trace

**Meningkatkan docs:**

- Docs umum → `docs/`
- Instalasi → `INSTALLATION.md`
- API docs → `docs/api/` (buat jika diperlukan)

## ✅ Panduan Testing

### Menulis Tests

```python
# tests/test_your_feature.py
import pytest
from core.your_module import your_function

def test_your_function_basic():
    """Test fungsionalitas dasar."""
    result = your_function("input")
    assert result == "expected_output"

def test_your_function_edge_case():
    """Test edge cases."""
    result = your_function("")
    assert result is None
```

### Test Coverage

Target untuk:

- **Core modules:** 80%+ coverage
- **Critical paths:** 90%+ coverage
- **Fitur baru:** 100% coverage

```bash
# Cek coverage
pytest --cov=core --cov-report=html tests/
```

## 🐛 Tips Debugging

### Enable Debug Mode

```env
# .env
DEBUG=True
LOG_LEVEL=DEBUG
```

### Cek Logs

```bash
# Application logs
tail -f logs/app.log

# Security logs
tail -f logs/security.log
```

### Gunakan Python Debugger

```python
# Tambahkan ke code Anda
import pdb; pdb.set_trace()
```

## 📝 Commit Messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: Fitur baru
- `fix`: Bug fix
- `docs`: Dokumentasi
- `style`: Formatting
- `refactor`: Restructuring code
- `test`: Menambah tests
- `chore`: Maintenance

### Contoh

```bash
feat(chatbot): tambah multi-intent detection

- Implementasi parsing pertanyaan majemuk
- Tambah logic kombinasi intent
- Update response handler

Closes #123
```

## 🎉 Pengakuan

Kontributor akan:

- Dicantumkan di project README
- Disebutkan di release notes
- Diberi kredit di commit history

## 📞 Mendapatkan Bantuan

- **Pertanyaan:** [GitHub Discussions](https://github.com/your-username/chatbot_SI/discussions)
- **Chat:** [Join Discord kami](#) (jika tersedia)
- **Email:** your.email@example.com

## 📚 Sumber Daya Tambahan

- [Python Style Guide](https://pep8.org/)
- [Flask Best Practices](https://flask.palletsprojects.com/en/latest/patterns/)
- [Git Workflow](https://guides.github.com/introduction/flow/)

---

## 🙏 Terima Kasih!

Kontribusi Anda membuat project ini lebih baik. Kami menghargai waktu dan usaha Anda!

**Selamat Coding!** 🚀
