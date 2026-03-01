"""Django ORM models — mapped from the OOP domain classes.

These models mirror the core domain objects (Product, Customer, Order,
OrderItem) while leveraging Django's ORM for database operations.
"""

from django.db import models
from django.core.validators import MinValueValidator, EmailValidator


class Product(models.Model):
    """A product in the inventory."""

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    quantity_in_stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"
        ordering = ["name"]

    def get_value_in_stock(self) -> float:
        """Return total monetary value of current stock."""
        return float(self.price) * self.quantity_in_stock

    def __str__(self) -> str:
        return f"{self.name} (${self.price})"


class Customer(models.Model):
    """A registered customer."""

    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True, validators=[EmailValidator()])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "customers"
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"


class Order(models.Model):
    """A customer order."""

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders"
    )
    order_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "orders"
        ordering = ["-order_date"]

    def calculate_total(self) -> float:
        """Return the sum of all order-item subtotals."""
        return sum(item.get_subtotal() for item in self.items.all())

    def __str__(self) -> str:
        return f"Order #{self.pk} — {self.customer.name}"


class OrderItem(models.Model):
    """A single line item inside an Order."""

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.RESTRICT, related_name="order_items"
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "order_items"

    def get_subtotal(self) -> float:
        """Return quantity * unit_price."""
        return float(self.unit_price) * self.quantity

    def __str__(self) -> str:
        return f"{self.quantity}x {self.product.name}"
