from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('table/<int:table_id>/', views.main, name='main_table'),
    path('order/<int:order_pk>/add/<int:dish_pk>/', views.add_dish, name='add_dish'),
    path('item/<int:item_pk>/served/', views.toggle_served, name='toggle_served'),
    path('item/<int:item_pk>/qty/<str:delta>/', views.change_qty, name='change_qty'),
    path('order/<int:pk>/close/', views.close_order, name='close_order'),
    path('report/', views.today_report, name='today_report'),
    path('dish/<int:dish_pk>/info/', views.dish_info, name='dish_info'),
    path('report/', views.today_report, name='today_report'),
    path('order/<int:pk>/update-comment/', views.update_comment, name='update_comment'),
]