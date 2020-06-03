from django.contrib import admin
from .models import Product,Approval,Warehouse,Order,OrderItem,Production


class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name','address','state','created_by',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku' , 'name', 'price',)


class ApprovalAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name', )


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_date','user',)
    list_filter = ('order_date','user',)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order_date','product','quantity','user',)
    list_filter = ('order_date','product','user',)


class ProductionAdmin(admin.ModelAdmin):
    list_display = ('date','product','quantity',)
    list_filter = ('date','product',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Approval , ApprovalAdmin)
admin.site.register(Warehouse,WarehouseAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(Production,ProductionAdmin)