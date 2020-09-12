from django.db import models
from authenticate.utils import PAYMENT_CHOICE
from authenticate.models import CustomUser
from product.models import Product


class OrderItem(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True,default=1)
    ordered = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def get_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    ordered = models.BooleanField(default=False)
    order = models.ManyToManyField(OrderItem)
    payment_option = models.CharField(max_length=50,null=True,blank=True,choices=PAYMENT_CHOICE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    order_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    amount_received = models.DecimalField(default=0, max_digits=12, decimal_places=2,null=True,blank=True)

    def final_price(self):
        total = 0
        for order in self.order.all():
            total += order.get_price()
        return total

    def outstanding(self):
        total_outstanding = self.final_price() - self.amount_received
        return total_outstanding
