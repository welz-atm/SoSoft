from .admin import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser,Guarantor,SalesDept,AccountDept,DistributorDept,GeneralDept,WarehouseDept,PurchaseDept,\
                                                                               Supplier,Department
from .utils import CATEGORIES,ROLES,SEX
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField


class InitialEmployeeForm(UserCreationForm):
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                                                  'First Name'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                                                 'Last Name'}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    job_role = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Role'}))
    sex = forms.ChoiceField(label='',widget=forms.Select(),choices=SEX)
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={'class':
                                                                                                'form-control'}))
    is_sales = forms.BooleanField()
    is_production = forms.BooleanField()
    is_purchase = forms.BooleanField()
    is_warehouse = forms.BooleanField()
    is_general = forms.BooleanField()
    is_accounts = forms.BooleanField()
    is_admin = forms.BooleanField()

    class Meta:
        model = CustomUser
        fields = ('is_admin','last_name','first_name', 'email','telephone','job_role','is_accounts','is_sales','is_purchase',\
                  'is_warehouse','is_general','is_production')

    def __init__(self, *args, **kwargs):
        super(InitialEmployeeForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].label = ''
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''


class InitialEmployeeEditForm(UserChangeForm):
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                         'First Name'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                        'Last Name'}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    job_role = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Job Role'}))
    sex = forms.ChoiceField(label='', widget=forms.Select(), choices=SEX)
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget())
    password = forms.CharField(label='', widget=forms.TextInput(attrs={'type': 'hidden'}))
    is_sales = forms.BooleanField()
    is_production = forms.BooleanField()
    is_purchase = forms.BooleanField()
    is_warehouse = forms.BooleanField()
    is_general = forms.BooleanField()
    is_accounts = forms.BooleanField()
    is_admin = forms.BooleanField()

    class Meta:
        model = CustomUser
        fields = ('is_admin','last_name','first_name', 'email','job_role','password','is_accounts','is_sales','is_purchase',
                  'is_warehouse','is_general','is_production')


class EmployeeFormNonEditable(forms.ModelForm):
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'First Name'}),disabled=True)
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Last Name'}),disabled=True)
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}),disabled=True)
    address = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Address'}))
    country = CountryField(multiple=False)
    image = forms.ImageField()
    telephone = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'placeholder': 'Telephone'}))

    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','email')


class GuarantorForm(forms.ModelForm):
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                                                  'First Name'}))
    other_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                                                  'Other Name'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                                                 'Last Name'}))
    user = forms.ModelChoiceField(label='',widget=forms.Select(attrs={'class':'form-control','placeholder':
                                                                      'Select Staff'}),queryset=CustomUser.objects.all())
    address = forms.CharField(label='',
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    state = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}))
    image = forms.ImageField()
    telephone = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder':
                                                                                                      'Telephone'}))

    class Meta:
        model = Guarantor
        fields = ('last_name','other_name','first_name','user','image','address','state','telephone',)


class DistributorForm(UserCreationForm):
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                                                  'First Name'}))
    other_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                                                  'Other Name'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                                                 'Last Name'}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    address = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    state = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}))
    telephone = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder':
                                                                                                      'Telephone'}))
    company_name = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                                                   'Company Name'}))
    company_reg = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                          'Company Registration Numer'}))
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={'class':
                                                                                                'form-control'}))
    image = forms.ImageField()
    assigned_to = forms.ModelChoiceField(label='', widget=forms.Select(attrs={'class': 'form-control',
                                                                              'placeholder': 'created_by'}),
                                         queryset=SalesDept.objects.all())

    class Meta:
        model = CustomUser
        fields = ('last_name','other_name','first_name', 'email','image','company_name','company_reg','address','state',
                  'country','telephone','assigned_to')

    def __init__(self, *args, **kwargs):
        super(DistributorForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].label = ''
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''


class DistributorEditForm(UserChangeForm):
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                                                  'First Name'}))
    other_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                                                  'Other Name'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                                                 'Last Name'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    address = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    state = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}))
    telephone = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder':
                                                                                                      'Telephone'}))
    job_role = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Role'}))
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={'class':
                                                                                                       'form-control'}))
    image = forms.ImageField()
    assigned_to = forms.ModelChoiceField(label='', widget=forms.Select(attrs={'class': 'form-control',
                                                                              'placeholder': 'created_by'}),
                                         queryset=SalesDept.objects.all())
    password = forms.CharField(label='', widget=forms.TextInput(attrs={'type': 'hidden'}))

    class Meta:
        model = CustomUser
        fields = ('last_name','other_name','first_name', 'email','image','company_name','company_reg','address','state',
                  'country','telephone','assigned_to',)

    def __init__(self, *args, **kwargs):
        super(DistributorEditForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].label = ''
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''


class SupplierForm(UserCreationForm):
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                                                  'First Name'}))
    other_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                                                  'Other Name'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                                                 'Last Name'}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    address = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    state = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}))
    telephone = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder':
                                                                                                      'Telephone'}))
    category = forms.ChoiceField(label='',widget=forms.Select(attrs={'class': 'form-control'},choices=CATEGORIES))
    company_name = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                                                   'Company Name'}))
    company_reg = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                          'Company Registration Number'}))
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={'class':
                                                                                                'form-control'}))
    image = forms.ImageField()

    class Meta:
        model = CustomUser
        fields = ('last_name','other_name','first_name', 'email','image','company_name','category','company_reg','address','state',
                  'country','telephone')

    def __init__(self, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].label = ''
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''


class SupplierEditForm(UserChangeForm):
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                  'First Name'}))
    other_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                  'Other Name'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                 'Last Name'}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    address = forms.CharField(label='',
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    state = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}))
    telephone = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder':
                                                                      'Telephone'}))
    company_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                    'Company Name'}))
    category = forms.ChoiceField(label='', widget=forms.Select(attrs={'class': 'form-control'}, choices=CATEGORIES))
    company_reg = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                   'Company Registration Number'}))
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={'class':
                                                                                                'form-control'}))
    image = forms.ImageField()

    class Meta:
        model = CustomUser
        fields = ('last_name', 'other_name', 'first_name', 'email', 'image', 'company_name','category', 'company_reg', 'address',
                  'state','country', 'telephone')

    def __init__(self, *args, **kwargs):
        super(SupplierEditForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].label = ''
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''


class SalesDeptForm(forms.ModelForm):
    role = forms.CharField(label='',widget=forms.Select(attrs={'class':'form-control','placeholder':'Position'},
                                                        choices=ROLES))

    class Meta:
        model = SalesDept
        fields = ('role',)


class AccountDeptForm(forms.ModelForm):
    role = forms.CharField(label='', widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Position'},
                                                         choices=ROLES))

    class Meta:
        model = AccountDept
        fields = ('role',)


class DistributorDeptForm(forms.ModelForm):
    role = forms.CharField(label='', widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Position'},
                                                         choices=ROLES))

    class Meta:
        model = DistributorDept
        fields = ('role',)


class GeneralDeptForm(forms.ModelForm):
    role = forms.CharField(label='', widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Position'},
                                                         choices=ROLES))

    class Meta:
        model = GeneralDept
        fields = ('role',)


class WarehouseDeptForm(forms.ModelForm):
    role = forms.CharField(label='', widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Position'},
                                                         choices=ROLES))

    class Meta:
        model = WarehouseDept
        fields = ('role',)


class PurchaseDeptForm(forms.ModelForm):
    role = forms.CharField(label='', widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Position'},
                                                         choices=ROLES))

    class Meta:
        model = PurchaseDept
        fields = ('role',)


class SupplierDeptForm(forms.ModelForm):
    role = forms.CharField(label='', widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Position'},
                                                         choices=ROLES))
    doc_cac = forms.FileField(label='',widget=forms.FileInput(attrs={'class':'form-control'}))
    doc_bank_ref = forms.FileField(label='',widget=forms.FileInput(attrs={'class':'form-control'}))

    class Meta:
        model = Supplier
        fields = ('role','doc_cac','doc_bank_ref',)


class DepartmentForm(forms.ModelForm):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                   'Name of Department'}))
    username = forms.EmailField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                        'Username'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':
                                                                           'Password'}))
    port = forms.IntegerField()
    protocol = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                       'TLS/SSL Port'}))
    server = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':
                                                                     'Mail Server'}))

    class Meta:
        model = Department
        fields = ('name','username','password','port','protocol','server',)
