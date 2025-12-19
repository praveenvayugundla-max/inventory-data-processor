from abc import ABC, abstractmethod

class PriceDecorator(ABC):
    """
    Abstract Decorator class
    """

    def __init__(self, price):
        self.price = price

    @abstractmethod
    def get_price(self):
        pass
