import logging
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token
)
from .models import db, Product, User


logging.basicConfig(level=logging.INFO)

main = Blueprint('main', __name__)

# Home route
@main.route('/')
def home():
    return jsonify({"message": "Welcome to Inventory API!"})

# POST /products - Create a new product
@main.route('/products', methods=['POST'])
@jwt_required()
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
@jwt_required()
def get_products():
    products = Product.query.all()
    product_list = [
        {"id": p.id, "name": p.name, "price": p.price, "quantity": p.quantity}
        for p in products
    ]
    return jsonify(product_list)

# GET /products/<id> - Get single product
@main.route('/products/<int:id>', methods=['GET'])
@jwt_required()
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
@jwt_required()
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    

    data = request.get_json()
    logging.info(f"Received data: {data}")


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
@jwt_required()
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"}), 200



# USER REGISTRATION (POST)

@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate fields
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "username, email, and password are required"}), 400

    # Check if username exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400

    # Check if email exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 400

    # Create new user
    new_user = User(
    username=data["username"],
    email=data["email"],
)

    new_user.set_password(data['password'])   # using model function

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201





# POST /login

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Missing username or password"}), 400

    user = User.query.filter_by(username=data["username"]).first()

    if not user or not check_password_hash(user.password_hash, data["password"]):
        return jsonify({"error": "Invalid username or password"}), 401

    # Create JWT token
    access_token = create_access_token(identity=str(user.id))

    return jsonify({"token": access_token}), 200


@main.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([
        {
            "id": u.id,
            "username": u.username,
            "email": u.email
        }
        for u in users
    ])


@main.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    })


@main.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()

    if "email" in data:
        user.email = data["email"]

    if "password" in data:
        user.set_password(data["password"])

    db.session.commit()

    return jsonify({"message": "User updated successfully"})



@main.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"})
