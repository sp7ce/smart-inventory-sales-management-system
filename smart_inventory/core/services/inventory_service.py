"""Business services that orchestrate domain operations."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Tuple

from core.models import Product, Customer, Order


class InventoryService:
    """High-level operations on the inventory.

    Provides façade methods used by both the DAO layer and Django views.
    """

    @staticmethod
    def create_order(
        order_id: int,
        customer: Customer,
        items: List[Tuple[Product, int]],
        order_date: datetime | None = None,
    ) -> Order:
        """Create an order, deducting stock for every item.

        Args:
            order_id: New order identifier.
            customer: The ordering customer.
            items: Pairs of (product, quantity).
            order_date: Optional explicit date.

        Returns:
            The fully populated :class:`Order`.
        """
        order = Order(id=order_id, customer=customer, order_date=order_date)
        for product, qty in items:
            order.add_item(product, qty)
        return order

    @staticmethod
    def total_stock_value(products: List[Product]) -> float:
        """Return the combined stock value of all products."""
        return sum(p.get_value_in_stock() for p in products)

    @staticmethod
    def products_by_category(products: List[Product]) -> Dict[str, List[Product]]:
        """Group products by category."""
        result: Dict[str, List[Product]] = {}
        for p in products:
            result.setdefault(p.category, []).append(p)
        return result
