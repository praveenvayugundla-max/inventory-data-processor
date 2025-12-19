from .decorators import PriceDecorator, Price


class DiscountDecorator(PriceDecorator):
    """
    Applies a percentage discount to the base price
    """

    def __init__(self, price: Price, discount_percent: float):
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Discount percent must be between 0 and 100")

        super().__init__(price)
        self.discount_percent = discount_percent

    def get_price(self) -> float:
        base_price = self.price.get_price()
        discount_amount = base_price * (self.discount_percent / 100)
        return base_price - discount_amount
