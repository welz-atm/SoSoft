from django import forms
from .models import Product,Order,Approval,OrderItem,Production,Warehouse,WarehouseItem,Sales
from authenticate.models import CustomUser


class ProductForm(forms.ModelForm):
    sku = forms.IntegerField(label='',widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':
                                                                                              'Stock Keeping Unit'}))
    name = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Name'}))
    price = forms.IntegerField(label='',widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Price'}))
    image = forms.ImageField()

    class Meta:
        model= Product
        fields = ('sku','name','price','image',)


class OrderItemForm(forms.ModelForm):
    product = forms.ModelChoiceField(label='',widget=forms.Select(attrs={'class':'form-control','placeholder':
                                                                         'Product'}),queryset=Product.objects.all())
    quantity = forms.IntegerField(label='',widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':
                                                                                                   'Quantity'}))

    class Meta:
        model = OrderItem
        fields = ('product','quantity',)


class ApproveOrderForm(forms.ModelForm):
    approval = forms.ModelChoiceField(label='',widget=forms.Select(attrs={'class':'form-control','placeholder':
                                                                          'Status'}),queryset=Approval.objects.all())

    class Meta:
        model = Order
        fields = ('approval',)


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

    class Meta:
        model = Warehouse
        fields = ('name','address','state',)


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