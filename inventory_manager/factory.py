from inventory_manager.product import Product, FoodProduct, ElectronicProduct

class ProductFactory:
    """Factory to create Product objects based on raw data."""

    @staticmethod
    def create(row: dict) -> Product:
        name = row.get("Item Name", "").strip()
        quantity = int(row.get("Quantity", 0))
        price = float(row.get("Price", 0))
        category = row.get("Category", "").strip().lower()

        # 🥖 Food Product
        if category == "food" or "Expiry Date" in row:
            expiry = row.get("Expiry Date")
            return FoodProduct(None, name, quantity, price, expiry_date=expiry)

        # ⚡ Electronic Product
        elif category == "electronics" or "Warranty" in row:
            warranty = row.get("Warranty") or row.get("Warranty (months)")
            return ElectronicProduct(None, name, quantity, price, warranty_months=int(warranty))

        # 📦 Default Product
        return Product(None, name, quantity, price)
