import firebase_admin
from firebase_admin import credentials, auth, firestore
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

def get_user_by_email(email):
    """Get user by email."""
    try:
        user = auth.get_user_by_email(email)
        return user
    except Exception as e:
        print(f"Error getting user by email: {str(e)}")
        return None

def update_user_profile(uid, data):
    """Update user profile in Firestore."""
    try:
        db = get_firestore()
        user_ref = db.collection('users').document(uid)
        user_ref.update(data)
        return True
    except Exception as e:
        print(f"Error updating user profile: {str(e)}")
        return False

def send_email(to_email, subject, body):
    """Send email using SMTP."""
    try:
        # Get email configuration from environment variables
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = int(os.getenv('SMTP_PORT', 587))
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')
        from_email = os.getenv('FROM_EMAIL')

        if not all([smtp_server, smtp_username, smtp_password, from_email]):
            raise ValueError("SMTP configuration is incomplete")

        # Create message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # Add body
        msg.attach(MIMEText(body, 'html'))

        # Create SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Send email
        server.send_message(msg)
        server.quit()

        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False 