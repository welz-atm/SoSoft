from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .forms import ProductForm,OrderItemForm,CreateApprovalForm,ApprovalForm,ProductionForm,EditProductionForm,\
                   WarehouseCreateForm,WarehouseSuppliedForm,WarehouseReceivedForm,SalesForm,UpdateItemForm,\
                   OrderItemForm,ItemForm,WarehouseCompanyForm,SelectPaymentForm,DistributorOrderItemForm,\
                   RequisitionForm,QuotationForm,EmailForm,TaskForm,BillOfMaterialForm,BomMaterialForm,CommentForm,\
                   DocumentForm,SkillForm,EducationForm,ExperienceForm,CandidateForm,LeaveForm,ExpenseForm
from .models import Product,Order,Approval,OrderItem,Production,Warehouse,WarehouseItem,Sales,Payment,Item,SalesDept,\
                    Requisition,Email,Task,Quotation,PurchaseOrder,BomMaterial,BillOfMaterial,Document,Skill,Education,\
                    Experience,Candidate,Leave,Expense
from authenticate.models import CustomUser,Supplier,Department,PurchaseDept
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import poplib
from email import parser
from email.header import decode_header
from .celery_task import send_mail_rfq
from django.template.loader import render_to_string
from paystackapi.transaction import Transaction


@login_required()
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
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
def edit_product(request, pk):
    edit = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST , instance=edit)
        if form.is_valid():
            form.save()
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
def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('all_items')
    else:
        form = ItemForm(request.POST)
    context = {
        'form': form
    }
    return render(request,'product/create_item.html',context)


@login_required()
def all_items(request):
    items = Item.objects.all()
    context = {
        'items': items
    }
    return render(request,'product/all_items.html',context)


@login_required()
def edit_item(request, pk):
    edit = Item.objects.get(pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST , instance=edit)
        if form.is_valid():
            form.save()
            return redirect('all_items')
    else:
        form = ItemForm(instance=edit)
    context = {
        'form': form
    }
    return render(request,'product/edit_item.html',context)


@login_required()
def delete_item(request,pk):
    to_delete = Item.objects.get(pk=pk)
    to_delete.delete()
    return redirect ('all_requisite_items')


@login_required()
def create_approval(request):
    if request.method == 'POST':
        form = CreateApprovalForm(request.POST)
        if form.is_valid():
            form.save()
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
def charge_payment(request,pk):
    order = Order.objects.get(pk=pk)
    response = Transaction.initialize(amount=order.final_price()*100,email=request.user.email,
                                      callback_url='http://127.0.0.1:8000/product/success/')
    go = response['data']
    url = go['authorization_url']
    reference = go['reference']
    payment = Payment.objects.create(order=order,reference=reference,user=request.user,amount=order.final_price())
    payment.save()
    return redirect(url)


@login_required()
def success(request):
    payments = Payment.objects.filter(user=request.user).order_by('date')
    context = {
        'payments': payments
    }
    return render(request, 'product/success.html', context)


@login_required()
def failed(request):
    return render(request, 'product/failed.html', {})






def chat(request):
    return render(request,'product/chat.html',{})