from .decorators import PriceDecorator, Price


class TaxDecorator(PriceDecorator):
    """
    Applies tax percentage on the base price
    """

    def __init__(self, price: Price, tax_percent: float):
        if tax_percent < 0:
            raise ValueError("Tax percent cannot be negative")

        super().__init__(price)
        self.tax_percent = tax_percent

    def get_price(self) -> float:
        base_price = self.price.get_price()
        tax_amount = base_price * (self.tax_percent / 100)
        return base_price + tax_amount
