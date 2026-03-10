# Mini Online Store

This Django project connects to Firebase Firestore and (optionally) Firebase Authentication.
The `store` app contains views for browsing products, a session‑based shopping cart, and a
checkout that records orders in Firestore.

## Setup

1. Install requirements (Django, firebase-admin, etc.):
   ```bash
   pip install django firebase-admin
   ```

2. Make migrations for the local `Product` model (optional if you're only using Firestore):
   ```bash
   python manage.py makemigrations store
   python manage.py migrate
   ```

3. Configure your Firebase service account key by placing the JSON file path in
   `store/firebase.py` (already done) and ensure the credentials file exists.

4. Populate the `Products` collection in Firestore with documents matching the schema
   described in `store/FIRESTORE_STRUCTURE.md`.

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Visit <http://127.0.0.1:8000/> to browse products. The site uses Bootstrap
   via CDN and is responsive by default.

## Features

- **Product fields**: name, price, description, stock, category, image_url.
- **Product detail** page with quantity selector and add-to-cart button.
- **Cart system** held in Django session; can update quantities or remove items.
- **Checkout** form that saves the order to Firestore and clears the cart.
- **Authentication (optional)**: sample login view expecting a Firebase ID token.
- **Responsive frontend** using Bootstrap.

## Extending

- You can add user accounts and link orders to `request.session['uid']` once
  authentication is wired up.
- A local `Product` model exists if you'd like to synchronize Firestore data into
  your SQL database, or for use in the Django admin.

See `store/FIRESTORE_STRUCTURE.md` for Firestore document examples.
