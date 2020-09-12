from django.contrib import admin
from .models import Product,Approval,Warehouse,Order,OrderItem,Production,WarehouseItem,Sales,Payment,Item


class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name','address','state','owner',)


class WarehouseItemAdmin(admin.ModelAdmin):
    list_display = ('date','product','received','supplied',)


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


class SalesAdmin(admin.ModelAdmin):
    list_display = ('product','quantity','sold_by',)
    list_filter = ('product','quantity','sold_by',)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('date','user','reference','amount','channel','status',)
    list_filter = ('date','user','reference','channel','status',)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name','description',)


admin.site.register(Sales, SalesAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Approval , ApprovalAdmin)
admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(WarehouseItem, WarehouseItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Production, ProductionAdmin)
admin.site.register(Item, ItemAdmin)