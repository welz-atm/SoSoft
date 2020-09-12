from django import forms
from .models import Product,Order,Approval,OrderItem,Production,Warehouse,WarehouseItem,Sales,Item,Requisition,Email,\
                    Quotation,Task,BillOfMaterial,BomMaterial,Comment,Education,Skill,Candidate,Experience,Document
from authenticate.models import CustomUser,DistributorDept,SalesDept,Department
from authenticate.utils import CATEGORIES
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField


class ProductForm(forms.ModelForm):
    sku = forms.IntegerField(label='',widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':
                                                                                              'Stock Keeping Unit'}))
    name = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Name'}))
    price = forms.IntegerField(label='',widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Price'}))
    image = forms.ImageField()

    class Meta:
        model= Product
        fields = ('sku','name','price','image',)


class ItemForm(forms.ModelForm):
    name = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Name'}))
    description = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Description'}))
    image = forms.ImageField()
    category = forms.CharField(label='',widget=forms.Select(attrs={'class':'form-control'},choices=CATEGORIES))

    class Meta:
        model= Item
        fields = ('name','description','image','category',)


class OrderItemForm(forms.ModelForm):
    product = forms.ModelChoiceField(label='',widget=forms.Select(attrs={'class':'form-control','placeholder':
                                                                         'Product'}),queryset=Product.objects.all())
    quantity = forms.IntegerField(label='',widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':
                                                                                                   'Quantity'}),initial=1)
    user = forms.ModelChoiceField(label='', widget=forms.Select(attrs={'class': 'form-control', 'placeholder':
                                                                'Product'}), queryset=DistributorDept.objects.all())

    class Meta:
        model = OrderItem
        fields = ('product','quantity','user',)


class DistributorOrderItemForm(forms.ModelForm):
    product = forms.ModelChoiceField(label='',widget=forms.Select(attrs={'class':'form-control','placeholder':
                                                                         'Product'}),queryset=Product.objects.all())
    quantity = forms.IntegerField(label='',widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':
                                                                                                   'Quantity'}))

    class Meta:
        model = OrderItem
        fields = ('product','quantity',)


STATUS = [('Approved','Approved'),('Awaiting Approval','Awaiting Approval'),('Not Approved','Not Approved')]


class ApproveOrderForm(forms.ModelForm):
    status = forms.ChoiceField(label='',widget=forms.Select(attrs={'class':'form-control','placeholder':
                                                                   'Status'}),choices=STATUS)

    class Meta:
        model = Order
        fields = ('approval',)


class ApprovalForm(forms.ModelForm):
    status = forms.ChoiceField(label='',widget=forms.Select(attrs={'class':'form-control','placeholder':
                                                                   'Status'}),choices=STATUS)
    comment = forms.CharField(label='',widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Comment'}))

    class Meta:
        model = Approval
        fields = ('atatus','comment')


class CreateApprovalForm(forms.ModelForm):
    name = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Name'}))

    class Meta:
        model = Approval
        fields = ('name',)


class ProductionForm(forms.ModelForm):
    product = forms.ModelChoiceField(label='',widget=forms.Select(attrs={'class':'form-control','placeholder':
                                                                         'Product'}),queryset=Product.objects.all())
    quantity = forms.IntegerField(label='',widget=forms.NumberInput(attrs={'class':'form-control','placeholder':
                                                                                                  'Quantity'}))
    no_of_workers = forms.IntegerField(label='',widget=forms.NumberInput(attrs={'class':'form-control','placeholder':
                                                                                'Nos of Workers'}))

    class Meta:
        model = Production
        fields = ('product','quantity','no_of_workers',)


class EditProductionForm(forms.ModelForm):
    product = forms.ModelChoiceField(label='',widget=forms.Select(attrs={'class':'form-control','placeholder':
                                                                         'Product'}),queryset=Product.objects.all())
    quantity = forms.IntegerField(label='',widget=forms.NumberInput(attrs={'class':'form-control','placeholder':
                                                                                                  'Quantity'}))
    no_of_workers = forms.IntegerField(label='',widget=forms.NumberInput(attrs={'class':'form-control','placeholder':
                                                                                'Nos of Workers'}))

    class Meta:
        model = Production
        fields = ('product','quantity','no_of_workers',)


class WarehouseCreateForm(forms.ModelForm):
    name = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Name'}))
    address = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Address'}))
    state = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'State'}))
    owner = forms.ModelChoiceField(label='', widget=forms.Select(attrs={'class': 'form-control', 'placeholder':
                                   'Product'}), queryset=CustomUser.objects.filter(is_distributor=True))

    class Meta:
        model = Warehouse
        fields = ('name','address','state','owner',)


class WarehouseCompanyForm(forms.ModelForm):
    name = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Name'}))
    address = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Address'}))
    state = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'State'}))
    owner = forms.ModelChoiceField(label='', widget=forms.Select(attrs={'class': 'form-control', 'placeholder':
                                   'Product'}), queryset=CustomUser.objects.filter(is_warehouse=True))

    class Meta:
        model = Warehouse
        fields = ('name','address','state','owner',)


class WarehouseReceivedForm(forms.ModelForm):
    product = forms.ModelChoiceField(label='',widget=forms.Select(attrs={'class':'form-control','placeholder':
                                                                         'Product'}),queryset=Product.objects.all())
    received = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder':
                                                                                                     'Quantity Received'}))

    class Meta:
        model = WarehouseItem
        fields = ('product','received',)


class WarehouseSuppliedForm(forms.ModelForm):
    product = forms.ModelChoiceField(label='',widget=forms.Select(attrs={'class':'form-control','placeholder':
                                                                         'Product'}),queryset=Product.objects.all())
    supplied = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder':
                                                                                                     'Quantity Supplied'}))

    class Meta:
        model = WarehouseItem
        fields = ('product','supplied',)


class SalesForm(forms.ModelForm):
    product = forms.ModelChoiceField(label='',widget=forms.Select(attrs={'class':'form-control','placeholder':
                                                                         'Product'}),queryset=Product.objects.all())
    quantity = forms.IntegerField(label='',widget=forms.NumberInput(attrs={'class':'form-control','placeholder':
                                                                                                  'Quantity'}))
    name = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Name'}))
    telephone = forms.IntegerField(label='',widget=forms.NumberInput(attrs={'class':'form-control','placeholder':
                                                                                                   'Telephone'}))

    class Meta:
        model = Sales
        fields = ('name','telephone','product','quantity',)


class OrderForm(forms.ModelForm):
    address = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                               'Address'}))
    state = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                             'State'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    class Meta:
        model = Order
        fields = ('address','state','email',)


PAYMENT_CHOICE = (('Cash','Cash'),('Cheque','Cheque'),('Online Payment','Online Payment'))


class SelectPaymentForm(forms.ModelForm):
    payment_option = forms.CharField(label='Payment Option',widget=forms.Select(attrs={'class': 'form-control'},
                                                                                choices=PAYMENT_CHOICE))
    amount_received = forms.IntegerField(label='Amount Received',
                                         widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Price'}))

    class Meta:
        model = Order
        fields = ('payment_option','amount_received')


QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 26)]


class UpdateItemForm(forms.ModelForm):
    quantity = forms.TypedChoiceField(label='',choices=QUANTITY_CHOICES,
                                      widget=forms.Select(attrs={'class':'form-control','placeholder':'Quantity'}))

    class Meta:
        model = OrderItem
        fields = ('quantity',)


class RequisitionForm(forms.ModelForm):
    req_quantity = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder':
                                                                                                      'Telephone'}))
    req_item_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                            'Item Name'}))
    req_description = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':
                                                                             'Description'}))
    req_reason = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':
                                                                        'Reason'}))
    req_expiry = forms.DateTimeField(label='Expiry Date',widget=forms.DateInput(attrs={'class':'form-control'}))
    req_image = forms.ImageField()

    class Meta:
        model = Requisition
        fields = ('req_item_name','req_description','req_quantity','req_expiry','req_reason','req_image')


class QuotationForm(forms.ModelForm):
    discount = forms.IntegerField(label='Discount', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    forwarding_cost = forms.IntegerField(label='Forwarding Cost', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    tax = forms.IntegerField(label='Tax', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    comment = forms.CharField(label='',widget=forms.Textarea(attrs={'class':'form-control',
                                                                    'placeholder':'Comment'}))
    req_image = forms.ImageField()
    terms_and_condition = forms.CharField(label='',widget=forms.Textarea(attrs={'class':'form-control',
                                                                                'placeholder':'Terms and Conditions'}))

    class Meta:
        model = Quotation
        fields = ('discount','forwarding_cost','tax','comment','terms_and_condition','image',)


MAIL_STATUS = [('Working on It','Working on It'),('Work Completed','Work Completed'),('Escalated','Escalated'),
               ('Awaiting Customer Response','Awaiting Customer Response')]


class EmailForm(forms.ModelForm):
    from_email = forms.ModelMultipleChoiceField(label='',widget=forms.EmailInput(attrs={'class':'form-control',
                                                                          'placeholder':'Sender Email'}),queryset=Department.objects.filter())
    to_email = forms.EmailField(label='',widget=forms.EmailInput(attrs={'class':'form-control',
                                                                        'placeholder':'Recipient Email'}))
    subject = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                      'Subject of Email'}))
    message = forms.CharField(label='',widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Message'}))
    attachment = forms.FileField(label='',widget=forms.FileInput(attrs={'class':'form-control'}))

    class Meta:
        model = Email
        fields = ('from_email','to_email','subject','attachment','message','status',)


TASK_STATUS = [('In Progress','In Progress'),('Completed','Completed'),('Escalated','Escalated'),
               ('Awaiting Customer Response','Awaiting Customer Response')]


class TaskForm(forms.ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                             'Title'}))
    description = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':
                                                                  'Description'}))
    solution = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':
                                                                      'Solution'}))
    status = forms.ChoiceField(label='Status',widget=forms.Select(attrs={'class': 'form-control'},
                                                                  choices=TASK_STATUS))
    time_spent = forms.DateTimeField(label='',widget=forms.DateTimeInput())
    assigned_to = forms.ModelChoiceField(label='Assign To User',widget=forms.Select(attrs={'class':'form-control'}),queryset=CustomUser.objects.all())

    class Meta:
        model = Task
        fields = ('title','assigned_to','description','solution','status','time_spent')


class BillOfMaterialForm(forms.ModelForm):
    product = forms.ModelChoiceField(label='Select Product',widget=forms.Select(attrs={'class':'form-control'}),
                                     queryset=Product.objects.all())
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Solution'}))

    class Meta:
        model = BillOfMaterial
        fields = ('product','name',)
        
        
class BomMaterialForm(forms.ModelForm):
    item = forms.ModelChoiceField(label='',widget=forms.Select(attrs={'class': 'form-control'}),
                                  queryset=Item.objects.all())
    quantity = forms.IntegerField()
    description = forms.CharField(label='',widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'Description'}))

    class Meta:
        model = BomMaterial
        fields = ('item','quantity','description',)


class CommentForm(forms.ModelForm):
    description = forms.CharField(label='',widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Description'}))

    class Meta:
        model = Comment
        fields = ('description',)