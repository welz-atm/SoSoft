from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('create_product/',views.create_product,name='create_product'),
    path('edit_product/<int:pk>/',views.edit_product,name='edit_product'),
    path('all_products/',views.all_products,name='all_products'),
    path('view_order/<int:pk>/',views.view_order,name='view_order'),
    path('all_orders/',views.all_orders,name='all_orders'),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('delete_order/<int:pk>/',views.delete_order,name='delete_order'),
    path('create_approval/',views.create_approval,name='create_approval'),
    path('edit_approval/<int:pk>/',views.edit_approval,name='edit_approval'),
    path('all_approvals/',views.all_approvals,name='all_approvals'),
    path('delete_approval/<int:pk>/',views.delete_approval,name='delete_approval'),
    path('all_production',views.all_production,name='all_production'),
    path('create_production',views.create_production,name='create_production'),
    path('edit_production/<int:pk>/',views.edit_production,name='edit_production'),
    path('delete_production/<int:pk>/',views.delete_production,name='delete_production'),
    path('pending_orders',views.pending_order,name='pending_orders'),
    path('checkout/',views.checkout,name='checkout'),
    path('order_summary',views.order_summary,name='order_summary'),
    path('add_cart/<int:pk>/',views.add_cart,name='add_cart'),
    path('remove_cart/<int:pk>/',views.remove_from_cart,name='remove_cart'),
    path('create_warehouse/',views.create_warehouse,name='create_warehouse'),
    path('edit_warehouse/<int:pk>/',views.edit_warehouse,name='edit_warehouse'),
    path('all_warehouses/',views.all_warehouse,name='all_warehouses'),
    path('delete_warehouse/<int:pk>/',views.delete_warehouse,name='delete_warehouse'),
    path('create_received/',views.create_warehouse_received,name='create_received'),
    path('warehouse_stock/',views.warehouse_stock,name='warehouse_stock'),
    path('all_received/',views.all_received,name='all_received'),
    path('all_supplied/',views.all_supplied,name='all_supplied'),
    path('delete_received/<int:pk>/',views.delete_received,name='delete_received'),
    path('delete_supplied/<int:pk>/',views.delete_supplied,name='delete_supplied'),
    path('edit_received/<int:pk>/',views.edit_received,name='edit_received'),
    path('create_sales/',views.create_sales,name='create_sales'),
    path('all_sales/',views.all_sales,name='all_sales'),
    path('my_customers/',views.my_customers,name='my_customers'),
    path('to_supply/',views.to_supply,name='to_supply'),
    path('approve_supplied/',views.approve_supplied,name='approve_supplied'),
    path('distributor_supplied/',views.distributor_supplied,name='distributor_supplied'),
    path('not_supplied/',views.not_supplied,name='not_supplied'),
    path('success/',views.success,name='success'),
    path('failed/',views.failed,name='failed'),

]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)