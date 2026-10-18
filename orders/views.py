import difflib
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Prefetch, Q
from django.http import JsonResponse
from django.utils import timezone
from .models import Order, OrderItem, Dish, Table, Category


@login_required
def main(request, table_id=None):
    tables = Table.objects.all()
    open_orders = {o.table_id: o for o in Order.objects.filter(is_closed=False)}

    q = request.GET.get('q', '').strip()
    all_dishes = Dish.objects.filter(is_available=True).select_related('category')

    if q:
        names = list(all_dishes.values_list('name', flat=True))
        close = difflib.get_close_matches(q, names, n=20, cutoff=0.5)
        dishes = all_dishes.filter(Q(name__icontains=q) | Q(name__in=close))
    else:
        dishes = all_dishes

    categories = Category.objects.prefetch_related(
        Prefetch('dishes', queryset=dishes)
    )

    current_table = None
    current_order = None
    if table_id:
        current_table = get_object_or_404(Table, pk=table_id)
        current_order = open_orders.get(current_table.id)
        if current_order is None:
            current_order = Order.objects.create(table=current_table)

    return render(request, 'orders/main.html', {
        'tables': tables,
        'open_orders': open_orders,
        'categories': categories,
        'current_table': current_table,
        'current_order': current_order,
        'q': q,
    })


@login_required
@require_POST
def add_dish(request, order_pk, dish_pk):
    order = get_object_or_404(Order, pk=order_pk, is_closed=False)
    dish = get_object_or_404(Dish, pk=dish_pk)

    has_served = order.items.filter(is_served=True).exists()

    item = order.items.filter(dish=dish, is_served=False).first()
    if item:
        item.quantity += 1
        item.save()
    else:
        OrderItem.objects.create(
            order=order, dish=dish, quantity=1,
            added_later=has_served,
        )
    return redirect('main_table', table_id=order.table_id)


@login_required
@require_POST
def toggle_served(request, item_pk):
    item = get_object_or_404(OrderItem, pk=item_pk)
    item.is_served = not item.is_served
    item.save()
    return redirect('main_table', table_id=item.order.table_id)


@login_required
@require_POST
def change_qty(request, item_pk, delta):
    item = get_object_or_404(OrderItem, pk=item_pk)
    table_id = item.order.table_id
    item.quantity += int(delta)
    if item.quantity <= 0:
        item.delete()
    else:
        item.save()
    return redirect('main_table', table_id=table_id)


@login_required
@require_POST
def close_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.is_closed = True
    order.save()
    return redirect('main')
    if 'comment' in request.POST:
        order.comment = request.POST.get('comment', '').strip()

    order.is_closed = True
    order.save()
    return redirect('main')

@login_required
@require_POST
def update_comment(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.comment = request.POST.get('comment', '').strip()
    order.save()
    return redirect('main_table', table_id=order.table_id)

@login_required
def dish_info(request, dish_pk):
    dish = get_object_or_404(Dish, pk=dish_pk)
    return JsonResponse({
        'name': dish.name,
        'composition': dish.composition or 'Состав не указан',
    })


@login_required
def today_report(request):
    today = timezone.localdate()
    closed = Order.objects.filter(
        is_closed=True,
        created_at__date=today,
    ).prefetch_related('items__dish')
    return render(request, 'orders/report.html', {'orders': closed, 'date': today})