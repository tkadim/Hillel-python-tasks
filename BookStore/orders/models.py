from django.conf import settings
from django.db import models
from django.db.models import ForeignKey
from django.db.models.fields import CharField

from store.models import Book

class Order(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = 'orders',
    )

    status = CharField(
        max_length = 20,
        choices = Status.choices,
        default = Status.PENDING,
    )

    shipping_address = models.CharField(max_length=255, blank=True)

    phone_number = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} ({self.user.username})"

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = ForeignKey(
        Order,
        on_delete = models.CASCADE,
        related_name = 'items',
    )

    book = models.ForeignKey(
        Book,
        on_delete = models.SET_NULL,
        null = True,
    )

    book_title = models.CharField(max_length=255)

    quantity = models.PositiveIntegerField(default=1)

    price_at_purchase = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.book_title} x {self.quantity}"

    @property
    def subtotal(self):
        return self.price_at_purchase * self.quantity