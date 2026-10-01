from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F

from cart.cart import get_cart
from orders.models import Order, OrderItem
from store.models import Book


@transaction.atomic
def create_order_from_cart(request, shipping_address='', phone_number=''):
    cart = get_cart(request)
    items = cart.get_items()

    if not items:
        return None

    order = Order.objects.create(
        user=request.user,
        shipping_address=shipping_address,
        phone_number=phone_number,
    )

    for item in items:

        book = Book.objects.select_for_update().get(id=item["book"].id)

        if book.stock < item['quantity']:
            raise ValidationError(
                f"Insufficient stock of the book {book.title}"
                f"In stock: {book.stock}, In cart: {item['quantity']}"
            )

        OrderItem.objects.create(
            order=order,
            book=book,
            book_title=book.title,
            quantity=item["quantity"],
            price_at_purchase=book.price,
        )

        book.stock = F("stock") - item["quantity"]
        book.save(update_fields=["stock"])

    cart.clear()
    return order