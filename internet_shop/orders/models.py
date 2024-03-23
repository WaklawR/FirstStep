from django.db import models
from shop.models import Product


class Order(models.Model):
    first_name = models.CharField(verbose_name="Имя", max_length=50)
    last_name = models.CharField(verbose_name="Фамилия", max_length=50)
    email = models.EmailField(verbose_name="E-mail")
    address = models.CharField(verbose_name="Адрес", max_length=250)
    postal_code = models.CharField(verbose_name="Почтовый индекс", max_length=20)
    city = models.CharField(verbose_name="Город", max_length=100)

    date_created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    date_modified = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)

    paid = models.BooleanField(verbose_name="Оплачено", default=False)
    mailed = models.BooleanField(verbose_name="Уведомлено", default=False)

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name="Заказ",
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.CASCADE,
        verbose_name="Продукт",
    )
    price = models.DecimalField(verbose_name="Цена продукта", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name="Количество продукта", default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
