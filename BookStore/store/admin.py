from django.contrib import admin
from .models import Category, Book

# admin.site.register(Category)
# admin.site.register(Book)

class BookInline(admin.TabularInline):
    model = Book
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [BookInline]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_filter = ['author', 'stock', 'category']
    search_fields = ['title', 'description']