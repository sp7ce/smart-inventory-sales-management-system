"""Data Access Object for the Customer entity."""

from __future__ import annotations

from typing import List, Optional

from database.connection import get_connection
from database.dao.base_dao import BaseDAO
from core.models import Customer


class CustomerDAO(BaseDAO):
    """CRUD operations for the *customers* table."""

    def save(self, customer: Customer) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO customers (name, email) VALUES (%s, %s)",
                (customer.name, customer.email),
            )
            customer.id = cursor.lastrowid
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def find_by_id(self, customer_id: int) -> Optional[Customer]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return Customer(id=row["id"], name=row["name"], email=row["email"])
        finally:
            cursor.close()
            conn.close()

    def find_all(self) -> List[Customer]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM customers ORDER BY name")
            return [
                Customer(id=r["id"], name=r["name"], email=r["email"])
                for r in cursor.fetchall()
            ]
        finally:
            cursor.close()
            conn.close()

    def update(self, customer: Customer) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE customers SET name = %s, email = %s WHERE id = %s",
                (customer.name, customer.email, customer.id),
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def delete(self, customer_id: int) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM customers WHERE id = %s", (customer_id,))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()
