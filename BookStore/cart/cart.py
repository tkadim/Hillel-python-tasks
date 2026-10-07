from decimal import Decimal

from django.core.exceptions import ValidationError

from .models import Cart as CartModel, CartItem
from store.models import Book

SESSION_CART_KEY = "cart"

class SessionCart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(SESSION_CART_KEY)
        if cart is None:
            cart = self.session[SESSION_CART_KEY] = {}
        self.cart = cart

    def add(self, book, quantity=1):
        book_id = str(book.id)
        current_quantity = self.cart.get(book_id, 0)
        new_quantity = current_quantity + quantity

        if new_quantity > book.stock:
            raise ValidationError(
                f"Out of stock of '{book.title}'"
                f"(In stock: {book.stock} pcs, In the cart: {current_quantity} pcs)"
            )

        self.cart[book_id] = new_quantity
        self._save()

    def update_quantity(self, book, quantity):
        """Set particular number of books"""
        if quantity > book.stock:
            raise ValidationError(f"There are only {book.stock} pcs of '{book.title}' in stock")

        if quantity <= 0:
            self.remove(book)
            return

        self.cart[str(book.id)] = quantity
        self._save()

    def remove(self, book):
        book_id = str(book.id)
        if book_id in self.cart:
            del self.cart[book_id]
            self._save()

    def clear(self):
        self.session[SESSION_CART_KEY] = {}
        self._save()

    def _save(self):
        self.session.modified = True

    def get_items(self):

        book_ids = self.cart.keys()
        books = Book.objects.filter(id__in=book_ids)
        items = []
        for book in books:
            quantity = self.cart[str(book.id)]
            items.append({
                'book': book,
                'quantity': quantity,
                'subtotal': book.price * quantity,
                "exceeds_stock": quantity > book.stock,
            })
        return items

    @property
    def total_price(self):
        return sum(item['subtotal'] for item in self.get_items())

    @property
    def total_items(self):
        return sum(self.cart.values())


class DatabaseCart:
    def __init__(self, request):
        self.cart_obj, _ = CartModel.objects.get_or_create(user=request.user)

    def add(self, book, quantity=1):
        item, created = CartItem.objects.get_or_create(
            cart=self.cart_obj, book=book, defaults={"quantity": quantity}
        )
        new_quantity = quantity if created else item.quantity + quantity

        if new_quantity > book.stock:
            raise ValidationError(

                f"Not enough '{book.title}' in stock "
                f"(In stock: {book.stock} pcs)"
            )

        if not created:
            item.quantity = new_quantity
            item.save()

    def update_quantity(self, book, quantity):
        if quantity > book.stock:
            raise ValidationError(f"Only {book.stock} pcs. of the book '{book.title}' in stock")

        if quantity <= 0:
            self.remove(book)
            return

        CartItem.objects.filter(cart=self.cart_obj, book=book).update(quantity=quantity)

    def remove(self, book):
        CartItem.objects.filter(cart=self.cart_obj, book=book).delete()

    def clear(self):
        self.cart_obj.items.all().delete()

    def get_items(self):
        items = []
        for item in self.cart_obj.items.select_related("book").all():
            items.append({
                "book": item.book,
                "quantity": item.quantity,
                "subtotal": item.subtotal,
                "exceeds_stock": item.quantity > item.book.stock,
            })
        return items

    @property
    def total_price(self):
        return self.cart_obj.total_price

    @property
    def total_items(self):
        return self.cart_obj.total_items


def get_cart(request):
    if request.user.is_authenticated:
        return DatabaseCart(request)
    return SessionCart(request)
