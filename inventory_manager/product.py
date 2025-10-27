from __future__ import annotations
from typing import Any, Dict
from pydantic import BaseModel, Field, ValidationError, conint, confloat

# ✅ Validation schema (matches your Week 1 CSV)
class ProductSchema(BaseModel):
    product_id: str | None = Field(None, alias="product_id")
    item_name: str = Field(..., alias="Item Name")
    quantity: conint(ge=0) = Field(..., alias="Quantity")
    price: confloat(gt=0) = Field(..., alias="Price")
    type: str | None = Field(None, alias="type")  # optional field for factory use

    class Config:
        allow_population_by_field_name = True


# ✅ Base class
class Product:
    """Base product class demonstrating encapsulation and behavior."""
    def __init__(self, product_id: str | None, name: str, quantity: int, price: float):
        self._product_id = product_id
        self._name = name
        self.__price = price  # private
        self.quantity = quantity

    def get_price(self) -> float:
        return self.__price

    def set_price(self, new_price: float) -> None:
        if new_price <= 0:
            raise ValueError("Price must be positive")
        self.__price = new_price

    @property
    def name(self) -> str:
        return self._name

    def total_value(self) -> float:
        return self.quantity * self.__price

    def get_description(self) -> str:
        return f"{self._name} | Qty: {self.quantity} | Price: {self.__price}"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Product":
        """Validate dict using Pydantic and return a Product."""
        validated = ProductSchema(**data)
        return cls(validated.product_id, validated.item_name, validated.quantity, validated.price)


# ✅ Specialized versions for OCP (Open/Closed Principle)
class FoodProduct(Product):
    def __init__(self, product_id: str | None, name: str, quantity: int, price: float, expiry_date: str | None = None):
        super().__init__(product_id, name, quantity, price)
        self.expiry_date = expiry_date

    def get_description(self) -> str:
        return f"{self.name} | Qty: {self.quantity} | Expires: {self.expiry_date or 'N/A'}"


class ElectronicProduct(Product):
    def __init__(self, product_id: str | None, name: str, quantity: int, price: float, warranty_months: int | None = None):
        super().__init__(product_id, name, quantity, price)
        self.warranty_months = warranty_months

    def get_description(self) -> str:
        return f"{self.name} | Qty: {self.quantity} | Warranty: {self.warranty_months or 'N/A'}"
