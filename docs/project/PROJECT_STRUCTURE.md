# 📁 Project Structure Guide

## Folder Organization

```
chatbot_SI/
│
├── 📂 api/                     # Flask Blueprints (API Routes)
│   ├── __init__.py
│   ├── chat_routes.py          # Chat API endpoints
│   └── admin_routes.py         # Admin panel API endpoints
│
├── 📂 core/                    # Chatbot Core Logic
│   ├── __init__.py             # Initialize chatbot, exports
│   ├── database.py             # DB connection & initialization
│   ├── ml_model.py             # ML training & prediction
│   ├── groq_client.py          # Groq API integration
│   ├── filters.py              # Topic filtering & multi-intent
│   └── response_handler.py     # Main response generation pipeline
│
├── 📂 config/                  # Configuration
│   ├── __init__.py
│   └── app_config.py           # Centralized app configuration
│
├── 📂 models/                  # Database Models & Operations
│   ├── __init__.py
│   └── admin_api.py            # Admin CRUD operations
│
├── 📂 utils/                   # Utility Functions & Helpers
│   ├── __init__.py
│   ├── validators.py           # Input validation & sanitization
│   ├── security.py             # Password strength, hashing, IP detection
│   └── logger.py               # Security & admin logging
│
├── 📂 scripts/                 # Standalone Scripts
│   ├── migration_script.py     # Database migration
│   └── chatbot_cli.py          # CLI/Streamlit chatbot (standalone)
│
├── 📂 tests/                   # Test Files
│   ├── __init__.py
│   ├── test_chatbot_filtering.py
│   ├── test_ipi_data.py
│   └── test_multi_intent.py
│
├── 📂 data/                    # Data Files
│   └── intents_ml.json         # Chatbot training data
│
├── 📂 static/                  # Static Files (Frontend)
│   ├── admin.html              # Admin login page
│   ├── admin-dashboard.html    # Admin dashboard
│   ├── index.html              # Main chatbot page
│   ├── css/
│   │   ├── styles.css
│   │   └── admin-styles.css
│   ├── js/
│   │   ├── app.js
│   │   ├── admin-app.js
│   │   └── particles.js
│   └── images/
│
├── 📂 logs/                    # Application Logs
│   ├── security.log            # Login attempts, unauthorized access
│   ├── admin_actions.log       # Admin CRUD operations
│   └── app.log                 # General application logs
│
├── 📂 docs/                    # Documentation
│   ├── DEPLOYMENT_CHECKLIST.md
│   ├── DEPLOYMENT_GUIDE.md
│   ├── GROQ_SETUP.md
│   └── RAILWAY_QUICKSTART.md
│
├── 📄 app.py                   # Main Flask Application (120 lines)
├── 📄 app.py.backup            # Backup of original app.py
├── 📄 chatbot_core.py          # Original core (can delete after verification)
├── 📄 requirements.txt         # Python dependencies
├── 📄 .env                     # Environment variables (not in git)
├── 📄 .env.example             # Example environment variables
├── 📄 .gitignore               # Git ignore patterns
├── 📄 README.md                # Project documentation
├── 📄 PROJECT_STRUCTURE.md     # This file
├── 📄 Procfile                 # Deployment configuration
└── 📄 runtime.txt              # Python version
```

## 📝 File Descriptions

### Core Application

- **app.py** - Main Flask application with simplified structure (120 lines)
- **chatbot_core.py** - Original monolithic core (can delete after testing)
- **app.py.backup** - Backup of original app.py before refactoring

### API Blueprints (`api/`)

- **chat_routes.py** - Chat endpoints (`/api/chat`, `/api/clear-history`, `/api/health`)
- **admin_routes.py** - Admin panel routes (`/admin`, `/api/admin/*`)

### Core Modules (`core/`)

- **database.py** - Database connection (Railway & local), JSON loading, chat logging
- **ml_model.py** - ML model training, intent prediction, confidence scoring
- **groq_client.py** - Groq API client, natural response rephrasing, multi-intent combination
- **filters.py** - Topic relevance filtering, multi-intent detection
- **response_handler.py** - Main response pipeline, caching, multi-stage processing
- ****init**.py** - Package initialization, `initialize_chatbot()` function

### Configuration (`config/`)

- **app_config.py** - Centralized configuration class (Flask, security, chatbot settings)

### Models (`models/`)

- **admin_api.py** - Admin authentication, CRUD operations for intents/patterns/responses, chat logging

### Utilities (`utils/`)

- **validators.py** - Input validation (username, password, intent names, sanitization)
- **security.py** - Password strength checking, hashing, IP detection
- **logger.py** - Security logging, admin action logging

### Scripts (`scripts/`)

- **migration_script.py** - Database migration from JSON to MySQL
- **chatbot_cli.py** - Standalone CLI chatbot with Streamlit UI

### Tests (`tests/`)

- **test_chatbot_filtering.py** - Topic filtering tests
- **test_ipi_data.py** - IPI data tests
- **test_multi_intent.py** - Multi-intent detection tests

## 🚀 Quick Start

### 1. Install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Setup database:

```bash
python scripts/migration_script.py
```

### 3. Run application:

```bash
python app.py
```

### 4. Access:

- **Chatbot**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin

## 📦 Import Patterns

### Importing from core:

```python
from core import initialize_chatbot, get_bot_response, groq_client
```

### Importing from api:

```python
from api import chat_bp, admin_bp, init_chat_routes, init_admin_routes
```

### Importing from config:

```python
from config import Config
```

### Importing from models:

```python
from models import admin_api
```

### Importing from utils:

```python
from utils.validators import validate_username, validate_password
from utils.security import check_password_strength, get_client_ip
from utils.logger import log_login_attempt, log_admin_action
```

## Running Scripts

### Run migration:

```bash
python scripts/migration_script.py
```

### Run CLI chatbot (Streamlit):

```bash
streamlit run scripts/chatbot_cli.py
```

### Run tests:

```bash
# Individual test
python tests/test_chatbot_filtering.py

# All tests (if pytest installed)
pytest tests/
```

## 🔒 Security Features Location

- **Rate Limiting**: app.py (Flask-Limiter)
- **Input Validation**: utils/validators.py
- **Password Strength**: utils/security.py
- **Logging**: utils/logger.py → logs/
- **Security Headers**: app.py (Flask-Talisman)

## 📊 Best Practices

### 1. **Models** - Database operations only

- Keep database logic in `models/`
- Use parameterized queries
- Handle errors gracefully

### 2. **Utils** - Reusable utility functions

- Common validation logic
- Security utilities
- Logging functions

### 3. **API** - Request handling only

- Thin controllers
- Delegate to core/models
- Return proper HTTP codes

### 4. **Core** - Business logic

- Chatbot intelligence
- ML processing
- Response generation

### 5. **Tests** - Keep test coverage high

- Test each module independently
- Integration tests for workflows
- Mock external dependencies

## 🔄 Adding New Features

### Need to add a new chat endpoint?

→ Add to `api/chat_routes.py`

### Need to modify ML logic?

→ Edit `core/ml_model.py`

### Need to change Groq integration?

→ Edit `core/groq_client.py`

### Need to add admin feature?

→ Add to `api/admin_routes.py`

### Need to update config?

→ Edit `config/app_config.py`

### Need to add validation?

→ Add to `utils/validators.py`

### Need to check logs?

→ View `logs/` folder files

## 📈 Architecture Benefits

- ✅ Modular & organized
- ✅ Single responsibility per module
- ✅ Easy to test independently
- ✅ Easy to maintain and extend
- ✅ Scalable architecture
- ✅ Industry best practices
- ✅ Clear separation of concerns
