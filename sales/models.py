from django.db import models
from product.models import Product
from authenticate.models import CustomUser


class Sales(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(null=True, blank=True)
    sold_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=True, blank=True)
    telephone = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{} sold'.format(self.product)
