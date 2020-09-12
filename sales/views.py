from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Sales


@login_required()
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


@login_required()
def all_sales(request):
    sales = Sales.objects.filter(sold_by = request.user).order_by('-date')
    context = {
        'sales':sales
    }
    return render(request,'product/all_sales.html',context)


@login_required()
def my_customers(request):
    customers = Sales.objects.filter(sold_by=request.user)
    context = {
        'customers': customers
    }
    return render(request, 'product/customers.html', context)