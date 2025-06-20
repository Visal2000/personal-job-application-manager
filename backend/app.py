# app.py
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

# Create the Flask app
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

# Initialize JWT
jwt = JWTManager(app)

# Import blueprints AFTER app is created
from auth import auth_bp
from jobs import jobs_bp

# Register routes
app.register_blueprint(auth_bp)
app.register_blueprint(jobs_bp)

if __name__ == '__main__':
    app.run(debug=True)
