from flask import Blueprint, jsonify, request
from .models import db, Product
from app.models import User, db
import jwt
import datetime
from flask import request
from functools import wraps
from flask import current_app
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash



def require_jwt(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Token must come from Authorization header
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            # Expecting: Bearer <token>
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            decoded = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )
            # Store decoded user info for later use
            request.user = decoded

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated




main = Blueprint('main', __name__)

# Home route
@main.route('/')
def home():
    return jsonify({"message": "Welcome to Inventory API!"})

# POST /products - Create a new product
@main.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()

    # Validation
    if not data or 'name' not in data or 'price' not in data or 'quantity' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    if data['price'] <= 0:
        return jsonify({"error": "Price must be greater than 0"}), 400

    if not isinstance(data['quantity'], int) or data['quantity'] < 0:
        return jsonify({"error": "Quantity must be a non-negative integer"}), 400

    new_product = Product(
        name=data['name'],
        price=data['price'],
        quantity=data['quantity']
    )

    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added successfully!"}), 201

# GET /products - Get all products
@main.route('/products', methods=['GET'])
@require_jwt
def get_products():
    products = Product.query.all()
    product_list = [
        {"id": p.id, "name": p.name, "price": p.price, "quantity": p.quantity}
        for p in products
    ]
    return jsonify(product_list)

# GET /products/<id> - Get single product
@main.route('/products/<int:id>', methods=['GET'])
@require_jwt
def get_product_by_id(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    })

# PUT /products/<id> - Update product details
@main.route('/products/<int:id>', methods=['PUT'])
@require_jwt
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()

    if 'name' in data:
        product.name = data['name']
    if 'price' in data:
        if data['price'] <= 0:
            return jsonify({"error": "Price must be positive"}), 400
        product.price = data['price']
    if 'quantity' in data:
        if not isinstance(data['quantity'], int) or data['quantity'] < 0:
            return jsonify({"error": "Quantity must be a non-negative integer"}), 400
        product.quantity = data['quantity']

    db.session.commit()
    return jsonify({"message": "Product updated successfully"}), 200


# DELETE /products/<id> - Delete product
@main.route('/products/<int:id>', methods=['DELETE'])
@require_jwt
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"}), 200


@main.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Basic validation
    if not username or not email or not password:
        return jsonify({"error": "username, email, and password are required"}), 400

    # Check if user already exists
    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing_user:
        return jsonify({"error": "User with this username or email already exists"}), 400

    # Hash the password
    hashed_password = generate_password_hash(password)

    new_user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
        role="staff"   # default role for Week-5 Day-1
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201


@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    # verify hashed password
    if not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid username or password"}), 401

    # Create JWT token
    token = jwt.encode(
        {
            "user_id": user.id,
            "username": user.username,
            "role": user.role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return jsonify({"token": token}), 200

