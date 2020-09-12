from django import forms
from .models import Education,Skill,Candidate,Experience,Document
from authenticate.models import CustomUser
from authenticate.utils import LEAVE_TYPE,PAID_BY,EXPENSE_TYPE
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField


class SkillForm(forms.ModelForm):
    name = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Skill Name'}))

    class Meta:
        model = Skill
        fields = ('name',)


class ExperienceForm(forms.ModelForm):
    company_name = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Company Name'}))
    job_title = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Job Title'}))
    job_description = forms.CharField(label='',widget=forms.TextArea(attrs={'class':'form-control','placeholder':'Job Description'}))
    start_date = forms.DateTimeField(label='Date Started',widget=forms.DateTimeField())
    end_date = forms.DateTimeField(label='Date Ended',widget=forms.DateTimeField())

    class Meta:
        model = Experience
        fields = ('company_name','job_title','job_description','start_date','end_date',)


class CandidateForm(forms.ModelForm):
    name = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Company Name'}))
    email = forms.EmailField(label='',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}))
    address = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Company Name'}))
    state = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Company Name'}))
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={'class':
                                                                                                       'form-control'}))
    dob = forms.DateTimeField()

    class Meta:
        model = Candidate
        fields = ('name','email','address','state','country',)


class EducationForm(forms.ModelForm):
    sch_name = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'School Name'}))
    qualification = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':
                                                                           'Qualification'}))
    year_started = forms.DateTimeField(label='Date Started',widget=forms.DateTimeField())
    year_finished = forms.DateTimeField(label='Date Ended',widget=forms.DateTimeField())

    class Meta:
        model = Education
        fields = ('sch_name','qualification','year_started','year_finished',)


class DocumentForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    form = forms.FileField()
    can_access = forms.ModelMultipleChoiceField(label='',widget=forms.SelectMultiple(attrs={'class':'form-control'}),
                                                queryset=CustomUser.objects.all())
    can_edit = forms.BooleanField(label='',widget=forms.CheckboxInput(attrs={'class':'form-control'}))

    class Meta:
        model = Document
        fields = ('title','file','can_access','can_edit',)


class LeaveForm(forms.ModelForm):
    start_date = forms.DateTimeField(label='',widget=forms.DateTimeInput())
    end_date = forms.DateTimeField(label='',widget=forms.DateTimeInput())
    leave_type = forms.ChoiceField(label='',widget=forms.Select(attrs={'class':'form-control'},choices=LEAVE_TYPE))
    note = forms.CharField(label='',widget=forms.Textarea(attrs={'class':'form-control','placeholder':'School Name'}))
    date_applied = forms.DateTimeField(label='',widget=forms.DateTimeInput(attrs={'class':'form-control'}))

    class Meta:
        model = Leave
        fields = ('start_date','end_date','leave_type','note',)


class ExpenseForm(forms.ModelForm):
    date = forms.DateTimeField(label='',widget=forms.DateTimeInput(attrs={'class':'form-control'}))
    description = forms.CharField(label='',widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Description'}))
    expense_type = forms.ChoiceField(label='',widget=forms.Select(attrs={'class':'form-control'},choices=EXPENSE_TYPE))
    task = forms.ModelChoiceField(label='',widget=forms.Select(attrs={'class':'form-control'}),
                                  queryset=Task.objects.all())
    requisition = forms.ModelChoiceField(label='',widget=forms.Select(attrs={'class':'form-control'}),
                                         queryset=Requisition.objects.all())
    amount = forms.DecimalField(label='',widget=forms.NumberInput(attrs={'class':'form-control','placeholder':
                                                                  'Amount'}),max_digits=12,max_value=2)
    paid_by = forms.ChoiceField(label='',widget=forms.Select(attrs={'class':'form-control'},choices=PAID_BY))

    class Meta:
        model = Expense
        fields = ('date','description','expense_type','task','requisition','amount','paid_by',)