from __future__ import annotations
from typing import Dict, Any
from .product import Product, FoodProduct, ElectronicProduct, ProductSchema
from pydantic import ValidationError


class ProductFactory:
    @staticmethod
    def create(data: Dict[str, Any]) -> Product:
        """
        Creates a Product (or subclass) based on the 'type' field.
        data: one row of CSV data as a dictionary.
        """
        ptype = (data.get("type") or data.get("Type") or "").strip().lower()

        # Validate using Pydantic schema first
        validated = ProductSchema(**data)

        kwargs = {
            "product_id": getattr(validated, "product_id", None),
            "name": validated.item_name,
            "quantity": validated.quantity,
            "price": validated.price,
        }

        if ptype in ("food", "grocery"):
            kwargs["expiry_date"] = data.get("expiry_date")
            return FoodProduct(**kwargs)
        elif ptype in ("electronic", "electronics"):
            kwargs["warranty_months"] = (
                int(data.get("warranty_months")) if data.get("warranty_months") else None
            )
            return ElectronicProduct(**kwargs)
        else:
            return Product(**kwargs)
