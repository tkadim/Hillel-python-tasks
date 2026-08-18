from os import name

from django.db.models import Q, Count, Sum, F
from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Category


def index(request):
    books = Book.objects.all()
    return render(request, 'books.html', {'books': books})

def queries(request):
    books = Book.objects.all()

    fantasy_cat = Category.objects.get(name='Fantasy')
    filtered_books = books.filter(Q(price__gt=300) & Q(category=fantasy_cat))
    filtered_books_stock = filtered_books.aggregate(number=Sum('stock'))

    return render(request, 'queries.html', {'queries': filtered_books, 'total_stock': filtered_books_stock['number']})