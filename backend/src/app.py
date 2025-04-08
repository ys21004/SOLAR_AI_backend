import os
import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = str(Path(__file__).parent)
if src_path not in sys.path:
    sys.path.append(src_path)

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from firebase_admin import firestore

# Import routes and Firebase config
from routes.maintenance_routes import maintenance_routes
from firebase_config import initialize_firebase, get_firestore
from middleware.auth_middleware import require_auth

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",  # Allow all origins during development
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # Initialize Firebase
    try:
        db = initialize_firebase()
        print("Firebase initialized successfully")
    except Exception as e:
        print(f"Failed to initialize Firebase: {str(e)}")
        raise

    # Test route to verify Firebase connection
    @app.route('/api/test/firebase', methods=['GET'])
    def test_firebase():
        try:
            db = get_firestore()
            # Try to create a test document
            test_ref = db.collection('test').document('connection_test')
            test_ref.set({
                'timestamp': firestore.SERVER_TIMESTAMP,
                'status': 'success'
            })
            return jsonify({
                'status': 'success',
                'message': 'Firebase connection successful!'
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Firebase connection failed: {str(e)}'
            }), 500

    # Test route to verify Firebase Authentication
    @app.route('/api/test/auth', methods=['GET'])
    @require_auth
    def test_auth():
        return jsonify({
            'status': 'success',
            'message': 'Authentication successful!',
            'user': {
                'uid': request.user['uid'],
                'email': request.user.get('email', 'No email found')
            }
        })

    # Register blueprints
    app.register_blueprint(maintenance_routes, url_prefix='/api/maintenance')

    # Example authenticated route
    @app.route('/api/user/profile', methods=['GET'])
    @require_auth
    def get_user_profile():
        user_id = request.user['uid']
        db = get_firestore()
        
        # Get user document from Firestore
        user_doc = db.collection('users').document(user_id).get()
        
        if not user_doc.exists:
            return jsonify({
                'error': 'User profile not found',
                'status': 404
            }), 404
        
        return jsonify(user_doc.to_dict())

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            "error": "Resource not found",
            "status": 404
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "error": "Internal server error",
            "status": 500
        }), 500

    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            "status": "healthy",
            "service": "SolarAI Backend"
        })

    return app

def main():
    app = create_app()
    
    # Change the port to 5001
    port = int(os.getenv('PORT', 5001))  # Default to 5001 if not set
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.getenv('FLASK_ENV') == 'development'
    )

if __name__ == '__main__':
    main()
