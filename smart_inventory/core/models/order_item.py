"""OrderItem model — a single line item inside an Order."""

from __future__ import annotations

from typing import TYPE_CHECKING

from core.exceptions import InvalidQuantityException

if TYPE_CHECKING:
    from core.models.product import Product


class OrderItem:
    """One line in an order: a product and the quantity ordered.

    Attributes:
        product: The product being ordered.
        quantity: Number of units ordered (must be > 0).
    """

    def __init__(self, product: "Product", quantity: int) -> None:
        if quantity <= 0:
            raise InvalidQuantityException(quantity=quantity)
        self.product: "Product" = product
        self.quantity: int = quantity

    def get_subtotal(self) -> float:
        """Return the subtotal for this line item.

        Returns:
            product.price * quantity
        """
        return self.product.price * self.quantity

    def __repr__(self) -> str:
        return (
            f"OrderItem(product='{self.product.name}', "
            f"qty={self.quantity}, subtotal={self.get_subtotal():.2f})"
        )

    def __str__(self) -> str:
        return f"{self.quantity}x {self.product.name} = ${self.get_subtotal():.2f}"
