import firebase_admin
from firebase_admin import credentials, auth, firestore
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def initialize_firebase():
    """Initialize Firebase Admin SDK with credentials."""
    try:
        # Get the path to the service account key file from environment variable
        cred_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH')
        
        if not cred_path:
            raise ValueError("FIREBASE_SERVICE_ACCOUNT_PATH environment variable is not set")
        
        # Initialize Firebase Admin SDK
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        
        # Initialize Firestore
        db = firestore.client()
        
        return db
    except Exception as e:
        print(f"Error initializing Firebase: {str(e)}")
        raise

def get_firestore():
    """Get Firestore database instance."""
    return firestore.client()

def verify_token(token):
    """Verify Firebase ID token."""
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        print(f"Error verifying token: {str(e)}")
        return None 