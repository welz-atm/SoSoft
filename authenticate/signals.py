from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import CustomUser
from .models import SalesDept,AccountDept,DistributorDept,WarehouseDept,GeneralDept


@receiver(post_save,sender=CustomUser)
def dept_users(sender,created,instance,**kwargs):
    if created:
        sales = SalesDept.objects.create(user=instance)
        sales.role = 'member'
        sales.save()
