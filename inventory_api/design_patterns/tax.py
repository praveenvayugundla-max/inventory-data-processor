from .decorators import PriceDecorator


class TaxDecorator(PriceDecorator):
    """
    Applies tax percentage on the base price
    """

    def __init__(self, price, tax_percent: float):
        super().__init__(price)
        self.tax_percent = tax_percent

    def get_price(self) -> float:
        base_price = self.price.get_price()
        tax_amount = base_price * (self.tax_percent / 100)
        return base_price + tax_amount
