"""Order model — represents a customer order containing line items."""

from __future__ import annotations

from datetime import datetime
from typing import List, TYPE_CHECKING

from core.exceptions import InvalidQuantityException, OutOfStockException
from core.models.order_item import OrderItem

if TYPE_CHECKING:
    from core.models.customer import Customer
    from core.models.product import Product


class Order:
    """A customer order in the Smart Inventory system.

    Attributes:
        id: Unique identifier.
        customer: The customer who placed the order.
        order_date: Timestamp of creation.
        items: List of :class:`OrderItem` objects.
    """

    def __init__(
        self,
        id: int,
        customer: "Customer",
        order_date: datetime | None = None,
    ) -> None:
        self.id: int = id
        self.customer: "Customer" = customer
        self.order_date: datetime = order_date or datetime.now()
        self.items: List[OrderItem] = []

    def add_item(self, product: "Product", quantity: int) -> OrderItem:
        """Add a product to the order.

        This also removes the requested quantity from the product's stock.

        Args:
            product: The product to add.
            quantity: Number of units (must be > 0).

        Returns:
            The created :class:`OrderItem`.

        Raises:
            InvalidQuantityException: If *quantity* is not positive.
            OutOfStockException: If *quantity* exceeds available stock.
        """
        if quantity <= 0:
            raise InvalidQuantityException(quantity=quantity)
        # This will raise OutOfStockException if not enough stock
        product.remove_stock(quantity)
        item = OrderItem(product, quantity)
        self.items.append(item)
        return item

    def calculate_total(self) -> float:
        """Return the grand total for the order.

        Returns:
            Sum of all item subtotals.
        """
        return sum(item.get_subtotal() for item in self.items)

    def __repr__(self) -> str:
        return (
            f"Order(id={self.id}, customer='{self.customer.name}', "
            f"items={len(self.items)}, total={self.calculate_total():.2f})"
        )

    def __str__(self) -> str:
        lines = [
            f"Order #{self.id} — {self.customer.name} "
            f"({self.order_date:%Y-%m-%d %H:%M})",
            "-" * 40,
        ]
        for item in self.items:
            lines.append(f"  {item}")
        lines.append("-" * 40)
        lines.append(f"  TOTAL: ${self.calculate_total():.2f}")
        return "\n".join(lines)
