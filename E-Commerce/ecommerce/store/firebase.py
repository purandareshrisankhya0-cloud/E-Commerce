import firebase_admin
from firebase_admin import credentials, firestore
import os
from pathlib import Path

# Initialize Firebase variables
db = None

def initialize_firebase():
    """
    Initialize Firebase - works both locally and in Codespace.
    Set FIREBASE_KEY_PATH environment variable to specify custom JSON key location.
    """
    global db
    
    # Get the store app directory
    store_dir = Path(__file__).resolve().parent
    
    # Check multiple possible locations for the Firebase key file
    possible_paths = [
        # 1. Same directory as this file (store folder)
        store_dir / 'e-commerce-aa53b-firebase-adminsdk-fbsvc-8ab0cf2976.json',
        # 2. Environment variable (highest priority)
        os.environ.get('FIREBASE_KEY_PATH', ''),
    ]
    
    # Filter and find the first valid path
    firebase_key_path = None
    for path in possible_paths:
        if path and os.path.exists(str(path)):
            firebase_key_path = str(path)
            break
    
    if firebase_key_path:
        try:
            cred = credentials.Certificate(firebase_key_path)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            print(f"Firebase initialized successfully with key: {firebase_key_path}")
        except Exception as e:
            print(f"Warning: Failed to initialize Firebase: {e}")
            db = None
    else:
        print("WARNING: Firebase credentials not found. Firebase features will be disabled.")
        print("Set FIREBASE_KEY_PATH environment variable or ensure JSON file exists in the store directory.")

# Initialize Firebase on module import
initialize_firebase()
