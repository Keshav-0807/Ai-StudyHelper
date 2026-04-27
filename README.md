# AI Study Helper

AI Study Helper is a comprehensive web application designed to enhance the learning experience by automatically generating multiple-choice quizzes from uploaded study materials. It leverages the power of Google's Gemini API to create intelligent and context-aware questions.

## Features

* **User Authentication:** Secure registration and login functionality using JWT.
* **Document Upload & Quiz Generation:** Upload your study materials and automatically generate multiple-choice quizzes using the Gemini API.
* **Interactive Quiz Interface:** Take the generated quizzes with a responsive and user-friendly interface. Includes a "Clear Response" feature to reset answers.
* **Results Tracking:** View detailed results after completing a quiz.
* **User Profile & History:** Keep track of past quizzes and monitor your progress over time.

## Project Structure

The project is divided into two main components:

* `frontend/`: Contains the user interface built with HTML, CSS, Vanilla JavaScript, and Vite.
* `backend/`: Contains the REST API built with Python, Flask, and SQLAlchemy.

## Prerequisites

* Python 3.8+
* Node.js and npm

## Getting Started

### 1. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Open the `.env` file and fill in your `GEMINI_API_KEY` and `JWT_SECRET_KEY`.
4. Run the Flask development server:
   ```bash
   python app.py
   ```
   The backend API will start running on `http://localhost:5000`.

### 2. Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install the required Node dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   The frontend application will start running on `http://localhost:8000`.

## API Endpoints Overview

* **Authentication:**
  * `POST /register`: Register a new user
  * `POST /login`: Log in an existing user
  * `POST /verify`: Verify JWT token
  * `POST /refresh`: Refresh access token
  * `DELETE /account`: Delete user account
* **Quizzes:**
  * `POST /upload`: Upload a document and generate a quiz
* **Results:**
  * `POST /submit-result`: Submit quiz answers
  * `GET /results-data`: Get all results for the logged-in user
  * `GET /results-data/<id>`: Get a specific result by ID
