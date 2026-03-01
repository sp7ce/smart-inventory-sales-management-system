"""Product model — represents a product in the inventory.

Handles stock management and valuation.
"""

from __future__ import annotations

from core.exceptions import InvalidQuantityException, OutOfStockException


class Product:
    """A product in the Smart Inventory system.

    Attributes:
        id: Unique identifier for the product.
        name: Human-readable product name.
        category: Product category (e.g. 'Electronics').
        price: Unit price (>= 0).
        quantity_in_stock: Current stock level (>= 0).
    """

    def __init__(
        self,
        id: int,
        name: str,
        category: str,
        price: float,
        quantity_in_stock: int = 0,
    ) -> None:
        self.id: int = id
        self.name: str = name
        self.category: str = category
        self.price: float = float(price)
        self.quantity_in_stock: int = int(quantity_in_stock)

    # ------------------------------------------------------------------
    # Stock management
    # ------------------------------------------------------------------

    def add_stock(self, qty: int) -> None:
        """Add *qty* units to stock.

        Args:
            qty: Number of units to add (must be > 0).

        Raises:
            InvalidQuantityException: If *qty* is not positive.
        """
        if qty <= 0:
            raise InvalidQuantityException(quantity=qty)
        self.quantity_in_stock += qty

    def remove_stock(self, qty: int) -> None:
        """Remove *qty* units from stock.

        Args:
            qty: Number of units to remove (must be > 0).

        Raises:
            InvalidQuantityException: If *qty* is not positive.
            OutOfStockException: If *qty* exceeds available stock.
        """
        if qty <= 0:
            raise InvalidQuantityException(quantity=qty)
        if qty > self.quantity_in_stock:
            raise OutOfStockException(
                product_name=self.name,
                requested=qty,
                available=self.quantity_in_stock,
            )
        self.quantity_in_stock -= qty

    def get_value_in_stock(self) -> float:
        """Return the total monetary value of current stock.

        Returns:
            price * quantity_in_stock
        """
        return self.price * self.quantity_in_stock

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"Product(id={self.id}, name='{self.name}', "
            f"category='{self.category}', price={self.price}, "
            f"qty={self.quantity_in_stock})"
        )

    def __str__(self) -> str:
        return f"{self.name} (${self.price:.2f}) — {self.quantity_in_stock} in stock"
