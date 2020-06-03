from django.shortcuts import render,redirect,HttpResponse
from .forms import  ProductForm,OrderItemForm,CreateApprovalForm,ApproveOrderForm,ProductionForm,EditProductionForm,\
                                                                        WarehouseCreateForm,WarehouseSuppliedForm,\
                                                                        WarehouseReceivedForm,SalesForm,OrderForm
from .models import Product,Order,Approval,OrderItem,Production,Warehouse,WarehouseItem,Sales
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from paystackapi.paystack import Paystack


@login_required()
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request ,'Task created successfully')
            return redirect('all_products')
    else:
        form = ProductForm(request.POST)
    context = {
        'form': form
    }
    return render(request,'product/create_product.html',context)


@login_required()
def all_products(request):
    products = Product.objects.all()
    context = {
        'products':products
    }
    return render(request,'product/all_products.html',context)


@login_required()
def edit_product(request , pk):
    edit = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST , instance=edit)
        if form.is_valid():
            form.save()
            messages.success(request ,'Task created')
            return redirect('all_products')
    else:
        form = ProductForm(instance=edit)
    context = {
        'form': form
    }
    return render(request,'product/edit_product.html',context)


@login_required()
def delete_product(request,pk):
    to_delete = Product.objects.get(pk=pk)
    to_delete.delete()
    return redirect ('all_products')


@login_required()
def create_approval(request):
    if request.method == 'POST':
        form = CreateApprovalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request ,'Task created successfully')
            return redirect('all_approvals')
    else:
        form = CreateApprovalForm(request.POST)
    context = {
        'form': form
    }
    return render(request,'product/create_approval.html',context)


@login_required()
def all_approvals(request):
    approvals = Approval.objects.all().order_by('id')
    context = {
        'approvals':approvals
    }
    return render(request,'product/all_approvals.html',context)


@login_required()
def edit_approval(request , pk):
    edit = Approval.objects.get(pk=pk)
    if request.method == 'POST':
        form = CreateApprovalForm(request.POST , instance=edit)
        if form.is_valid():
            form.save()
            messages.success(request ,'Order created')
            return redirect('all_approvals')
    else:
        form = CreateApprovalForm(instance=edit)
    context = {
        'form': form
    }
    return render(request,'product/edit_approval.html',context)


@login_required()
def delete_approval(request , pk):
    to_delete = Approval.objects.get(pk=pk)
    to_delete.delete()
    return redirect ('all_approvals')


@login_required()
def all_orders(request):
    orders = Order.objects.filter(is_paid=True).order_by('-order_date')
    context = {
        'orders':orders
    }
    return render(request,'product/all_orders.html',context)


def pending_order(request):
    pending = Order.objects.filter(user=request.user,is_paid=False).order_by('-order_date')
    context = {
        'pending':pending
    }
    return render(request,'product/pending_orders.html',context)


@login_required()
def delete_order(request , pk):
    to_delete = Order.objects.get(pk=pk)
    to_delete.delete()
    return redirect ('all_orders')


def view_order(request,pk):
    view = Order.objects.get(pk=pk)
    context = {
        'view': view
    }
    return render(request,'product/view_order.html',context)


def my_orders(request):
    orders = Order.objects.filter(user=request.user,is_paid=True)
    context = {
        'order': orders
    }
    return render(request,'product/my_orders.html',context)


def add_cart(request,pk):
    product = Product.objects.get(pk=pk)
    order_item,created = OrderItem.objects.get_or_create(product=product,user=request.user)
    orders = Order.objects.filter(user=request.user)
    if orders.exists():
        order = orders[0]
        if order.order.filter(product=product).exists():
            order_item.quantity += 1
            order_item.save()
            return redirect('order_summary')
        else:
            order.order.add(order_item)
            return redirect('order_summary')
    else:
        order = Order.objects.create(
            user=request.user)
        order.order.add(order_item)
        messages.info(request, "Product Added")
        return redirect("order_summary")


def remove_from_cart(request,pk):
    ordered_item = OrderItem.objects.get(pk=pk)
    ordered_item.delete()
    return redirect('my_cart')


def checkout(request):
    return render(request,'product/checkout.html',{})


def order_summary(request):
    orders = Order.objects.get(user = request.user)
    context = {
        'orders':orders
    }
    return render(request,'product/order_summary.html',context)


def create_production(request):
    if request.method == 'POST':
        form = ProductionForm(request.POST)
        if form.is_valid():
            production = form.save(commit=False)
            production.user = request.user
            production.save()
            messages.success(request,'Submitted Successfully')
            return redirect('all_production')
    else:
        form = ProductionForm()
    context = {
        'form':form
    }
    return render(request,'product/create_production.html',context)


def edit_production(request):
    if request.method == 'POST':
        form = EditProductionForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'Saved successfully')
            return redirect('all_production')
    else:
        form = EditProductionForm(request.POST,instance=request.user)
    context = {
        'form':form
    }
    return render(request,'product/edit_production.html',context)


def all_production(request):
    production = Production.objects.all().order_by('date')
    context = {
        'production':production
    }
    return render(request,'product/all_production.html',context)


def delete_production(request,pk):
    product = Production.objects.get(pk=pk)
    product.delete()
    return redirect('all_production')


def create_warehouse(request):
    if request.method == 'POST':
        form = WarehouseCreateForm(request.POST)
        if form.is_valid():
            warehouse = form.save(commit=False)
            warehouse.created_by = request.user
            warehouse.save()
            messages.success(request,'Warehouse created successfully')
            return redirect('all_warehouses')
    else:
        form = WarehouseCreateForm()
    context = {
          'form':form
        }
    return render(request,'product/create_warehouse.html',context)


def edit_warehouse(request,pk):
    warehouse = Warehouse.objects.get(pk=pk)
    if request.method == 'POST':
        form = WarehouseCreateForm(request.POST , instance=warehouse)
        if form.is_valid():
            form.save()
            messages.success(request,'Warehouse created successfully')
            return redirect('all_warehouses')
    else:
        form = WarehouseCreateForm()
    context = {
          'form':form
        }
    return render(request,'product/edit_warehouse.html',context)


def delete_warehouse(request,pk):
    product = Production.objects.get(pk=pk)
    product.delete()
    return redirect('all_warehouses')


def all_warehouse(request):
    warehouses = Warehouse.objects.all()
    context = {
        'warehouses':warehouses
    }
    return render(request,'product/all_warehouses.html',context)


def my_warehouse(request):
    my_warehouses = Warehouse.objects.filter(user=request.user)
    context = {
        'my_warehouses': my_warehouses
    }
    return render(request,'product/my_warehouse.html',context)


def warehouse_stock(request):
    warehouse = Warehouse.objects.all().aggregate(Sum('received'))['received_sum']
    ware = Warehouse.objects.all().aggregate(Sum('supplied'))['supplied_sum']
    total = warehouse - ware
    context = {
        'total':total
    }
    return render(request,'product/stock.html',context)


def create_warehouse_received(request):
    if request.user.is_warehouse is True:
        if request.method == 'POST':
            form = WarehouseReceivedForm(request.POST)
            if form.is_valid():
                received = form.save(commit=False)
                received.is_received = True
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
                received = form.save(commit=False)
                received.is_received = True
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


def to_supply(request):
    supplied = Order.objects.filter(is_paid=True,is_shipped=False)
    context = {
        'supply':supplied
    }
    return render(request,'product/not_supplied.html',context)


def approve_supplied(request,pk):
    approved = Order.objects.get(pk=pk)
    approved.is_supplied = True
    approved.save()
    return redirect('supplied')


def not_supplied(request,pk):
    approved = Order.objects.get(pk=pk)
    approved.is_supplied = False
    approved.save()
    return redirect('supplied')


def delete_received(request,pk):
    to_delete = WarehouseReceivedForm.objects.get(pk=pk)
    to_delete.delete()
    return redirect('all_received')


def delete_supplied(request,pk):
    to_delete = WarehouseSuppliedForm.objects.get(pk=pk)
    to_delete.delete()
    return redirect('all_supplied')


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


def all_received(request):
    received = WarehouseItem.objects.filter(is_received=True,user=request.user).order_by('date')
    context = {
        'received':received
    }
    return render(request,'product/all_received.html',context)


def all_supplied(request):
    supplied = Order.objects.filter(is_shipped=True,user=request.user).order_by('order_date')
    context = {
        'supplied':supplied
    }
    return render(request,'product/all_supplied.html',context)


def distributor_supplied(request):
    supplied = WarehouseItem.objects.filter(is_supplied=True, user=request.user).order_by('date')
    context = {
        'supplied': supplied
    }
    return render(request, 'product/all_supplied.html', context)


def create_sales(request):
    if request.method == 'POST':
        form = SalesForm(request.POST)
        if form.is_valid():
            sales = form.save(commit=False)
            sales.sold_by = request.user
            sales.save()
            supplied = WarehouseItem.objects.create(supplied=sales.quantity, product=sales.product,user=request.user,
                                                    is_supplied=True)
            supplied.save()
            return redirect('all_sales')
    else:
        form = SalesForm()

    context = {
        'form':form
    }
    return render(request,'product/create_sales.html',context)


def all_sales(request):
    sales = Sales.objects.filter(sold_by = request.user).order_by('-date')
    context = {
        'sales':sales
    }
    return render(request,'product/all_sales.html',context)


def my_customers(request):
    customers = Sales.objects.filter(sold_by=request.user)
    context = {
        'customers': customers
    }
    return render(request, 'product/customers.html', context)


def success(request):
    return render(request, 'product/success.html', {})


def failed(request):
    return render(request, 'product/failed.html', {})


def stock_warehouse(request):
    return render(request, 'product/stock_warehouse.html', {})