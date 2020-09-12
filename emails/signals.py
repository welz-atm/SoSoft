from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import Task
from django.db.models import Max


@receiver(pre_save,sender=Task)
def task_nos(sender,instance,**kwargs):
    largest = Task.objects.all().aggregrate(Max('number'))['number__max']
    if largest:
        instance.number = largest + 1
    else:
        instance.number = 10000
