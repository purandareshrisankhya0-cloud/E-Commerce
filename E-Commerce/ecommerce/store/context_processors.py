"""
Context processor to make Firebase config available in all templates
"""
from django.conf import settings

def firebase_config(request):
    """
    Adds Firebase configuration to the template context.
    Set these as environment variables in your Codespace or .env file:
    - FIREBASE_API_KEY
    - FIREBASE_AUTH_DOMAIN
    - FIREBASE_PROJECT_ID
    - FIREBASE_STORAGE_BUCKET
    - FIREBASE_MESSAGING_SENDER_ID
    - FIREBASE_APP_ID
    """
    return {
        'firebase_config': settings.FIREBASE_CONFIG,
    }

