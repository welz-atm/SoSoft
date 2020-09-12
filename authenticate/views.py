from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from .models import CustomUser,Department
from .forms import InitialEmployeeForm,InitialEmployeeEditForm,EmployeeFormNonEditable,DepartmentForm
from hr.forms import SkillForm,ExperienceForm,EducationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from hr.models import Skill,Experience,Education
from production.models import Production
from order.models import Order
from warehouse.models import Warehouse


@login_required()
def home_view(request):
    sales = CustomUser.objects.get(user=request.user)
    produced = Production.objects.all().count()
    purchased = Order.objects.filter(order_by=sales).aggregate(Sum('amount_received'))['amount_received__sum']
    warehouses = Warehouse.objects.all()

    context = {
        'produced': produced,
        'purchased': purchased,
        'warehouses': warehouses
    }
    return render(request,'authenticate/dashboard.html',context)


def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            xx = CustomUser.objects.get(email=email)
            if xx.is_authenticated and xx.is_active is True:
                login(request, user)
                messages.success(request, 'Welcome to Sosoft.')
                return redirect('home')
            else:
                messages.info(request,'Confirm your login details or Check with Administrator')

        else:
            messages.info(request,'Please confirm your login details ')
            return redirect('login')
    else:
        return render(request, 'authenticate/auth_login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have logged out successfully.')
    return redirect('login')


def register_user(request):
    if request.user.is_admin is True:
        if request.method == 'POST':
            form = InitialEmployeeForm(request.POST)
            if form.is_valid():
                employee = form.save(commit=False)
                employee.is_active = True
                employee.save
                return redirect('all_users')
        else:
            form = InitialEmployeeForm()
        context = {'form': form}
        return render(request, 'authenticate/form_component.html', context)
    else:
        raise PermissionDenied


def edit_user(request):
    if request.user.is_admin:
        if request.method == 'POST':
            form = InitialEmployeeEditForm(request.POST)
            if form.is_valid():
                employee = form.save(commit=False)
                employee.is_active = True
                employee.save
                return redirect('all_users')
        else:
            form = InitialEmployeeForm()
        context = {'form': form}
        return render(request, 'authenticate/form_component.html', context)
    else:
        raise PermissionDenied


def view_profile(request,pk):
    user = CustomUser.objects.get(pk=pk)
    skill = Skill.objects.filter(user=user).select_related('user')
    education = Education.objects.filter(user=user).select_related('user')
    experience = Experience.objects.filter(user=user).select_related('user')

    context = {
        'skill':skill,
        'education':education,
        'experience':experience,
        'user':user
    }
    return render(request,'authenticate/user_profile.html',context)


def my_profile(request):
    skill = Skill.object.get(user=request.user)
    education = Education.objects.get(user=request.user)
    experience = Experience.objects.get(user=request.user)

    context = {
        'skill': skill,
        'education':education,
        'experience': experience
    }
    return render(request,'my_profile.html',context)


def edit_profile(request):
    skill = Skill.objects.get(user=request.user)
    experience = Experience.objects.get(user=request.user)
    education = Education.objects.get(user=request.user)
    if request.method == 'POST':
        form = EmployeeFormNonEditable(request.POST, instance=request.user)
        skill_form = SkillForm(request.POST, instance=skill)
        education_form = EducationForm(request.POST, instance=education)
        experience_form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid() and skill_form.is_valid() and education_form.is_valid() and experience_form.is_valid():
            form.save()
            skill = skill_form.save(commit=False)
            skill.user = request.user
            skill.save()
            experience = skill_form.save(commit=False)
            experience.user = request.user
            experience.save()
            education = skill_form.save(commit=False)
            education.user = request.user
            education.save()
            return redirect('users_profile')
    else:
        form = EmployeeFormNonEditable(instance=request.user)
        skill_form = SkillForm(instance=skill)
        education_form = EducationForm(instance=education)
        experience_form = ExperienceForm(instance=experience)
    context = {
        'form': form,
        'skill_form': skill_form,
        'education_form': education_form,
        'experience_form': experience_form
    }
    return render(request, 'authenticate/edit_profile.html', context)


def activate_user(request,pk):
    active_user = CustomUser.objects.get(pk=pk)
    active_user.is_active = True
    active_user.save()
    messages.success(request,'User account has been activated')
    return redirect('all_users')


def deactivate_user(request,pk):
    active_user = CustomUser.objects.get(pk=pk)
    active_user.is_active = False
    active_user.save()
    messages.success(request,'User account has been deactivated')
    return redirect('all_users')


@login_required()
def change_my_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST , user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request,'Password changed successfully')
            return redirect('dashboard')

    else:
        form = PasswordChangeForm(user=request.user)
    context = {'form': form}
    return render(request, 'authenticate/change_user_password.html',context)


def my_users(request):
    all_users = CustomUser.objects.all().exclude(pk=1)
    context = {
        'all_users': all_users
    }
    return render(request, 'authenticate/users.html',context)


def sales_list(request):
    all_sales = CustomUser.objects.filter(is_sales=True)
    context = {
        'all_sales':all_sales
    }
    return render(request,'authenticate/sales_list.html',context)


def account_list(request):
    all_accounts = CustomUser.objects.filter(is_accounts=True)
    context = {
        'all_accounts':all_accounts
    }
    return render(request,'authenticate/account_list.html',context)


def warehouse_list(request):
    all_warehouse_manager = CustomUser.objects.filter(is_warehouse=True)
    context = {
        'all_warehouse_manager' : all_warehouse_manager
    }
    return render(request,'authenticate/warehouse_manager_list.html',context)


def purchasing_list(request):
    all_purchasing = CustomUser.objects.filter(is_purchase=True)
    context = {
        'all_purchasing' : all_purchasing
    }
    return render(request,'authenticate/purchasing_list.html',context)


def distributor_list(request):
    all_distributors = CustomUser.objects.filter(is_distributor=True)
    context = {
        'all_distributors':all_distributors
    }
    return render(request,'authenticate/distributor_list.html',context)


def supplier_list(request):
    all_suppliers = CustomUser.objects.filter(is_supplier=True)
    context = {
        'all_suppliers':all_suppliers
    }
    return render(request,'authenticate/suppliers_list.html',context)


def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            dept = form.save(commit=False)
            dept.is_member = True
            dept.save()
            return redirect('all_departments')
    else:
        form = DepartmentForm()
    context = {
        'form':form
    }
    context = {
        'form':form
    }
    return render(request,'product/create_department.html',context)