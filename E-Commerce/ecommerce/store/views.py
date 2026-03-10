from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib import messages

from . import firebase
from firebase_admin import auth


# helper to access cart stored in session

def _get_cart(request):
    return request.session.setdefault('cart', {})


def _save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def home(request):
    # Check if Firebase is initialized
    if firebase.db is None:
        messages.error(request, 'Database not connected. Please check Firebase configuration.')
        return render(request, 'store/home.html', {'products': []})
    
    # Fetch all products from Firestore
    products_ref = firebase.db.collection('Products').stream()
    products = []
    for doc in products_ref:
        data = doc.to_dict()
        data['id'] = doc.id
        products.append(data)

    return render(request, 'store/home.html', {'products': products})


def product_detail(request, product_id):
    if firebase.db is None:
        messages.error(request, 'Database not connected.')
        return redirect('home')
    
    doc = firebase.db.collection('Products').document(product_id).get()
    if not doc.exists:
        messages.error(request, 'Product not found.')
        return redirect('home')
    product = doc.to_dict()
    product['id'] = doc.id
    return render(request, 'store/product_detail.html', {'product': product})


@require_POST
def add_to_cart(request, product_id):
    if firebase.db is None:
        messages.error(request, 'Database not connected.')
        return redirect('home')
    
    quantity = int(request.POST.get('quantity', 1))
    doc = firebase.db.collection('Products').document(product_id).get()
    if not doc.exists:
        messages.error(request, 'Product does not exist.')
        return redirect('home')

    product = doc.to_dict()
    cart = _get_cart(request)
    if product_id in cart:
        cart[product_id]['quantity'] += quantity
    else:
        cart[product_id] = {
            'name': product.get('name'),
            'price': float(product.get('price', 0)),
            'quantity': quantity,
            'image_url': product.get('image_url', ''),
        }
    _save_cart(request, cart)
    messages.success(request, f"Added {quantity} x {product.get('name')} to cart.")
    return redirect('cart')


def cart_view(request):
    cart = _get_cart(request)
    items = []
    total = 0.0
    for pid, item in cart.items():
        subtotal = item['price'] * item['quantity']
        total += subtotal
        items.append({'id': pid, **item, 'subtotal': subtotal})
    return render(request, 'store/cart.html', {'cart_items': items, 'total': total})


@require_POST
def update_cart(request):
    cart = _get_cart(request)
    for pid, item in list(cart.items()):
        qty = int(request.POST.get(f'quantity_{pid}', item['quantity']))
        if qty <= 0:
            del cart[pid]
        else:
            cart[pid]['quantity'] = qty
    _save_cart(request, cart)
    messages.success(request, 'Cart updated.')
    return redirect('cart')


@require_POST
def checkout(request):
    cart = _get_cart(request)
    if not cart:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')

    if firebase.db is None:
        messages.error(request, 'Database not connected. Cannot process order.')
        return redirect('cart')

    # get customer info from form or session
    name = request.POST.get('name', '')
    email = request.POST.get('email', '')
    # billing address
    address = request.POST.get('address', '')
    city = request.POST.get('city', '')
    state = request.POST.get('state', '')
    zipcode = request.POST.get('zipcode', '')
    country = request.POST.get('country', '')
    
    from firebase_admin import firestore as _firestore

    order_data = {
        'items': cart,
        'total': sum(item['price'] * item['quantity'] for item in cart.values()),
        'name': name,
        'email': email,
        'address': {
            'street': address,
            'city': city,
            'state': state,
            'zipcode': zipcode,
            'country': country,
        },
        'status': 'pending',
        'created_at': _firestore.SERVER_TIMESTAMP,
    }
    firebase.db.collection('Orders').add(order_data)
    # clear cart
    request.session['cart'] = {}
    messages.success(request, 'Order placed successfully!')
    return redirect('home')


def login_view(request):
    # expecting an idToken from client-side Firebase SDK
    if request.method == 'POST':
        id_token = request.POST.get('idToken')
        try:
            decoded = auth.verify_id_token(id_token)
            request.session['uid'] = decoded['uid']
            messages.success(request, 'Logged in successfully.')
            return redirect('home')
        except Exception as e:
            messages.error(request, 'Authentication failed. Firebase may not be configured.')
    return render(request, 'store/login.html')


def logout_view(request):
    request.session.pop('uid', None)
    messages.info(request, 'Logged out.')
    return redirect('home')
