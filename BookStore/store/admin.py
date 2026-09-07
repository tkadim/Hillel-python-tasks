from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

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
    list_display = (
        'title',
        'author',
        'price',
        'image_preview'
    )
    list_filter = ['author', 'stock', 'category']
    search_fields = ['title', 'description']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" style="object-fit:contain;" />')

        return "Немає зображення"

    image_preview.short_description = "Прев'ю"


# admin.site.register(Category, CategoryAdmin)