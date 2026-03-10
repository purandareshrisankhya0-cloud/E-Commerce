import firebase_admin
from firebase_admin import credentials, firestore
import os
from pathlib import Path

# Get the project root directory (parent of the store app)
# This works both locally and in Codespace
project_root = Path(__file__).resolve().parent.parent.parent

# Check multiple possible locations for the Firebase key file
possible_paths = [
    os.path.join(os.path.dirname(__file__), 'e-commerce-aa53b-firebase-adminsdk-fbsvc-8ab0cf2976.json'),
    project_root / 'store' / 'e-commerce-aa53b-firebase-adminsdk-fbsvc-8ab0cf2976.json',
    os.environ.get('FIREBASE_KEY_PATH', ''),
]

# Find the first valid path
firebase_key_path = None
for path in possible_paths:
    if path and os.path.exists(path):
        firebase_key_path = path
        break

if firebase_key_path:
    cred = credentials.Certificate(firebase_key_path)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
else:
    # Log warning but don't crash - Firebase may not be configured
    print("WARNING: Firebase credentials not found. Set FIREBASE_KEY_PATH environment variable or ensure JSON file exists.")
