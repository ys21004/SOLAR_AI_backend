from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Import routes
from routes.maintenance_routes import maintenance_routes

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000"],  # Your React frontend URL
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type"]
        }
    })

    # Register blueprints
    app.register_blueprint(maintenance_routes, url_prefix='/api/maintenance')

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
