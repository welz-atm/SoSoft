from django.shortcuts import render,redirect
from .models import Order,OrderItem
from authenticate.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .celery_task import send_mail_rfq


@login_required()
def all_orders(request):
    orders = Order.objects.all().order_by('-order_date')
    context = {
        'orders':orders
    }
    return render(request,'product/all_orders.html',context)


@login_required()
def pending_order(request):
    pending = Order.objects.filter(user=request.user).order_by('-order_date')
    context = {
        'pending':pending
    }
    return render(request,'product/pending_orders.html',context)


@login_required()
def delete_order(request ,pk):
    to_delete = Order.objects.get(pk=pk)
    to_delete.delete()
    return redirect ('all_orders')


def view_order(request,pk):
    view = Order.objects.get(pk=pk)
    context = {
        'view': view
    }
    return render(request,'product/view_order.html',context)


@login_required()
def my_orders(request):
    sales = SalesDept.objects.get(user=request.user)
    orders = Order.objects.filter(order_by=sales,ordered=True).order_by('order_date')
    context = {
        'orders': orders
    }
    return render(request,'product/my_orders.html',context)


@login_required()
def add_cart(request):
    sales = SalesDept.objects.get(user=request.user)
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.order_by = sales
            order_item.save()
            orders = Order.objects.filter(order_by=sales)
            if orders.exists():
                order = orders[0]
                if order.order.filter(product=order_item.product).exists():
                    order_item.quantity += 1
                    order_item.save()
                    return redirect('order_summary')
                else:
                    order.order.add(order_item)
                    return redirect('order_summary')
            else:
                order = Order.objects.create(order_by=sales)
                order.order.add(order_item)
                messages.info(request, "Product Added")
                return redirect("order_summary")
    else:
        form = OrderItemForm()
    context = {
        'form': form
    }
    return render(request,'product/create_order.html',context)


@login_required()
def add_cart_sales(request,pk):
    distributor = CustomUser.objects.get(pk=pk)
    if request.method == 'POST':
        form = DistributorOrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.order_by = request.user
            order_item.user = distributor
            order_item.save()
            orders = Order.objects.filter(user=request.user)
            if orders.exists():
                order = orders[0]
                if order.order.filter(product=order_item.product).exists():
                    order_item.quantity += 1
                    order_item.save()
                    return redirect('order_summary')
                else:
                    order.order.add(order_item)
                    return redirect('order_summary')
            else:
                order = Order.objects.create(user=request.user)
                order.order.add(order_item)
                messages.info(request, "Product Added")
                return redirect("order_summary")
    else:
        form = DistributorOrderItemForm()
    context = {
        'form': form
    }
    return render(request,'product/create_order.html',context)


@login_required()
def remove_from_cart(request,pk):
    ordered_item = OrderItem.objects.get(pk=pk)
    ordered_item.delete()
    return redirect('my_cart')


@login_required()
def update_cart(request,pk):
    order = OrderItem.objects.get(pk=pk)
    if request.method == 'POST':
        form = UpdateItemForm(request.POST,instance=order)
        if form.is_valid():
            c = form.save(commit=False)
            c.user = request.user
            c.save()
            return redirect('order_summary')
    else:
        form = UpdateItemForm(instance=order)
    context = {
        'form': form,
        'order':order
    }
    return render(request,'product/update_cart.html',context)


@login_required()
def checkout(request):
    return render(request,'product/checkout.html',{})


@login_required()
def order_summary(request):
    sales = SalesDept.objects.get(user=request.user)
    orders = Order.objects.get(order_by = sales)

    context = {
        'orders':orders
    }
    return render(request,'product/order_summary.html',context)


@login_required()
def select_payment(request,pk):
    sales = SalesDept.objects.get(user=request.user)
    order = Order.objects.get(pk=pk)
    if request.method == 'POST':
        form = SelectPaymentForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            order_item = order.order.all()
            order.order.update(ordered=True)
            for item in order_item:
                item.save()
            order.ordered = True
            order.save()
            return redirect('all_orders')
    else:
        form = SelectPaymentForm()
    context = {
        'form':form
    }
    return render(request,'product/select_payment.html',context)
