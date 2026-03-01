"""Data Access Objects for the Smart Inventory system."""

from .product_dao import ProductDAO
from .customer_dao import CustomerDAO
from .order_dao import OrderDAO

__all__ = ["ProductDAO", "CustomerDAO", "OrderDAO"]
