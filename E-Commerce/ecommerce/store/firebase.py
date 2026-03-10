import firebase_admin
from firebase_admin import credentials, firestore
import os

# Get the directory where this file is located
base_dir = os.path.dirname(os.path.abspath(__file__))
firebase_key_path = os.path.join(base_dir, 'e-commerce-aa53b-firebase-adminsdk-fbsvc-8ab0cf2976.json')

# Also check environment variable
firebase_key_path = os.environ.get('FIREBASE_KEY_PATH', firebase_key_path)

cred = credentials.Certificate(firebase_key_path)

# Initialize app (only do this once)
firebase_admin.initialize_app(cred)

# Create Firestore client
db = firestore.client()
