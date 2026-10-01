from django.shortcuts import render, redirect, get_object_or_404
from store.models import Book
from .cart import get_cart


def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart = get_cart(request)
    cart.add(book)
    return redirect('cart:cart_detail')

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

