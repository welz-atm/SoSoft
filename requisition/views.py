from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .models import Quotation,Requisition,Expense
from django.contrib.auth.decorators import login_required

@login_required()
def create_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('my_expenses')
    else:
        form = ExpenseForm()
    context = {
        'form':form
    }
    return render(request,'product/create_expense.html',context)


@login_required()
def approve_expense(request,pk):
    expense = Expense.objects.get(pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST,instance=expense)
        approval_form = ApprovalForm(request.POST)
        comment_form = CommentForm(request.POST)
        if form.is_valid() and approval_form.is_valid() and comment_form.is_vaild():
            expense_form = form.save(commit=False)
            approval = approval_form.save(commit=False)
            comment = comment_form.save(commit=False)
            approval.approver = request.user
            approval.save()
            comment.user = request.user
            comment.save
            expense_form.approval = approval
            expense_form.comment = comment
            expense_form.save()
            return redirect('all_expenses')
    else:
        form = ExpenseForm()
        approval_form = ApprovalForm()
        comment_form = CommentForm()
    context = {
        'form':form,
        'approval_form':approval_form,
        'comment_form':comment_form
    }
    return render(request,'product/approve_expense.html',context)


@login_required()
def edit_expense(request,pk):
    expense = Expense.objects.get(pk=pk)
    if expense.approval == 'Awaiting Approval' or 'Disapproved':
        if request.method == 'POST':
            form = ExpenseForm(request.POST,instance=expense)
            if form.is_valid():
                expenses = form.save(commit=False)
                expenses.user = request.user
                expenses.save()
                return redirect('my_expenses')
        else:
            form = ExpenseForm()
        context = {
            'form':form
        }
        return render(request,'product/edit_expense.html',context)
    else:
        return HttpResponse('Expense has been approved and cannot be edited')


@login_required()
def create_req(request):
    if request.method == 'POST':
        form = RequisitionForm(request.POST,request.FILES)
        if form.is_valid():
            req = form.save(commit=False)
            req.user = request.user
            req.save()
            return redirect('all_requisitions')
    else:
        form = RequisitionForm()
    context = {
        'form': form
    }

    return render(request,'product/create_req.html',context)


@login_required()
def edit_req(request,pk):
    req = Requisition.objects.get(pk=pk)
    if req.is_approved is True:
        if request.method == 'POST':
            form = RequisitionForm(request.POST,request.FILES,instance=req)
            if form.is_valid():
                req_form = form.save(commit=False)
                req_form.user = request.user
                req_form.save()
                return redirect('all_requisitions')
        else:
            form = RequisitionForm(instance=req)

        context = {
            'form': form
        }
        return render(request,'product/edit_req.html',context)
    else:
        return HttpResponse('This req has been approved and cannot be edited')


@login_required()
def view_req(request,pk):
    req = get_object_or_404(Requisition,pk=pk)
    context = {
        'req':req
    }
    return render(request,'product/view_req.html',context)


@login_required()
def all_req(request):
    reqs = Requisition.objects.all().order_by('-req_date')
    context = {
        'reqs':reqs
    }
    return render(request,'product/all_reqs.html',context)


@login_required()
def my_reqs(request):
    reqs = Requisition.objects.filter(user=request.user).order_by('-req_date').select_related('user')
    context = {
        'reqs': reqs
    }
    return render(request,'product/my_reqs.html',context)


@login_required()
def approve_req(request,pk):
    req = Requisition.objects.get(pk=pk)
    if request.method == 'POST':
        form = RequisitionForm(request.POST,instance=req)
        approval_form = ApprovalForm(request.POST)
        if form.is_valid() and approval_form.is_valid():
            req = form.save(commit=False)
            req.user = request.user
            approval = approval_form.save(commit=False)
            approval.approver = req.user
            req.approval = approval.status
            if req.approval == 'Approved':
                req.is_approved = True
                req.save()
                approval.save()
                return redirect('all_reqs')
            else:
                req.save()
                approval.save()
                return redirect('all_reqs')
    else:
        form = RequisitionForm(instance=req)
        approval_form = ApprovalForm()
    context = {
        'req': req,
        'form': form,
        'approval_form': approval_form
    }
    return render(request,'product/approve_req.html',context)


@login_required()
def approved_reqs(request):
    reqs = Requisition.objects.filter(is_approved=True).orderby_date.select_related('approval','supplier','user')
    context = {
        'reqs':reqs
    }
    return render(request,'product/approved_reqs.html',context)


@login_required()
def request_for_quote(request,pk):
    req = Requisition.objects.get(pk=pk)
    if req.is_approved is True:
        req.is_rfq = True
        req.save()
        send_mail_rfq.delay(req.pk)
        return render('all_req')
    else:
        return HttpResponse('You cannot send RFQ as req has not been approved')


@login_required()
def all_rfqs(request):
    rfqs = Requisition.objects.filter(is_rfq=True)
    context = {
        'rfqs':rfqs
    }
    return render(request,'product/all_rfqs.html',context)


@login_required()
def my_rfqs(request):
    supplier = Supplier.objects.get(user=request.user)
    rfqs = Requisition.objects.filter(is_rfq=True,category=supplier.category).order_by('-date').select_related('approval','supplier','user')
    context = {
        'rfqs': rfqs
    }
    return render(request,'product/my_rfqs.html',context)


@login_required()
def create_quotation(request,pk):
    req = Requisition.objects.get(pk=pk)
    user = Supplier.objects.get(user=request.user)
    if request.method == 'POST':
        form = QuotationForm(request.POST,request.FILES)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.user = user
            quote.is_quoted = True
            quote.requisition = req
            quote.save()
            return redirect('my_quotations')
    else:
        form = QuotationForm()
    context = {
        'form':form,
        'req':req
    }
    return render(request,'product/quotation_page.html',context)


@login_required()
def my_quotations(request):
    user = Supplier.objects.get(user=request.user)
    quotations = Quotation.objects.filter(user=user,requisition__category=user.category).order_by('-date').select_related('requisition')
    context = {
        'quotations':quotations
    }
    return render(request,'product/my_quotations.html',context)


@login_required()
def edit_quote(request,pk):
    quote = Quotation.objects.get(pk=pk)
    if quote.requisition.is_approved is True:
        return HttpResponse('You cannot edit this quote.It has been approved')
    else:
        if request.method == 'POST':
            form = QuotationForm(request.POST,instance=quote)
            if form.is_valid():
                quotes = form.save(commit=False)
                quotes.user = request.user
                quotes.save()
                return redirect('my_quotations')
        else:
            form = QuotationForm(instance=quote)
        context= {
            'form':form
            }
        return render(request,'product/edit_quotation.html',context)


@login_required()
def view_quote(request,pk):
    req = Requisition.objects.get(pk=pk)
    quote = Quotation.objects.get(requisition=req)
    context = {
        'quotes':quote
    }
    return render(request,'product/view_quote.html',context)


@login_required()
def compare_quote(request,pk):
    req = Requisition.objects.get(pk=pk)
    quotes = Quotation.objects.filter(requisition__req_item_name=req.req_item_name)
    context = {
        'quotes':quotes
    }
    return render(request,'product/compare_quote.html',context)


@login_required()
def raise_purchase_order(request,pk):
    quote = Quotation.objects.get(pk=pk)
    user = PurchaseDept.objects.get(user=request.user)
    if request.user == user:
        purchase = PurchaseOrder.objects.create(quotation=quote,user=user,is_requested=True)
        purchase.save()
        # messages.info('You have raised a Purchase Order for Quote {}'.format(quote.nos))
    else:
        return HttpResponse('You do not have access to do this')


@login_required()
def all_purchase_orders(request):
    purchase_orders = PurchaseOrder.objects.all().order_by('-date').select_related('user','quotation')
    context = {
        'purchase_orders': purchase_orders
    }
    return render(request,'product/all_purchase_orders.html',context)


def preview_purchase_order(request,pk):
    quote = Quotation.objects.get(pk=pk)
    user = PurchaseDept.objects.get(user=request.user)
    if request.user == user:
        purchase = PurchaseOrder.objects.create(quotation=quote, user=user, is_requested=True)
        purchase.save()
        context={
            'purchase':purchase
        }
        return render_to_string('purchase_order.html',context)
    else:
        return HttpResponse('You do not have access to do this')
