from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=300, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True)
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="books")
    image = models.ImageField(upload_to='books/', blank=True, null=True, default="books/blank.jpg")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_title_author'
            )
        ]

    def __str__(self):
        return self.title