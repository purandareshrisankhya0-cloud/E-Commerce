# E-Commerce Project

## Overview

Django-based mini online store with Firebase Firestore backend for products and orders. Features product browsing, session-based shopping cart, checkout (saves to Firestore), and optional Firebase Authentication. Responsive frontend using Bootstrap CDN.

**Tech Stack**:

- Backend: Django 6.0.2
- Database: Firebase Firestore (primary), optional SQLite/Django models
- Auth: Firebase Admin SDK (server-side token verification)
- Frontend: Django templates, Bootstrap 5, custom CSS

## File Structure

```
E-Commerce/
├── README.md                 # This file
├── requirements.txt          # Python deps (Django>=4.2)
├── .gitignore
├── Front_end/                # Placeholder frontend script (Front_end.py)
└── ecommerce/                # Django project
    ├── manage.py
    ├── ecommerce/            # Project settings/urls
    │   ├── settings.py       # Firebase config/env vars
    │   ├── urls.py
    │   └── ...
    └── store/                # Main app
        ├── models.py         # Optional local Product model
        ├── views.py          # Core logic (home, cart, checkout)
        ├── firebase.py       # Firestore init/service account detection
        ├── FIRESTORE_STRUCTURE.md  # DB schema
        ├── urls.py
        ├── admin.py
        ├── static/store/css/styles.css
        ├── templates/store/   # HTML: base.html, home.html, cart.html, etc.
        ├── fixtures/sample_products.json
        └── migrations/
```

## Prerequisites

- Python 3.10+
- Firebase project with Firestore enabled
- Firebase service account JSON key: `e-commerce-aa53b-firebase-adminsdk-fbsvc-8ab0cf2976.json` (place in `ecommerce/store/` or set `FIREBASE_KEY_PATH` env var)
- Populate Firestore `Products` collection (see FIRESTORE_STRUCTURE.md)

## Setup

1. **Virtual Environment** (recommended):

   ```
   cd ecommerce
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

2. **Install Dependencies**:

   ```
   pip install -r ../requirements.txt
   pip install firebase-admin
   ```

3. **Firebase Config** (auto-detected, but verify):
   - Edit `ecommerce/store/firebase.py` if key path changes.
   - Set env vars in `ecommerce/ecommerce/settings.py` (FIREBASE\_\* keys).

4. **Django Migrations** (optional, for local models/admin):

   ```
   python manage.py makemigrations store
   python manage.py migrate
   ```

5. **Load Sample Data** (optional):
   ```
   python manage.py loaddata store/fixtures/sample_products.json
   ```

## Running the Project

```
cd ecommerce
python manage.py runserver
```

- Visit `http://127.0.0.1:8000/`
- Products load from Firestore `Products` collection
- Cart uses Django sessions

**Frontend Placeholder**:

```
cd ../Front_end
python Front_end.py  # Prints welcome message
```

## How It Works

1. **Home (`/`)**: Fetches all `Products` from Firestore → renders `store/home.html`.
2. **Product Detail (`/product/<id>/`)**: Loads specific product → add to cart form.
3. **Cart (`/cart/`)**: Session items → update qty/remove → totals.
4. **Checkout (`/checkout/`)**: Form → saves `Order` doc to Firestore → clears cart.
5. **Login (`/login/`)**: POST Firebase ID token → verifies → sets session `uid`.

**Connections**:

- Django views → `firebase.py` → Firestore client (reads Products, writes Orders).
- Service account auth (no user password storage).
- Error handling if DB not connected.

See `store/FIRESTORE_STRUCTURE.md` for exact JSON schemas (Products/Orders).

## Features

- Responsive design (Bootstrap)
- Image/price/stock display
- Qty updates in cart
- Order persistence in Firestore
- Optional Django Admin (`/admin/`)

## Deployment

- Production: Use Gunicorn/Waitress + static collect (`python manage.py collectstatic`).
- Set `DEBUG=False`, proper `ALLOWED_HOSTS`.
- Codespaces/Local: Firebase key auto-detected.

## Troubleshooting

- **Firebase not connected**: Check key file path/permissions. Run `python -c "from store import firebase; print(firebase.db)"`.
- **No products**: Populate Firestore `Products`.
- **Migrations**: Skip if pure Firestore.
- Env vars: Use `.env` + `python-dotenv`.

## GitHub

Changes committed to `blackboxai/readme-update` branch. See PR for details.
