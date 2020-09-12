from django.db import models
from authenticate.models import CustomUser
from product.models import Item,Product,Approval
from django.core.validators import MinValueValidator,MaxValueValidator
from requisition.models import Quotation


class Production(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    no_of_workers = models.IntegerField(null=True,blank=True)

    def cost_produced(self):
        return self.product.price * self.quantity


class BomMaterial(models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    description = models.CharField(max_length=1000)
    unit_cost = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def cost(self):
        return self.quantity * self.unit_cost


class BillOfMaterial(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    number = models.PositiveIntegerField(unique=True,validators=[MinValueValidator(5050),MaxValueValidator(99999999)])
    quotation = models.ForeignKey(Quotation,on_delete=models.CASCADE,null=True,blank=True)
    material = models.ManyToManyField('BomMaterial')
    created_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    approved_by = models.ForeignKey(Approval,on_delete=models.CASCADE,null=True,blank=True)
    is_draft = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __int__(self):
        return 'BOM/{}'.format(self.number)

    def total_cost(self):
        total = 0
        for item in self.material.all():
            total += item.cost()
        return total
