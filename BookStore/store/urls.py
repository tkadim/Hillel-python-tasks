from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views import View

from . import views
from .views import *

app_name = 'store'
urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.BooksListView.as_view(), name='index'),
    path('queries/', views.queries, name='queries'),
    # path('book/<int:book_id>/', views.book_detail, name='book_detail')
    path('<int:book_id>/', views.BookDetailView.as_view(), name='book_detail'),
    path('add/', views.BookCreateView.as_view(), name='book_create'),
    path('<int:book_id>/update/', views.BookUpdateView.as_view(), name='book_update'),
    path('<int:book_id>/delete/', views.BookDeleteView.as_view(), name='book_delete')
]