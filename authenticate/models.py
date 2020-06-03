from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django_countries.fields import CountryField


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):

        user = self.create_user(
            email,
            password=password

        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email= models.EmailField(verbose_name='email address',max_length=255,unique=True)
    first_name = models.CharField(max_length=120)
    other_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    company_name = models.CharField(max_length=120,null=True,blank=True)
    company_reg = models.IntegerField(null=True, blank=True)
    last_login = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_sales = models.BooleanField(default=False)
    is_accounts = models.BooleanField(default=False)
    is_general = models.BooleanField(default=False)
    is_distributor = models.BooleanField(default=False)
    is_warehouse = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    address = models.CharField(max_length=254, null=True, blank=True)
    state = models.CharField(max_length=15, null=True, blank=True)
    country = CountryField(multiple=False)
    image = models.ImageField()
    telephone = models.IntegerField(null=True, blank=True)
    job_role = models.CharField(max_length=20)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_fullname(self):
        return '{} {}'.format(self.last_name,self.first_name)


class Guarantor(models.Model):
    first_name = models.CharField(max_length=120,null=True,blank=True)
    other_name = models.CharField(max_length=120,null=True,blank=True)
    last_name = models.CharField(max_length=120,null=True,blank=True)
    address = models.CharField(max_length=50,null=True,blank=True)
    state = models.CharField(max_length=50,null=True,blank=True)
    telephone = models.IntegerField(null=True,blank=True)
    image = models.ImageField()
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.first_name,self.last_name)
