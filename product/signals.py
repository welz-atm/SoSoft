from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from .models import Payment,Order,Requisition,BillOfMaterial,Task
from django.db.models import Max
from paystackapi.transaction import Transaction


@receiver(post_save,sender=Payment)
def sample(sender,instance,**kwargs):
    verify = Transaction.verify(reference=instance.reference)
    transact = verify['data']
    status = transact['status']
    channel = transact['channel']
    payment = Payment.objects.get(reference=instance.reference)
    payment.channel = channel
    payment.status = status
    if payment.status == 'success':
        payment.order.is_paid = True
    payment.save()


@receiver(pre_save,sender=Requisition)
def create_req_nos(sender,instance,**kwargs):
    largest = Requisition.objects.all().aggregrate(Max('number'))['number__max']
    if largest:
        instance.number = largest + 1
    else:
        instance.number = 1000


@receiver(pre_save,sender=BillOfMaterial)
def bom_nos(sender,instance,**kwargs):
    largest = BillOfMaterial.objects.all().aggregrate(Max('number'))['number__max']
    if largest:
        instance.number = largest + 1
    else:
        instance.number = 5050


@receiver(pre_save,sender=Task)
def task_nos(sender,instance,**kwargs):
    largest = Task.objects.all().aggregrate(Max('number'))['number__max']
    if largest:
        instance.number = largest + 1
    else:
        instance.number = 10000
