from django.core import validators
from django.core.cache import cache
from django.db import models
from django.db.models import CheckConstraint, Q


def image_product_path(instance, filename):
    return f"products/{instance.subcategory.name}/{filename}"


class Category(models.Model):
    name = models.CharField(verbose_name="Имя категории", max_length=255)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Subcategory(models.Model):
    name = models.CharField(
        verbose_name="Имя суб-категории",
        max_length=255,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория суб-категории",
    )

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Суб-категория"
        verbose_name_plural = "Суб-категории"


class Product(models.Model):
    name = models.CharField(verbose_name="Название продукта", max_length=255)
    description = models.TextField(verbose_name="Описание")
    price = models.FloatField(verbose_name="Цена",
                              validators=[validators.MinValueValidator(limit_value=0.0)])
    stock = models.IntegerField(verbose_name="Наличие на складе",
                                validators=[validators.MinValueValidator(limit_value=0)])

    available = models.BooleanField(verbose_name="Доступность", default=False)
    image = models.ImageField(verbose_name="Изображение", upload_to=image_product_path, blank=True)

    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        verbose_name="Суб-категория",
    )

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.price} р."

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'product-{self.pk}')

    class Meta:
        ordering = ["name"]
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        constraints = (
            CheckConstraint(
                check=Q(price__gte=0.0),
                name='price_gte'
            ),
            CheckConstraint(
                check=Q(stock__gte=0),
                name='stock_gte'
            ),
        )
