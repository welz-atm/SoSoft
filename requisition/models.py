from django.db import models
from .models import Requisition
from emails.models import Task,Comment
from authenticate.models import CustomUser
from product.models import Approval
from production.models import BillOfMaterial
from authenticate.utils import EXPENSE_TYPE,PAID_BY,CATEGORIES
from django.core.validators import MinValueValidator,MaxValueValidator


class Expense(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=1000)
    expense_type = models.CharField(max_length=50,choices=EXPENSE_TYPE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    approval = models.ForeignKey(Approval,on_delete=models.CASCADE,null=True,blank=True)
    task = models.ForeignKey(Task,on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,null=True,blank=True)
    requisition = models.ForeignKey(Requisition,on_delete=models.CASCADE,null=True,blank=True)
    amount = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    paid_by = models.CharField(max_length=255,choices=PAID_BY)


class Quotation(models.Model):
    requisition = models.ForeignKey(Requisition,on_delete=models.CASCADE)
    discount = models.IntegerField(null=True,blank=True)
    forwarding_cost = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    is_quoted = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField()
    tax = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    item_cost = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    comment = models.CharField(max_length=250,null=True,blank=True)
    terms_and_condition = models.CharField(max_length=250)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def total_quote(self):
        discount = self.discount * self.item_cost / 100
        total = self.forwarding_cost + self.tax + discount
        return total


class PurchaseOrder(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    quotation = models.ForeignKey(Quotation,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    is_requested = models.BooleanField(default=False)


class Requisition(models.Model):
    req_date = models.DateTimeField(auto_now_add=True)
    req_nos = models.PositiveIntegerField(unique=True,validators=[MinValueValidator(1000),
                                          MaxValueValidator(99999999)])
    approval = models.ForeignKey(Approval, on_delete=models.CASCADE, null=True, blank=True,default='Awaiting Approval')
    is_approved = models.BooleanField(default=False)
    req_category = models.CharField(max_length=100,choices=CATEGORIES)
    is_rfq = models.BooleanField(default=False)
    supplier = models.ForeignKey(CustomUser,related_name='req_supplier',on_delete=models.CASCADE,null=True,blank=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    req_item_name = models.CharField(max_length=50, null=True, blank=True)
    req_quantity = models.IntegerField(default=1)
    req_description = models.CharField(max_length=200)
    req_reason = models.CharField(max_length=200)
    req_expiry = models.DateTimeField(null=True, blank=True)
    req_image = models.ImageField(null=True, blank=True)
    bill_of_material = models.ForeignKey(BillOfMaterial,on_delete=models.CASCADE,null=True,blank=True)

    def __int__(self):
        return 'REQ/{}/{}'.format(self.req_date,self.req_nos)



