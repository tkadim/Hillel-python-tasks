from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Book
from .cart import get_cart


def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart = get_cart(request)

    try:
        cart.add(book)
        messages.success(request, f"«{book.title}» was added to the cart.")
    except ValidationError as e:
        messages.error(request, str(e))

    return redirect('cart:cart_detail')


def update_cart_item(request, book_id):
    """Change quantity directly on the cart page"""
    book = get_object_or_404(Book, id=book_id)
    cart = get_cart(request)

    try:
        quantity = int(request.POST.get("quantity", 1))
        cart.update_quantity(book, quantity)
    except ValidationError as e:
        messages.error(request, str(e))

    return redirect("cart:cart_detail")

def remove_from_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart = get_cart(request)
    cart.remove(book)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = get_cart(request)
    context = {
        'items': cart.get_items(),
        'total_price': cart.total_price,
        'total_items': cart.total_items,
    }
    return render(request, 'cart/cart_detail.html', context)

def clear_cart(request):
    cart = get_cart(request)
    cart.clear()
    return redirect('cart:cart_detail')

