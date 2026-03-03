import firebase_admin
from firebase_admin import credentials, firestore

# Path to your downloaded Firebase service account key JSON
cred = credentials.Certificate('D:\Shrisankhya_project\ecommerce\e-commerce-aa53b-firebase-adminsdk-fbsvc-86292d5669.json')

# Initialize app (only do this once)
firebase_admin.initialize_app(cred)

# Create Firestore client
db = firestore.client()