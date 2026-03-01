"""Custom exception classes for the Smart Inventory system.

These exceptions handle domain-specific error conditions such as
stock shortages, invalid email formats, and invalid quantities.
"""


class OutOfStockException(Exception):
    """Raised when an operation requires more stock than is available.

    Attributes:
        product_name: The name of the product that is out of stock.
        requested: The quantity that was requested.
        available: The quantity currently available.
    """

    def __init__(
        self,
        message: str = "Product is out of stock",
        product_name: str = "",
        requested: int = 0,
        available: int = 0,
    ) -> None:
        self.product_name = product_name
        self.requested = requested
        self.available = available
        if product_name:
            message = (
                f"Out of stock: '{product_name}' — "
                f"requested {requested}, available {available}"
            )
        super().__init__(message)


class InvalidEmailException(Exception):
    """Raised when a customer email address fails validation.

    Attributes:
        email: The invalid email address.
    """

    def __init__(
        self, message: str = "Invalid email address", email: str = ""
    ) -> None:
        self.email = email
        if email:
            message = f"Invalid email address: '{email}'"
        super().__init__(message)


class InvalidQuantityException(Exception):
    """Raised when a quantity value is not positive.

    Attributes:
        quantity: The invalid quantity value.
    """

    def __init__(
        self, message: str = "Quantity must be positive", quantity: int = 0
    ) -> None:
        self.quantity = quantity
        if quantity is not None:
            message = f"Invalid quantity: {quantity}. Quantity must be a positive integer."
        super().__init__(message)
