from abc import ABC, abstractmethod
from typing import Protocol


class Price(Protocol):
    def get_price(self) -> float:
        ...


class PriceDecorator(ABC):
    def __init__(self, price: Price):
        self.price = price

    @abstractmethod
    def get_price(self) -> float:
        pass
