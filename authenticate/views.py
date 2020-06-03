from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from .models import CustomUser
from product.models import Warehouse,Production,Order
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import EmployeeEditForm,EmployeeForm,GuarantorForm,DistributorForm
from datetime import date


@login_required()
def home_view(request):
    return render(request ,'authenticate/index.html',{})


def choose_dept(request):
    return render(request,'authenticate/choose_dept.html',{})


def dashboard(request):
    produced = Production.objects.all().count()
    purchased = Order.objects.filter(is_paid=True).count()
    warehouses = Warehouse.objects.all()

    context = {
        'produced':produced,
        'purchased':purchased,
        'warehouses':warehouses
    }
    return  render(request,'authenticate/dashboard.html',context)


def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            xx = CustomUser.objects.get(email=email)
            if xx.is_authenticated and xx.is_active is True and xx.is_sales is True:
                login(request, user)
                messages.success(request, 'You have logged in successfully.')
                return redirect('home')
            elif xx.is_authenticated and xx.is_active is True and xx.is_accounts is True:
                login(request, user)
                messages.success(request, 'You have logged in successfully.')
                return redirect('home')
            elif xx.is_authenticated and xx.is_active is True and xx.is_distributor is True:
                login(request, user)
                messages.success(request, 'You have logged in successfully.')
                return redirect('home')
            elif xx.is_authenticated and xx.is_active is True and xx.is_warehouse is True:
                login(request, user)
                messages.success(request, 'You have logged in successfully.')
                return redirect('home')
            elif xx.is_authenticated and xx.is_active is True and xx.is_general is True:
                login(request, user)
                messages.success(request, 'You have logged in successfully.')
                return redirect('home')
            else:
                messages.info(request,'Confirm your login details or Check with Administrator')

        else:
            messages.success(request,'Please confirm your login details ')
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have logged out successfully.')
    return redirect('login')


def register_sales(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST,request.FILES)
        if form.is_valid():
            sales = form.save(commit=False)
            sales.is_sales = True
            sales.save()
            return redirect('all_sales_list')

    else:
        form = EmployeeForm()
    context = {'form': form}
    return render(request, 'authenticate/register_sales.html', context)


def register_account(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST,request.FILES)
        if form.is_valid():
            account = form.save(commit=False)
            account.is_accounts = True
            account.save()
            return redirect('all_accounts')

    else:
        form = EmployeeForm()
    context = {'form': form}
    return render(request, 'authenticate/register_account.html', context)


def register_warehouse_manager(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST,request.FILES)
        if form.is_valid():
            warehouse = form.save(commit=False)
            warehouse.is_warehouse = True
            warehouse.save()
            return redirect('all_warehouse_manager')

    else:
        form = EmployeeForm()
    context = {'form': form}
    return render(request, 'authenticate/register_warehouse_manager.html', context)


def register_distributor(request):
    if request.method == 'POST':
        form = DistributorForm(request.POST,request.FILES)
        if form.is_valid():
            distributor = form.save(commit=False)
            distributor.is_distributor = True
            distributor.save()
            return redirect('all_distributors')

    else:
        form = DistributorForm()
    context = {'form': form}
    return render(request, 'authenticate/register_distributor.html', context)


def register_general(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST,request.FILES)
        if form.is_valid():
            general = form.save(commit=False)
            general.is_general = True
            general.save()
            return redirect('all_users')

    else:
        form = EmployeeForm()
    context = {'form': form}
    return render(request, 'authenticate/register_general.html', context)


def register_guarantor(request):
    if request.method == 'POST':
        form = GuarantorForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('guarantors')
    else:
        form = GuarantorForm()
    context = {
        'form': form
    }
    return render(request,'authentication/register_guarantor.html',context)


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
def users_profile(request,pk):
    profile = CustomUser.objects.get(pk=pk)
    context = {
               'profile':profile
               }
    return render(request,'authenticate/users_profile.html',context)


@login_required()
def my_profile(request):
    if request.user.is_sales is True:
        if request.method == 'POST':
            form = EmployeeEditForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Update successful.')
                return redirect('my_profile')

        else:
            form = EmployeeEditForm(instance=request.user)
        context = {'form': form}
        return render(request, 'profile.html', context)

    elif request.user.is_account is True:
        if request.method == 'POST':
            form = EmployeeEditForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Update successful.')
                return redirect('my_profile')

        else:
            form = EmployeeEditForm(instance=request.user)
        context = {'form': form}
        return render(request, 'profile.html', context)

    elif request.user.is_warehouse is True:
        if request.method == 'POST':
            form = EmployeeEditForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Update successful.')
                return redirect('my_profile')

        else:
            form = EmployeeEditForm(instance=request.user)
        context = {'form': form}
        return render(request, 'profile.html', context)

    elif request.user.is_distributor is True:
        if request.method == 'POST':
            form = EmployeeEditForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Update successful.')
                return redirect('my_profile')

        else:
            form = EmployeeEditForm(instance=request.user)
        context = {'form': form}
        return render(request, 'profile.html', context)
    else:
        if request.method == 'POST':
            form = EmployeeEditForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Update successful.')
                return redirect('my_profile')

        else:
            form = EmployeeEditForm(instance=request.user)
        context = {'form': form}
        return render(request, 'profile.html', context)


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
    all_users = CustomUser.objects.all()
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


def warehouse_manager_list(request):
    all_warehouse_manager = CustomUser.objects.filter(is_warehouse=True)
    context = {
        'all_warehouse_manager' : all_warehouse_manager
    }
    return render(request,'authenticate/warehouse_manager_list.html',context)


def distributor_list(request):
    all_distributors = CustomUser.objects.filter(is_distributor=True)
    context = {
        'all_distributors':all_distributors
    }
    return render(request,'authenticate/distributor_list.html',context)