"""Views for the inventory application.

Implements Product CRUD, Customer registration, Order creation,
order history, and a dashboard with analytics integration.
"""

import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum, F, Count
from django.utils import timezone

from .models import Product, Customer, Order, OrderItem
from .forms import ProductForm, CustomerForm, OrderForm, OrderItemFormSet

logger = logging.getLogger("inventory")


# ══════════════════════════════════════════════════════════════
# Dashboard
# ══════════════════════════════════════════════════════════════

def dashboard(request):
    """Landing page with key business metrics."""
    total_products = Product.objects.count()
    total_customers = Customer.objects.count()
    total_orders = Order.objects.count()

    total_stock_value = (
        Product.objects.aggregate(
            total=Sum(F("price") * F("quantity_in_stock"))
        )["total"]
        or 0
    )

    total_revenue = (
        OrderItem.objects.aggregate(
            total=Sum(F("unit_price") * F("quantity"))
        )["total"]
        or 0
    )

    recent_orders = Order.objects.select_related("customer").prefetch_related("items")[:5]

    low_stock_products = Product.objects.filter(quantity_in_stock__lte=10).order_by("quantity_in_stock")[:5]

    top_products = (
        OrderItem.objects
        .values("product__name")
        .annotate(total_sold=Sum("quantity"))
        .order_by("-total_sold")[:5]
    )

    context = {
        "total_products": total_products,
        "total_customers": total_customers,
        "total_orders": total_orders,
        "total_stock_value": total_stock_value,
        "total_revenue": total_revenue,
        "recent_orders": recent_orders,
        "low_stock_products": low_stock_products,
        "top_products": top_products,
    }
    return render(request, "inventory/dashboard.html", context)


# ══════════════════════════════════════════════════════════════
# Product CRUD
# ══════════════════════════════════════════════════════════════

def product_list(request):
    products = Product.objects.all()
    return render(request, "inventory/product_list.html", {"products": products})


def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product created successfully.")
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "inventory/product_form.html", {"form": form, "title": "Add Product"})


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)
    return render(request, "inventory/product_form.html", {"form": form, "title": "Edit Product"})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        try:
            product.delete()
            messages.success(request, "Product deleted.")
        except Exception as e:
            logger.error("Error deleting product %s: %s", pk, e)
            messages.error(request, f"Cannot delete product: {e}")
        return redirect("product_list")
    return render(request, "inventory/product_confirm_delete.html", {"product": product})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "inventory/product_detail.html", {"product": product})


# ══════════════════════════════════════════════════════════════
# Customer CRUD
# ══════════════════════════════════════════════════════════════

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, "inventory/customer_list.html", {"customers": customers})


def customer_create(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer registered successfully.")
            return redirect("customer_list")
    else:
        form = CustomerForm()
    return render(request, "inventory/customer_form.html", {"form": form, "title": "Register Customer"})


def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer updated successfully.")
            return redirect("customer_list")
    else:
        form = CustomerForm(instance=customer)
    return render(request, "inventory/customer_form.html", {"form": form, "title": "Edit Customer"})


def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
        messages.success(request, "Customer deleted.")
        return redirect("customer_list")
    return render(request, "inventory/customer_confirm_delete.html", {"customer": customer})


# ══════════════════════════════════════════════════════════════
# Order Management
# ══════════════════════════════════════════════════════════════

def order_list(request):
    orders = Order.objects.select_related("customer").prefetch_related("items__product")
    return render(request, "inventory/order_list.html", {"orders": orders})


def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    order = form.save()
                    formset.instance = order
                    items = formset.save(commit=False)
                    for item in items:
                        item.unit_price = item.product.price
                        # Deduct stock
                        product = item.product
                        if item.quantity > product.quantity_in_stock:
                            raise Exception(
                                f"Not enough stock for {product.name}. "
                                f"Available: {product.quantity_in_stock}"
                            )
                        product.quantity_in_stock -= item.quantity
                        product.save()
                        item.save()
                    for obj in formset.deleted_objects:
                        obj.delete()
                messages.success(request, "Order created successfully.")
                return redirect("order_list")
            except Exception as e:
                logger.error("Order creation failed: %s", e)
                messages.error(request, f"Order creation failed: {e}")
    else:
        form = OrderForm()
        formset = OrderItemFormSet()
    return render(request, "inventory/order_form.html", {
        "form": form,
        "formset": formset,
        "title": "Create Order",
    })


def order_detail(request, pk):
    order = get_object_or_404(
        Order.objects.select_related("customer").prefetch_related("items__product"),
        pk=pk,
    )
    return render(request, "inventory/order_detail.html", {"order": order})
