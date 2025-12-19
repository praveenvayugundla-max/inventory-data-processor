from .decorators import PriceDecorator


class DiscountDecorator(PriceDecorator):
    """
    Applies a percentage discount to the base price
    """

    def __init__(self, price, discount_percent: float):
        super().__init__(price)
        self.discount_percent = discount_percent

    def get_price(self) -> float:
        base_price = self.price.get_price()
        discount_amount = base_price * (self.discount_percent / 100)
        return base_price - discount_amount
