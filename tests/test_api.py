import pytest
from app import create_app, db
from app.models import Product

@pytest.fixture
def client():
    """Setup a fresh test client and database before each test."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # use in-memory DB for tests

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_home_route(client):
    """Check if home route works."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json() == {"message": "Welcome to Inventory API!"}


def test_add_product(client):
    """Test POST /products"""
    data = {"name": "Laptop", "price": 1000, "quantity": 10}
    response = client.post('/products', json=data)
    assert response.status_code == 201
    assert "Product added successfully" in response.get_json()["message"]


def test_get_products(client):
    """Test GET /products returns all products"""
    # add a sample product
    db.session.add(Product(name="Phone", price=500, quantity=5))
    db.session.commit()

    response = client.get('/products')
    assert response.status_code == 200
    products = response.get_json()
    assert isinstance(products, list)
    assert len(products) == 1
    assert products[0]["name"] == "Phone"


def test_get_product_by_id(client):
    """Test GET /products/<id>"""
    product = Product(name="Mouse", price=200, quantity=3)
    db.session.add(product)
    db.session.commit()

    response = client.get(f'/products/{product.id}')
    assert response.status_code == 200
    assert response.get_json()["name"] == "Mouse"


def test_update_product(client):
    """Test PUT /products/<id>"""
    product = Product(name="Keyboard", price=300, quantity=2)
    db.session.add(product)
    db.session.commit()

    update_data = {"price": 350, "quantity": 5}
    response = client.put(f'/products/{product.id}', json=update_data)
    assert response.status_code == 200
    assert "Product updated successfully" in response.get_json()["message"]

    updated_product = Product.query.get(product.id)
    assert updated_product.price == 350
    assert updated_product.quantity == 5


def test_delete_product(client):
    """Test DELETE /products/<id>"""
    product = Product(name="Charger", price=150, quantity=4)
    db.session.add(product)
    db.session.commit()

    response = client.delete(f'/products/{product.id}')
    assert response.status_code == 200
    assert "deleted" in response.get_json()["message"]

    deleted = Product.query.get(product.id)
    assert deleted is None
