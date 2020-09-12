from django.db import models
from authenticate.models import CustomUser,Department
from authenticate.utils import MAIL_STATUS,TASK_STATUS
from django.core.validators import MinValueValidator,MaxValueValidator


class Email(models.Model):
    from_email = models.ForeignKey(Department,on_delete=models.CASCADE)
    to_email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=200,null=True,blank=True)
    message = models.CharField(max_length=1500)
    attachment = models.FileField(upload_to="files/")
    time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=MAIL_STATUS,null=True,blank=True)
    is_inc = models.BooleanField(default=False)
    is_out = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True,related_name='user_status')
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)


class Task(models.Model):
    title = models.CharField(max_length=150)
    number = models.PositiveIntegerField(unique=True,validators=[MinValueValidator(10000),
                                         MaxValueValidator(99999999)])
    description = models.CharField(max_length=1500)
    solution = models.CharField(max_length=1500)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=TASK_STATUS)
    email = models.ForeignKey(Email,on_delete=models.CASCADE,null=True,blank=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    comment = models.ManyToManyField('Comment')
    time_spent = models.DateTimeField(null=True,blank=True)
    assigned_to = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Comment(models.Model):
    description = models.CharField(max_length=1000,null=True,blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)