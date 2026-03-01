"""Data Access Object for the Product entity."""

from __future__ import annotations

from typing import List, Optional

from database.connection import get_connection
from database.dao.base_dao import BaseDAO
from core.models import Product


class ProductDAO(BaseDAO):
    """CRUD operations for the *products* table."""

    # ── CREATE ────────────────────────────────────────────────

    def save(self, product: Product) -> None:
        """Insert a new product row.

        After a successful insert the product's *id* attribute is updated
        with the auto-generated primary key.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO products (name, category, price, quantity_in_stock)
                VALUES (%s, %s, %s, %s)
                """,
                (product.name, product.category, product.price, product.quantity_in_stock),
            )
            product.id = cursor.lastrowid
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    # ── READ ──────────────────────────────────────────────────

    def find_by_id(self, product_id: int) -> Optional[Product]:
        """Return a :class:`Product` or *None*."""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return Product(
                id=row["id"],
                name=row["name"],
                category=row["category"],
                price=float(row["price"]),
                quantity_in_stock=row["quantity_in_stock"],
            )
        finally:
            cursor.close()
            conn.close()

    def find_all(self) -> List[Product]:
        """Return every product."""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM products ORDER BY name")
            return [
                Product(
                    id=r["id"],
                    name=r["name"],
                    category=r["category"],
                    price=float(r["price"]),
                    quantity_in_stock=r["quantity_in_stock"],
                )
                for r in cursor.fetchall()
            ]
        finally:
            cursor.close()
            conn.close()

    # ── UPDATE ────────────────────────────────────────────────

    def update(self, product: Product) -> None:
        """Update an existing product row."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE products
                   SET name = %s, category = %s, price = %s, quantity_in_stock = %s
                 WHERE id = %s
                """,
                (product.name, product.category, product.price,
                 product.quantity_in_stock, product.id),
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    # ── DELETE ────────────────────────────────────────────────

    def delete(self, product_id: int) -> None:
        """Delete a product by id."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()
