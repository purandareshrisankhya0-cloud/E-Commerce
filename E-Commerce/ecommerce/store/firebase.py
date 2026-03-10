import firebase_admin
from firebase_admin import credentials, firestore
import os
from pathlib import Path

# Initialize Firebase variables
db = None

def initialize_firebase():
    """
    Initialize Firebase - works locally, in Codespace, and production.
    Set FIREBASE_KEY_PATH environment variable to override automatic detection.
    """
    global db
    
    # Get the store app directory
    store_dir = Path(__file__).resolve().parent
    
    # Check for Codespace common paths
    codespace_paths = [
        '/workspaces/E-Commerce/E-Commerce/ecommerce/store',
        '/workspaces/E-Commerce/ecommerce/store',
        os.environ.get('CODESPACE_WORKSPACE_PATH', '') + '/E-Commerce/ecommerce/store' if os.environ.get('CODESPACE_WORKSPACE_PATH') else None,
    ]
    
    # Check multiple possible locations for the Firebase key file
    possible_paths = [
        # 1. Same directory as this file (store folder)
        store_dir / 'e-commerce-aa53b-firebase-adminsdk-fbsvc-8ab0cf2976.json',
    ]
    
    # Add Codespace paths
    for codespace_path in codespace_paths:
        if codespace_path:
            possible_paths.append(Path(codespace_path) / 'e-commerce-aa53b-firebase-adminsdk-fbsvc-8ab0cf2976.json')
    
    # Add environment variable path (highest priority)
    env_path = os.environ.get('FIREBASE_KEY_PATH', '')
    if env_path:
        possible_paths.append(env_path)
    
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
        print("Set FIREBASE_KEY_PATH environment variable or ensure JSON file exists.")

# Initialize Firebase on module import
initialize_firebase()
