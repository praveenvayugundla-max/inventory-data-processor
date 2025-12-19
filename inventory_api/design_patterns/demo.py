from .price import BasePrice
from .discount import DiscountDecorator
from .tax import TaxDecorator


def run_demo() -> None:
    base_price = BasePrice(1000)
    print("Base Price:", base_price.get_price())

    discounted_price = DiscountDecorator(base_price, discount_percent=10)
    print("After 10% Discount:", discounted_price.get_price())

    final_price = TaxDecorator(discounted_price, tax_percent=18)
    print("After 18% Tax:", final_price.get_price())


if __name__ == "__main__":
    run_demo()
