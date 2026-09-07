from os import name
from unicodedata import category

from django.contrib.auth.middleware import LoginRequiredMiddleware
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.management import templates
from django.db.models import Q, Count, Sum, F
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Book, Category


class BooksListView(ListView):
    model = Book
    template_name = 'store/books.html'
    context_object_name = 'books'

    paginate_by = 4

    def get_queryset(self):
        queryset = Book.objects.all()

        # ------------------------------------------------
        # ФІЛЬТР: текстовий пошук за назвою або автором
        # ------------------------------------------------
        search_query = self.request.GET.get("q")
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(author__icontains=search_query)
            )

        # ------------------------------------------------
        # ФІЛЬТР: конкретний автор (наприклад, випадаючий список)
        # ------------------------------------------------
        author = self.request.GET.get("author")
        if author:
            queryset = queryset.filter(author=author)

        # ------------------------------------------------
        # ФІЛЬТР: діапазон ціни
        # ------------------------------------------------
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # ------------------------------------------------
        # СОРТУВАННЯ (опційно, теж через GET-параметр)
        # ------------------------------------------------
        sort_by = self.request.GET.get("sort", "-id")  # за замовчуванням - найновіші спочатку
        allowed_sort_fields = ["title", "-title", "price", "-price", "-id"]
        if sort_by in allowed_sort_fields:
            queryset = queryset.order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Додаємо в контекст список унікальних авторів (для випадаючого списку
        фільтра) та поточні значення фільтрів, щоб форма "пам'ятала" вибір
        користувача після переходу на іншу сторінку пагінації.
        """
        context = super().get_context_data(**kwargs)

        context["all_authors"] = Book.objects.values_list(
            "author", flat=True
        ).distinct().order_by("author")

        # Поточні значення фільтрів - потрібні, щоб підставити їх
        # назад у поля форми (щоб фільтр не "скидався" при пагінації)
        context["current_query"] = self.request.GET.get("q", "")
        context["current_author"] = self.request.GET.get("author", "")
        context["current_min_price"] = self.request.GET.get("min_price", "")
        context["current_max_price"] = self.request.GET.get("max_price", "")
        context["current_sort"] = self.request.GET.get("sort", "-id")

        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["query_string"] = query_params.urlencode()

        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'store/book_detail.html'
    context_object_name = 'book'
    pk_url_kwarg = 'book_id'


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    template_name = 'store/book_form.html'
    fields = ['title', 'author', 'description', 'price', 'image']
    success_url = reverse_lazy('store:index')


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    template_name = 'store/book_form.html'
    fields = ['title', 'author', 'description', 'price', 'image']
    pk_url_kwarg = 'book_id'
    success_url = reverse_lazy('store:index')


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'store/book_confirm_delete.html'
    pk_url_kwarg = 'book_id'
    success_url = reverse_lazy('store:index')


def index(request):
    books = Book.objects.all()

    if not books:
        return HttpResponseNotFound("<h1>Books not found</h1>")

    return render(request, 'store/books.html', {'books': books})


def queries(request):
    books = Book.objects.all()

    fantasy_cat = Category.objects.get(name='Fantasy')
    filtered_books = books.filter(Q(price__gt=300) & Q(category=fantasy_cat))
    filtered_books_stock = filtered_books.aggregate(number=Sum('stock'))

    return render(request, 'store/queries.html', {'queries': filtered_books, 'total_stock': filtered_books_stock['number']})


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    return render(request, 'store/book_detail.html', {'book': book})