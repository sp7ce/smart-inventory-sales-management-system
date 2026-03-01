"""Unit tests for the core domain models and exceptions."""

import sys
import os
import unittest
from datetime import datetime

# Ensure the smart_inventory package is on the path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from core.models import Product, Customer, Order, OrderItem
from core.exceptions import (
    OutOfStockException,
    InvalidEmailException,
    InvalidQuantityException,
)


# ── Product Tests ─────────────────────────────────────────────────────

class TestProduct(unittest.TestCase):
    """Tests for the Product model."""

    def setUp(self) -> None:
        self.product = Product(
            id=1, name="Laptop", category="Electronics",
            price=999.99, quantity_in_stock=10,
        )

    def test_add_stock(self) -> None:
        self.product.add_stock(5)
        self.assertEqual(self.product.quantity_in_stock, 15)

    def test_add_stock_invalid_quantity(self) -> None:
        with self.assertRaises(InvalidQuantityException):
            self.product.add_stock(0)
        with self.assertRaises(InvalidQuantityException):
            self.product.add_stock(-3)

    def test_remove_stock(self) -> None:
        self.product.remove_stock(3)
        self.assertEqual(self.product.quantity_in_stock, 7)

    def test_remove_stock_invalid_quantity(self) -> None:
        with self.assertRaises(InvalidQuantityException):
            self.product.remove_stock(0)

    def test_remove_stock_out_of_stock(self) -> None:
        with self.assertRaises(OutOfStockException):
            self.product.remove_stock(20)

    def test_get_value_in_stock(self) -> None:
        self.assertAlmostEqual(
            self.product.get_value_in_stock(), 999.99 * 10
        )

    def test_str_repr(self) -> None:
        self.assertIn("Laptop", str(self.product))
        self.assertIn("Laptop", repr(self.product))


# ── Customer Tests ────────────────────────────────────────────────────

class TestCustomer(unittest.TestCase):
    """Tests for the Customer model."""

    def test_valid_email(self) -> None:
        customer = Customer(id=1, name="Alice", email="alice@example.com")
        self.assertTrue(customer.validate_email())

    def test_invalid_email_no_at(self) -> None:
        with self.assertRaises(InvalidEmailException):
            Customer(id=2, name="Bob", email="bob-example.com")

    def test_invalid_email_no_domain(self) -> None:
        with self.assertRaises(InvalidEmailException):
            Customer(id=3, name="Carol", email="carol@")

    def test_str_repr(self) -> None:
        c = Customer(id=1, name="Alice", email="alice@example.com")
        self.assertIn("Alice", str(c))
        self.assertIn("alice@example.com", repr(c))


# ── OrderItem Tests ───────────────────────────────────────────────────

class TestOrderItem(unittest.TestCase):
    """Tests for the OrderItem model."""

    def setUp(self) -> None:
        self.product = Product(
            id=1, name="Mouse", category="Accessories",
            price=25.50, quantity_in_stock=50,
        )

    def test_get_subtotal(self) -> None:
        item = OrderItem(self.product, 4)
        self.assertAlmostEqual(item.get_subtotal(), 25.50 * 4)

    def test_invalid_quantity(self) -> None:
        with self.assertRaises(InvalidQuantityException):
            OrderItem(self.product, 0)


# ── Order Tests ───────────────────────────────────────────────────────

class TestOrder(unittest.TestCase):
    """Tests for the Order model."""

    def setUp(self) -> None:
        self.customer = Customer(
            id=1, name="Alice", email="alice@example.com"
        )
        self.product_a = Product(
            id=1, name="Keyboard", category="Accessories",
            price=45.00, quantity_in_stock=20,
        )
        self.product_b = Product(
            id=2, name="Monitor", category="Electronics",
            price=300.00, quantity_in_stock=5,
        )

    def test_add_item_and_total(self) -> None:
        order = Order(id=1, customer=self.customer)
        order.add_item(self.product_a, 2)
        order.add_item(self.product_b, 1)
        self.assertAlmostEqual(order.calculate_total(), 45.0 * 2 + 300.0)
        self.assertEqual(len(order.items), 2)

    def test_add_item_reduces_stock(self) -> None:
        order = Order(id=2, customer=self.customer)
        order.add_item(self.product_a, 3)
        self.assertEqual(self.product_a.quantity_in_stock, 17)

    def test_add_item_out_of_stock(self) -> None:
        order = Order(id=3, customer=self.customer)
        with self.assertRaises(OutOfStockException):
            order.add_item(self.product_b, 10)

    def test_add_item_invalid_quantity(self) -> None:
        order = Order(id=4, customer=self.customer)
        with self.assertRaises(InvalidQuantityException):
            order.add_item(self.product_a, -1)

    def test_order_str(self) -> None:
        order = Order(
            id=5, customer=self.customer,
            order_date=datetime(2026, 1, 15, 10, 30),
        )
        order.add_item(self.product_a, 1)
        text = str(order)
        self.assertIn("Alice", text)
        self.assertIn("TOTAL", text)


if __name__ == "__main__":
    unittest.main()
