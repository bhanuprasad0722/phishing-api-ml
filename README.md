# Phishing Detection API using Machine Learning

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-5.2.9-green.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This is a **RESTful API** built with **Django** and **Django REST Framework** that detects whether a given URL is **phishing** or **legitimate** using a pre-trained **Random Forest Classifier** machine learning model.

### Key Features
- Secure user registration and JWT-based authentication
- Authenticated endpoint to submit a URL and receive real-time phishing prediction with confidence score
- Prediction history automatically saved in the database for logged-in users
- 14 heuristic-based features extracted directly from the URL string (no external page fetching required)
- CORS enabled for easy integration with frontend applications
- Admin panel to view users and prediction history
- Automated testing and GitHub Actions CI
- Deployed on Render.com via direct GitHub repository connection

The model uses URL characteristics such as length, special characters, HTTPS presence, suspicious keywords, subdomain count, and more to deliver accurate phishing detection.

**Live API**: https://phishing-api-ml-1.onrender.com

## Technologies Used

- **Framework**: Django 5.2.9, Django REST Framework 3.16.1
- **Authentication**: djangorestframework-simplejwt 5.5.1
- **Machine Learning**: scikit-learn 1.8.0, joblib 1.5.3, numpy 2.3.5, pandas 2.3.3
- **Production Server**: Gunicorn 23.0.0
- **Database**: SQLite (development), configurable for PostgreSQL in production
- **Other**: django-cors-headers 4.9.0, python-dotenv 1.2.1
- **Testing**: pytest 9.0.2, pytest-django 4.11.1

All dependencies are listed in `requirements.txt`.

## Quick Start (Local Development)

### Prerequisites
- Python 3.11 or higher
- Git

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/bhanuprasad0722/phishing-api-ml.git
   cd phishing-api-ml

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   
4. **Apply Database Migrations**
   ```bash
   python config/manage.py migrate

5. **Run the Development Server**
   ```bash
   python config/manage.py runserver

## Production Deployment (Render.com)

The API is currently deployed on Render.com using direct connection to this GitHub repository (not via Docker image).

- Render automatically pulls from the main branch, installs dependencies, runs migrations, and starts Gunicorn.
- Environment variables (e.g., SECRET_KEY, database config) should be set in the Render dashboard for security.
- Allowed hosts and CSRF trusted origins are configured to support Render deployment.

## API Endpoints
### Authentication

**Register New User**
```bash
POST /api/auth/register/JSON{
  "username": "your_username",
  "email": "your@email.com",
  "password": "your_secure_password"
}
Response:JSON{ "message": "User Registered Successfully" }
```
**Login**
```bash
POST /api/auth/login/JSON{
  "username": "your_username",
  "password": "your_secure_password"
}
Response:JSON{
  "refresh": "jwt_refresh_token",
  "access": "jwt_access_token"
}
```
**Refresh Token**
```bash
POST /api/auth/refresh/JSON
  { "refresh": "your_refresh_token" }
```
## Prediction

**Check if URL is Phishing**
```bash
POST /api/predictions/predict/
Requires Authentication (Bearer Token in Authorization header)
JSON{
  "url": "https://example-suspicious-login.com"
}
Response:JSON{
  "url": "https://example-suspicious-login.com",
  "prediction": "phishing",   // or "legitimate"
  "confidence": 0.97
}
```
## Admin Panel
- Access at /admin/ using superuser credentials to manage users and view full prediction history.

## Machine Learning Model Details

- Algorithm: Random Forest Classifier
- Pre-trained Model: Located at **config/ml/artifacts/random_forest_model.pkl** (included in repo)
- Feature Extraction: 14 URL-based features including:
- URL length and depth
- Count of dots, digits, hyphens, '@', etc.
- Presence of HTTPS
- Subdomain and path analysis
- IP address in URL
- Suspicious keywords (login, bank, secure, update, etc.)
- Known URL shorteners
- Presence of query parameters
- Suspicious TLDs

## Testing
**Run the test suite locally:**
```bash
pytest config/
```
- Tests cover user registration, authentication, prediction endpoint, and model loading. Slow tests are marked and excluded by default in CI.

## Project Structure
.
├── .github/workflows/ci.yml              # GitHub Actions CI (tests + Docker build)
├── config/
│   ├── manage.py
│   ├── config/                           # Django settings, URLs, WSGI
│   ├── users/                            # User registration app
│   ├── predictions/                      # Core prediction logic, models, views
│   └── ml/
│       ├── feature_extraction.py         # All URL feature functions
│       ├── train.py                      # Model training script
│       └── artifacts/
│           └── random_forest_model.pkl   # Pre-trained ML model
├── Dockerfile                                # For local Docker testing
├── build.sh                                  # Used in Docker build
├── requirements.txt
├── pytest.ini
└── .gitignore

## Contributing
**Contributions are welcome!**
- Fork the repository
- Create a feature branch (git checkout -b feature/amazing-feature)
- Commit your changes (git commit -m 'Add amazing feature')
- Push to the branch (git push origin feature/amazing-feature)
- Open a Pull Request

**Built with ❤️ by @bhanuprasad0722**
