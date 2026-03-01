"""Admin panel configuration for the inventory app."""

from django.contrib import admin
from .models import Product, Customer, Order, OrderItem


# ── Inline for OrderItems ────────────────────────────────────────────

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ("get_subtotal",)

    def get_subtotal(self, obj):
        return f"${obj.get_subtotal():.2f}" if obj.pk else "—"
    get_subtotal.short_description = "Subtotal"


# ── Product Admin ────────────────────────────────────────────────────

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "quantity_in_stock", "stock_value")
    list_filter = ("category",)
    search_fields = ("name", "category")
    list_editable = ("price", "quantity_in_stock")

    def stock_value(self, obj):
        return f"${obj.get_value_in_stock():.2f}"
    stock_value.short_description = "Stock Value"


# ── Customer Admin ───────────────────────────────────────────────────

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email")


# ── Order Admin ──────────────────────────────────────────────────────

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "order_date", "total")
    list_filter = ("order_date",)
    search_fields = ("customer__name",)
    inlines = [OrderItemInline]

    def total(self, obj):
        return f"${obj.calculate_total():.2f}"
    total.short_description = "Total"
