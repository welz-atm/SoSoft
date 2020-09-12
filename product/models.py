from django.db import models
from authenticate.models import CustomUser
from authenticate.utils import CATEGORIES,STATUS
from order.models import Order


class Product(models.Model):
    sku = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=120, null=True, blank=True)
    price = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    category = models.CharField(max_length=50,choices=CATEGORIES)

    def __str__(self):
        return self.name


class Approval(models.Model):
    status = models.CharField(max_length=20, null=True, blank=True,choices=STATUS)
    comment = models.CharField(max_length=150,null=True,blank=True)
    approver = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    reference = models.CharField(max_length=25)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True,null=True)
    amount = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10,default='success',null=True, blank=True)
    channel = models.CharField(max_length=15,default='card',null=True, blank=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return self.reference


#class Target(models.Model):