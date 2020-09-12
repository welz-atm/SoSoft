from django.db import models
from authenticate.models import CustomUser
from authenticate.utils import LEAVE_TYPE,EXPENSE_TYPE,PAID_BY
from requisition.models import Requisition
from product.models import Approval
from emails.models import Task,Comment


class Experience(models.Model):
    company_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    job_description = models.CharField(max_length=500)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)


class Skill(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Education(models.Model):
    sch_name = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    year_started = models.DateTimeField()
    year_finished = models.DateTimeField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    dob = models.DateTimeField()
    skills = models.ManyToManyField(Skill)
    education = models.ManyToManyField(Education)
    experience = models.ManyToManyField(Experience)


class Leave(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    leave_type = models.CharField(max_length=255,choices=LEAVE_TYPE)
    note = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    date_applied = models.DateTimeField(auto_now_add=True)
    approval = models.ForeignKey(Approval,on_delete=models.CASCADE)


class Document(models.Model):
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=25,choices=DOC_TYPE)
    form = models.FileField()
    can_access = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    can_edit = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
