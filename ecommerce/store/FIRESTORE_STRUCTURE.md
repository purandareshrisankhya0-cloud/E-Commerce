# Firestore Data Structure

To make the Django views above work you should populate your Firestore database with two collections:

## Products
Each document in the `Products` collection represents a product.
Example fields:

```json
{
  "name": "Red T-shirt",
  "price": 19.99,
  "description": "Comfortable cotton shirt in red.",
  "stock": 42,
  "category": "Apparel",
  "image_url": "https://example.com/images/red-shirt.jpg"
}
```

The document ID is used as `product_id` in the URLs; you can either let Firestore auto‑generate IDs or choose your own.

## Orders
When a user checks out, a new document is added to the `Orders` collection by the server.
The document has the following shape (fields are for guidance):

```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "items": {
    "abcd1234": {"name": "Red T-shirt", "price": 19.99, "quantity": 2, "image_url": "..."},
    "efgh5678": {"name": "Blue Jeans", "price": 49.95, "quantity": 1}
  },
  "total": 89.93,
  "status": "pending",
  "created_at": "2026-03-03T12:34:56Z"  // you can add a timestamp using Firestore serverTimestamp
}
```

You can add more fields such as `uid` if you are recording which authenticated user placed the order.

## Authentication
This example relies on Firebase Authentication on the client side. Your frontend should obtain an
ID token via one of the Firebase SDKs (JavaScript, Android, iOS) and POST it to `/login/`.
The server verifies the token using the Admin SDK and stores the user's `uid` in the Django session.

You do not need to pre‑populate anything in Firestore for auth, but ensure you have enabled
`Email/Password` (or any other) sign‑in method in the Firebase console.

---

Feel free to update or expand this document as your project grows.