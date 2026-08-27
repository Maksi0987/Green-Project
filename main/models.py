from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name="Назва категорії")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="URL-слаг")

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("main:product_list_by_category", kwargs={"category_slug": self.slug})


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва товару")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Слаг для URL")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Категорія"
    )
    description = models.TextField(verbose_name="Опис")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name="Зображення")

    views = models.IntegerField(default=0, verbose_name="Перегляди")
    is_active = models.BooleanField(default=True, verbose_name="В наявності")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Час створення")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} (ID: {self.id})"

    def get_absolute_url(self):
        # Виправлено баг з .html на кінці
        return reverse("main:product_detail", kwargs={"id": self.id, "slug": self.slug})