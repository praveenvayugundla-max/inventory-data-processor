import csv
from app import create_app, db
from app.models import Product

app = create_app()

with app.app_context():
    file_path = "data/inventory.csv"

    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Validation: ensure numeric conversion
            try:
                name = row['Name']
                quantity = int(row['Quantity'])
                price = float(row['Price'])
            except (KeyError, ValueError):
                print(f"Skipping invalid row: {row}")
                continue

            new_product = Product(name=name, price=price, quantity=quantity)
            db.session.add(new_product)

        db.session.commit()
        print("✅ CSV data migrated successfully into PostgreSQL database!")
