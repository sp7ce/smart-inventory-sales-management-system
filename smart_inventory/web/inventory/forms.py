"""Django forms with custom validation and user-friendly error messages."""

import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Product, Customer, Order, OrderItem


# ── Product Form ──────────────────────────────────────────────────────

class ProductForm(forms.ModelForm):
    """Form for creating / editing a Product."""

    class Meta:
        model = Product
        fields = ["name", "category", "price", "quantity_in_stock"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Product name",
            }),
            "category": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Category",
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-control", "step": "0.01", "min": "0",
            }),
            "quantity_in_stock": forms.NumberInput(attrs={
                "class": "form-control", "min": "0",
            }),
        }

    def clean_price(self) -> float:
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise ValidationError("Price cannot be negative.")
        return price

    def clean_quantity_in_stock(self) -> int:
        qty = self.cleaned_data.get("quantity_in_stock")
        if qty is not None and qty < 0:
            raise ValidationError("Stock quantity cannot be negative.")
        return qty


# ── Customer Form ────────────────────────────────────────────────────

class CustomerForm(forms.ModelForm):
    """Form for registering / editing a Customer."""

    class Meta:
        model = Customer
        fields = ["name", "email"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Full name",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control", "placeholder": "email@example.com",
            }),
        }

    _EMAIL_RE = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

    def clean_email(self) -> str:
        email = self.cleaned_data.get("email", "")
        if not self._EMAIL_RE.match(email):
            raise ValidationError(
                f"'{email}' is not a valid email address."
            )
        # Check uniqueness (exclude self on update)
        qs = Customer.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("A customer with this email already exists.")
        return email


# ── Order Form ───────────────────────────────────────────────────────

class OrderForm(forms.ModelForm):
    """Form for creating an Order (header only)."""

    class Meta:
        model = Order
        fields = ["customer"]
        widgets = {
            "customer": forms.Select(attrs={"class": "form-select"}),
        }


# ── OrderItem Inline Formset ─────────────────────────────────────────

class OrderItemForm(forms.ModelForm):
    """Form for a single line item."""

    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]
        widgets = {
            "product": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={
                "class": "form-control", "min": "1",
            }),
        }

    def clean_quantity(self) -> int:
        qty = self.cleaned_data.get("quantity")
        if qty is not None and qty <= 0:
            raise ValidationError("Quantity must be at least 1.")
        return qty

    def clean(self):
        cleaned = super().clean()
        product = cleaned.get("product")
        quantity = cleaned.get("quantity")
        if product and quantity:
            if quantity > product.quantity_in_stock:
                raise ValidationError(
                    f"Not enough stock for {product.name}. "
                    f"Available: {product.quantity_in_stock}, requested: {quantity}."
                )
        return cleaned


OrderItemFormSet = forms.inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    extra=3,
    can_delete=True,
    min_num=1,
    validate_min=True,
)
