from django.shortcuts import render
from .models import Warehouse,WarehouseItem
from authenticate.models import CustomUser
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.decorators import login_required


@login_required()
def create_warehouse(request):
    if request.method == 'POST':
        form = WarehouseCreateForm(request.POST)
        if form.is_valid():
            warehouse = form.save(commit=False)
            warehouse.save()
            messages.success(request,'Warehouse created successfully')
            return redirect('all_warehouses')
    else:
        form = WarehouseCreateForm()
    context = {
          'form':form
        }
    return render(request,'product/create_warehouse.html',context)


@login_required()
def create_company_warehouse(request):
    if request.method == 'POST':
        form = WarehouseCompanyForm(request.POST)
        if form.is_valid():
            warehouse = form.save(commit=False)
            warehouse.save()
            messages.success(request,'Warehouse created successfully')
            return redirect('all_warehouses')
    else:
        form = WarehouseCompanyForm()
    context = {
          'form':form
        }
    return render(request,'product/create_company_warehouse.html',context)


@login_required()
def edit_warehouse(request,pk):
    warehouse = Warehouse.objects.get(pk=pk)
    if request.method == 'POST':
        form = WarehouseCreateForm(request.POST , instance=warehouse)
        if form.is_valid():
            form.save()
            messages.success(request,'Warehouse created successfully')
            return redirect('all_warehouses')
    else:
        form = WarehouseCreateForm(instance=warehouse)
    context = {
          'form':form
        }
    return render(request,'product/edit_warehouse.html',context)


@login_required()
def delete_warehouse(request,pk):
    warehouse = Warehouse.objects.get(pk=pk)
    warehouse.delete()
    return redirect('all_warehouses')


@login_required()
def all_warehouse(request):
    warehouses = Warehouse.objects.all()
    context = {
        'warehouses':warehouses
    }
    return render(request,'product/all_warehouses.html',context)


@login_required()
def my_warehouse(request):
    my_warehouses = Warehouse.objects.filter(user=request.user)
    context = {
        'my_warehouses': my_warehouses
    }
    return render(request,'product/my_warehouse.html',context)


@login_required()
def warehouse_stock(request):
    warehouse = Warehouse.objects.all().aggregate(Sum('received'))['received_sum']
    ware = Warehouse.objects.all().aggregate(Sum('supplied'))['supplied_sum']
    total = warehouse - ware
    context = {
        'total':total
    }
    return render(request,'product/stock.html',context)


@login_required()
def create_warehouse_received(request):
    if request.user.is_warehouse is True:
        if request.method == 'POST':
            form = WarehouseReceivedForm(request.POST)
            if form.is_valid():
                warehouse = Warehouse.objects.get(owner=request.user)
                received = form.save(commit=False)
                received.is_received = True
                received.warehouse = warehouse
                received.user = request.user
                received.save()
                return redirect('all_received')
        else:
            form = WarehouseReceivedForm()
        context = {
            'form':form
        }
        return render(request,'product/create_received.html',context)
    elif request.user.is_distributor is True:
        if request.method == 'POST':
            form = WarehouseReceivedForm(request.POST)
            if form.is_valid():
                warehouse = Warehouse.objects.get(owner=request.user)
                received = form.save(commit=False)
                received.is_received = True
                received.warehouse = warehouse
                received.user = request.user
                received.save()
                return redirect('all_received')
        else:
            form = WarehouseReceivedForm()
        context = {
            'form':form
        }
        return render(request,'product/create_received.html',context)
    else:
        return HttpResponse('You do not have access to this page')


@login_required()
def to_supply(request):
    supplied = Order.objects.filter(is_paid=True,is_shipped=False)
    context = {
        'supply':supplied
    }
    return render(request,'product/not_supplied.html',context)


@login_required()
def approve_supplied(request,pk):
    approved = Order.objects.get(pk=pk)
    approved.is_supplied = True
    approved.save()
    return redirect('supplied')


@login_required()
def not_supplied(request,pk):
    approved = Order.objects.get(pk=pk)
    approved.is_supplied = False
    approved.save()
    return redirect('supplied')


@login_required()
def delete_received(request,pk):
    to_delete = WarehouseItem.objects.get(pk=pk)
    to_delete.delete()
    return redirect('all_received')


@login_required()
def delete_supplied(request,pk):
    to_delete = WarehouseItem.objects.get(pk=pk)
    to_delete.delete()
    return redirect('all_supplied')


@login_required()
def edit_received(request,pk):
    received = WarehouseItem.objects.get(pk=pk)
    if request.method == 'POST':
        form = WarehouseReceivedForm(request.POST,instance=received)
        if form.is_valid():
            form.save()
            return redirect('all_received')
    else:
        form = WarehouseReceivedForm(request.POST)
    context = {
        'form':form
    }
    return render(request,'product/edit_received.html',context)


@login_required()
def all_received(request):
    received = WarehouseItem.objects.filter(is_received=True,user=request.user).order_by('date')
    context = {
        'received':received
    }
    return render(request,'product/all_received.html',context)


@login_required()
def all_supplied(request):
    supplied = Order.objects.filter(is_shipped=True,user=request.user).order_by('order_date')
    context = {
        'supplied':supplied
    }
    return render(request,'product/all_supplied.html',context)


@login_required()
def general_received(request):
    received = WarehouseItem.objects.filter(is_received=True).order_by('date')
    context = {
        'received':received
    }
    return render(request,'product/all_received.html',context)


@login_required()
def general_supplied(request):
    supplied = Order.objects.filter(is_shipped=True).order_by('order_date')
    context = {
        'supplied':supplied
    }
    return render(request,'product/all_supplied.html',context)


@login_required()
def distributor_supplied(request):
    supplied = WarehouseItem.objects.filter(is_supplied=True, user=request.user).order_by('date')
    context = {
        'supplied': supplied
    }
    return render(request, 'product/all_supplied.html', context)


@login_required()
def stock_warehouse(request):
    warehouses = Warehouse.objects.all()
    context = {
        'warehouses': warehouses
    }
    return render(request, 'product/stock_warehouse.html', context)


@login_required()
def stock(request,pk):
    user = CustomUser.objects.get(pk=pk)
    warehouses = WarehouseItem.objects.filter(user=user)
    context = {
        'warehouses':warehouses
    }
    return render(request,'product/stock.html',context)
