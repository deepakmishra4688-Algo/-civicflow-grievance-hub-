from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///grievances.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Mail Configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', True)
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

from extensions import db, mail

db.init_app(app)
mail.init_app(app)

# Import after extensions initialization
import models
from routes import complaints_bp, auth_bp, admin_bp
from classifier import classify_complaint

app.register_blueprint(complaints_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'API running', 'timestamp': datetime.now().isoformat()}), 200

@app.route('/api/classify', methods=['POST'])
def classify():
    data = request.get_json()
    text = data.get('text', '')
    result = classify_complaint(text)
    return jsonify(result), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    debug_mode = os.getenv('FLASK_ENV', 'production') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
