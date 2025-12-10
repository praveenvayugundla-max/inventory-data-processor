from flask import Blueprint, jsonify, request
from .models import db, Product

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
def get_products():
    products = Product.query.all()
    product_list = [
        {"id": p.id, "name": p.name, "price": p.price, "quantity": p.quantity}
        for p in products
    ]
    return jsonify(product_list)

# GET /products/<id> - Get single product
@main.route('/products/<int:id>', methods=['GET'])
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
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"}), 200
