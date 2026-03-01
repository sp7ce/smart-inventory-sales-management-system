"""Data Access Object for Order (with OrderItems) using transactions."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from database.connection import get_connection
from database.dao.base_dao import BaseDAO
from core.models import Product, Customer, Order, OrderItem


class OrderDAO(BaseDAO):
    """CRUD operations for the *orders* and *order_items* tables.

    All writes use a single transaction so that either the entire
    order (header + items) is committed, or nothing is.
    """

    # ── CREATE ────────────────────────────────────────────────

    def save(self, order: Order) -> None:
        """Persist an order **and** all its items in one transaction."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO orders (customer_id, order_date) VALUES (%s, %s)",
                (order.customer.id, order.order_date),
            )
            order.id = cursor.lastrowid

            for item in order.items:
                cursor.execute(
                    """
                    INSERT INTO order_items (order_id, product_id, quantity, unit_price)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (order.id, item.product.id, item.quantity, item.product.price),
                )

            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    # ── READ ──────────────────────────────────────────────────

    def find_by_id(self, order_id: int) -> Optional[Order]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT o.*, c.name AS customer_name, c.email AS customer_email
                  FROM orders o
                  JOIN customers c ON o.customer_id = c.id
                 WHERE o.id = %s
                """,
                (order_id,),
            )
            row = cursor.fetchone()
            if row is None:
                return None

            customer = Customer(
                id=row["customer_id"],
                name=row["customer_name"],
                email=row["customer_email"],
            )
            order = Order(
                id=row["id"],
                customer=customer,
                order_date=row["order_date"],
            )

            cursor.execute(
                """
                SELECT oi.*, p.name AS product_name, p.category, p.price AS product_price,
                       p.quantity_in_stock
                  FROM order_items oi
                  JOIN products p ON oi.product_id = p.id
                 WHERE oi.order_id = %s
                """,
                (order_id,),
            )
            for ir in cursor.fetchall():
                product = Product(
                    id=ir["product_id"],
                    name=ir["product_name"],
                    category=ir["category"],
                    price=float(ir["product_price"]),
                    quantity_in_stock=ir["quantity_in_stock"],
                )
                order.items.append(OrderItem(product, ir["quantity"]))

            return order
        finally:
            cursor.close()
            conn.close()

    def find_all(self) -> List[Order]:
        """Return all orders (header only, no items loaded for speed)."""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT o.*, c.name AS customer_name, c.email AS customer_email
                  FROM orders o
                  JOIN customers c ON o.customer_id = c.id
                 ORDER BY o.order_date DESC
                """
            )
            orders: List[Order] = []
            for row in cursor.fetchall():
                customer = Customer(
                    id=row["customer_id"],
                    name=row["customer_name"],
                    email=row["customer_email"],
                )
                orders.append(
                    Order(
                        id=row["id"],
                        customer=customer,
                        order_date=row["order_date"],
                    )
                )
            return orders
        finally:
            cursor.close()
            conn.close()

    # ── UPDATE ────────────────────────────────────────────────

    def update(self, order: Order) -> None:
        """Update order date and re-write all items."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE orders SET order_date = %s WHERE id = %s",
                (order.order_date, order.id),
            )
            cursor.execute("DELETE FROM order_items WHERE order_id = %s", (order.id,))
            for item in order.items:
                cursor.execute(
                    """
                    INSERT INTO order_items (order_id, product_id, quantity, unit_price)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (order.id, item.product.id, item.quantity, item.product.price),
                )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    # ── DELETE ────────────────────────────────────────────────

    def delete(self, order_id: int) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()
