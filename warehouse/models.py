from django.db import models
from authenticate.models import CustomUser
from authenticate.utils import UNITS
from django.db.models import Sum
from product.models import Product,Item


class Warehouse(models.Model):
    name = models.CharField(max_length=15,null=True, blank=True)
    address = models.CharField(max_length=50,null=True, blank=True)
    state = models.CharField(max_length=20,null=True, blank=True)
    owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class WarehouseItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse,on_delete=models.CASCADE)
    received = models.IntegerField(null=True, blank=True,default=0)
    date = models.DateField(auto_now_add=True)
    supplied = models.IntegerField(null=True, blank=True,default=0)
    unit = models.CharField(max_length=12,null=True,blank=True,choices=UNITS,default='Pack(s)')
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    is_received = models.BooleanField(default=False)
    is_supplied = models.BooleanField(default=False)

    def get_stock(self):
        return self.received - self.supplied

    @staticmethod
    def total_received():
        received = WarehouseItem.objects.all().aggregate(Sum('received'))['received__sum']
        return received

    @staticmethod
    def total_supplied():
        supplied = WarehouseItem.objects.all().aggregate(Sum('supplied'))['supplied__sum']
        return supplied

    @staticmethod
    def total_stock():
        received = WarehouseItem.objects.all().aggregate(Sum('received'))['received__sum']
        supplied = WarehouseItem.objects.all().aggregate(Sum('supplied'))['supplied__sum']
        stock = received - supplied
        return stock
