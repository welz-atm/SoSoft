from django.db import models
from authenticate.models import CustomUser


class Product(models.Model):
    sku = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=120, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Approval(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.name


class Warehouse(models.Model):
    name = models.CharField(max_length=15,null=True, blank=True)
    address = models.CharField(max_length=50,null=True, blank=True)
    state = models.CharField(max_length=20,null=True, blank=True)
    created_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class WarehouseItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    received = models.IntegerField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    supplied = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    is_received = models.BooleanField(default=False)
    is_supplied = models.BooleanField(default=False)

    def get_stock(self):
        return self.received - self.supplied


class OrderItem(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True,default=1)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def get_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    is_shipped = models.BooleanField(default=False)
    order = models.ManyToManyField(OrderItem)
    first_name = models.CharField(max_length=50,null=True,blank=True)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    address = models.CharField(max_length=50,null=True,blank=True)
    state = models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_fullname

    def final_price(self):
        total = 0
        for order in self.order.all():
            total += order.get_price()
        return total


class Production(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    no_of_workers = models.IntegerField(null=True,blank=True)

    def cost_produced(self):
        return self.product.price * self.quantity


class Stock(models.Model):
    warehouse = models.ForeignKey(Warehouse,on_delete=models.CASCADE)
    produced = models.ManyToManyField(Production)
    in_stock = models.ManyToManyField(WarehouseItem)

    def total_produced(self):
        total = 0
        for produce in self.produced.all():
            total += produce.quantity
            return total

    def total_received(self):
        total = 0
        for stock in self.in_stock.all():
            total += stock.received
            return total

    def total_supplied(self):
        total = 0
        for stock in self.in_stock.all():
            total += stock.supplied
            return total

    def total_stock(self):
        total = 0
        for stock in self.in_stock.all():
            total += stock.get_stock
            return total


class Sales(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(null=True, blank=True)
    sold_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=True, blank=True)
    telephone = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{} sold'.format(self.product)




