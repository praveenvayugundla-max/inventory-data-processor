class BasePrice:
    def __init__(self, amount: float):
        if amount < 0:
            raise ValueError("Base price cannot be negative")
        self.amount = amount

    def get_price(self) -> float:
        return self.amount
