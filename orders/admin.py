from django.contrib import admin
from .models import Category, Dish, Table, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name',)


admin.site.register(Table)
admin.site.register(Order)
admin.site.register(OrderItem)

