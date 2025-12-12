from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .models import db, Category, Product

category_bp = Blueprint("category", __name__, url_prefix="/categories")



# CREATE CATEGORY

@category_bp.route("/", methods=["POST"])
@jwt_required()
def create_category():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Category name is required"}), 400

    if Category.query.filter_by(name=data["name"]).first():
        return jsonify({"error": "Category already exists"}), 400

    new_category = Category(name=data["name"])

    try:
        db.session.add(new_category)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500

    return jsonify({"message": "Category created", "id": new_category.id}), 201


# GET ALL CATEGORIES

@category_bp.route("/", methods=["GET"])
@jwt_required()
def get_categories():
    categories = Category.query.all()
    return jsonify([{"id": c.id, "name": c.name} for c in categories])


# GET SINGLE CATEGORY

@category_bp.route("/<int:category_id>", methods=["GET"])
@jwt_required()
def get_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    return jsonify({
        "id": category.id,
        "name": category.name,
        "products": [
            {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "quantity": p.quantity
            }
            for p in category.products
        ]
    })



# UPDATE CATEGORY

@category_bp.route("/<int:category_id>", methods=["PUT"])
@jwt_required()
def update_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    data = request.get_json()

    if "name" in data:
        category.name = data["name"]

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Failed to update category"}), 500

    return jsonify({"message": "Category updated"})


# DELETE CATEGORY

@category_bp.route("/<int:category_id>", methods=["DELETE"])
@jwt_required()
def delete_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    try:
        db.session.delete(category)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Failed to delete category"}), 500

    return jsonify({"message": "Category deleted"})


# ASSIGN PRODUCT → CATEGORY

@category_bp.route("/assign", methods=["POST"])
@jwt_required()
def assign_product():
    data = request.get_json()

    if "product_id" not in data or "category_id" not in data:
        return jsonify({"error": "product_id and category_id are required"}), 400

    # Single combined DB call approach
    product = Product.query.get(data["product_id"])
    category = Category.query.get(data["category_id"])

    if not product:
        return jsonify({"error": "Product not found"}), 404
    if not category:
        return jsonify({"error": "Category not found"}), 404

    product.category_id = category.id

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Failed to assign product"}), 500

    return jsonify({"message": "Product assigned to category"})
