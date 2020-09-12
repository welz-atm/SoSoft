"""easyerp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authenticate.urls')),
    path('product/', include('product.urls')),
    path('order/', include('order.urls')),
    path('sales/', include('sales.urls')),
    path('invoice/', include('invoice.urls')),
    path('requisition/', include('requisition.urls')),
    path('production/', include('production.urls')),
    path('warehouse/', include('warehouse.urls')),
    path('hr/', include('hr.urls')),
    path('emails/', include('emails.urls')),
    path("paystack", include(('paystack.urls','paystack'),namespace='paystack')),
]

if settings.DEBUG: # new
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
