from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('', views.home_view , name='home'),
    path('login_user/', views.login_user , name='login'),
    path('logout_user/', views.logout_user , name='logout'),
    path('dashboard/', views.dashboard , name='dashboard'),
    path('register_general/' , views.register_general , name='register_general'),
    path('register_sales/' , views.register_sales , name='register_sales'),
    path('register_accounts/' , views.register_account , name='register_account'),
    path('register_distributor/' , views.register_distributor , name='register_distributor'),
    path('register_warehouse_manager/' , views.register_warehouse_manager , name='register_warehouse_manager'),
    path('register_guarantor/' , views.register_guarantor , name='guarantors'),
    path('user_profile/<int:pk>/', views.users_profile, name='users_profile'),
    path('activate_user/<int:pk>/' , views.activate_user , name='activate_user'),
    path('deactivate_user/<int:pk>/' , views.deactivate_user , name='deactivate_user'),
    path('change_my_password/' , views.change_my_password , name='change_my_password'),
    path('all_users/' , views.my_users , name='all_users'),
    path('my_profile/' , views.my_profile , name='my_profile'),
    path('distributors/',views.distributor_list,name='all_distributors'),
    path('sales/',views.sales_list,name='all_sales_list'),
    path('accounts/',views.account_list,name='all_accounts'),
    path('warehouse/',views.warehouse_manager_list,name='all_warehouse_manager'),

]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)