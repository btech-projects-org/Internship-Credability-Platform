# NLP & CNN-Based Internship Credibility Model

## Project Overview
Production-quality machine learning system for analyzing internship offer credibility using Natural Language Processing and Convolutional Neural Networks.

## Architecture

### Frontend (`frontend/`)
- **Pages**: HTML files with strict DOM-only structure
- **CSS**: Modular styling (base, components, animations)
- **JS**: Organized by responsibility (core, analysis, config, utils)
- **Assets**: Media files (background video)
- **Scripts**: Python utilities for local development

### Backend (`backend/`)
- **Flask App**: REST API server (Python 3.12+)
- **Routes**: API endpoints for credibility prediction
- **Datasets**: Kaggle (EMSCAD) & HuggingFace (DiFraud) loaders
- **Preprocessing**: Text cleaning, tokenization, feature scaling
- **Services**: URL analysis, sentiment analysis, credibility engine
- **Models**: Random Forest & Text CNN (training + inference)
- **Evaluation**: Comprehensive metrics calculation

## Technology Stack

**Frontend:**
- HTML5, CSS3, Vanilla JavaScript
- No frameworks (pure DOM manipulation)

**Backend:**
- Python 3.12+
- Flask (REST API)
- scikit-learn (Random Forest)
- TensorFlow/Keras (Text CNN)
- Transformers (Sentiment Analysis)

**Datasets:**
- EMSCAD (Kaggle): Fake job postings
- DiFraud (HuggingFace): Twitter rumours detection

## Installation

### Prerequisites
- Python 3.12+
- pip
- Git

### Setup

1. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
```

2. **Configure API Keys**
Edit `backend/config/secrets.env`:
```env
KAGGLE_USERNAME=your_username
KAGGLE_KEY=your_api_key
HF_API_KEY=your_huggingface_key
```

3. **Start Backend**
```bash
python backend/app.py
```

4. **Serve Frontend**
```bash
cd frontend
python scripts/serve_frontend.py
```

Visit: `http://localhost:8000`

## Project Structure

```
├── frontend/
│   ├── pages/              # HTML files
│   ├── css/                # Stylesheets
│   │   ├── base/
│   │   ├── components/
│   │   └── animations/
│   ├── js/                 # JavaScript modules
│   │   ├── core/
│   │   ├── analysis/
│   │   ├── config/
│   │   └── utils/
│   ├── assets/             # Media files
│   └── scripts/            # Python utilities
│
├── backend/
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Dependencies
│   ├── config/             # Secrets & config
│   ├── routes/             # API endpoints
│   ├── datasets/           # Dataset loaders
│   ├── preprocessing/      # Text processing
│   ├── services/           # Business logic
│   ├── models/             # ML models
│   └── evaluation/         # Metrics
│
├── documentation/          # Project documentation
└── tests/                  # Tests
```

## API Endpoints

### POST `/api/predict`
Predict internship credibility

### POST `/api/sentiment`
Analyze text sentiment

### POST `/api/extract_url_features`
Extract URL-based features

## Model Training

```bash
python backend/models/train_random_forest.py
python backend/models/train_text_cnn.py
```

## Validation

```bash
python frontend/scripts/path_validator.py
python frontend/scripts/api_contract_check.py
```

## Dataset Access

All datasets accessed via APIs (no local files):
- **Kaggle**: EMSCAD dataset
- **HuggingFace**: DiFraud dataset

## Security

- API keys in `backend/config/secrets.env` (gitignored)
- CORS configured
- Input validation on all endpoints

## License
Academic Project
