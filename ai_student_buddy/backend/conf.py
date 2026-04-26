from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from argon2 import PasswordHasher
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
from datetime import timedelta
import google.generativeai as genai

app = Flask(__name__)
CORS(app)
load_dotenv()

api = Api(app)
db = SQLAlchemy()
ag_ph = PasswordHasher()
jwt = JWTManager(app)

JWT_SETTINGS = {
    "jwt_key": os.environ.get("JWT_SECRET_KEY"),
    "access_exp": timedelta(minutes=5),
    "refresh_exp": timedelta(days=30),
}

# ALWAYS use gemini-2.5-flash
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
gen_model = genai.GenerativeModel('gemini-2.5-flash')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///student_buddy.db"
app.config["JWT_SECRET_KEY"] = JWT_SETTINGS.get("jwt_key")
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10MB upload limit
app.config["UPLOAD_FOLDER"] = "uploads"

db.init_app(app)
