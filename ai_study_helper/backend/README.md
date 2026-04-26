# AI Study Helper

A Flask web application that generates multiple-choice quizzes from uploaded documents using the Gemini 2.5 Flash API.

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Open .env and fill in GEMINI_API_KEY and JWT_SECRET_KEY
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open http://localhost:5000 in your browser.
