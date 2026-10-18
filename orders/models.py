from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Dish(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='dishes')
    name = models.CharField(max_length=200)
    composition = models.TextField(blank=True, verbose_name='Состав')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Table(models.Model):
    number = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"Стол {self.number}"


class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False)
    comment = models.TextField(
        blank=True,
        default="",
        verbose_name="Комментарий к заказу",
        help_text="Например: принесите кофе с корицей, всё блюда без лука"
    )
    def __str__(self):
        return f"Заказ #{self.pk} — стол {self.table.number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    dish = models.ForeignKey(Dish, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    is_served = models.BooleanField(default=False)
    added_later = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dish.name} × {self.quantity}"