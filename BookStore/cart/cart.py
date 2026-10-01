from decimal import Decimal
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
        if book_id in self.cart:
            self.cart[book_id] += quantity
        else:
            self.cart[book_id] = quantity
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
        if not created:
            item.quantity += quantity
            item.save()

    def remove(self, book):
        CartItem.objects.filter(cart=self.cart_obj, book=book).delete()

    def clear(self):
        self.cart_obj.items.all().delete()

    def get_items(self):
        return [
            {'book': item.book, 'quantity': item.quantity, 'subtotal': item.subtotal}
            for item in self.cart_obj.items.select_related('book').all()
        ]

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
