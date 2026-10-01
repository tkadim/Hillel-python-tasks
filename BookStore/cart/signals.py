from django.contrib.auth import user_logged_in
from django.dispatch import receiver
from store.models import Book
from .models import Cart as CartModel, CartItem

from cart.cart import SESSION_CART_KEY

import logging

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def merge_session_with_db_cart(sender, request, user, **kwargs):
    session_cart = request.session.get(SESSION_CART_KEY)
    if not session_cart:
        return

    db_cart, _ = CartModel.objects.get_or_create(user=user)

    for book_id_str, quantity in session_cart.items():
        try:
            book = Book.objects.get(id=int(book_id_str))
        except Book.DoesNotExist as e:
            logger.exception(f"The book {book.title} is out of stock")
            continue

        item, created = CartItem.objects.get_or_create(
            cart=db_cart, book=book, defaults={'quantity': quantity}
        )

        if not created:
            item.quantity += quantity
            item.save()

    request.session[SESSION_CART_KEY] = {}
    request.session.modified = True