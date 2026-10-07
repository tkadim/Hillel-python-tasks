from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F

from cart.cart import get_cart
from orders.models import Order, OrderItem
from store.models import Book
from django.core.mail import send_mail

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


def validate_payment(order, event):
    if event["amount_total"] != order.total_price * 100:
        raise ValueError("Invalid payment amount")

    if event["payment_status"] != "paid":
        raise ValueError("Payment not completed")


def send_order_email(order):
    subject = "Your order has been accepted."

    message = f"Thank you for your order #{order.id}"

    send_mail(
        subject,
        message,
        "shop@bookstore.com",
        [order.customer.email],
    )