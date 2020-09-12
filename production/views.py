from django.shortcuts import render,redirect
from .models import Production,BillOfMaterial
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required()
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


@login_required()
def edit_production(request):
    if request.method == 'POST':
        form = EditProductionForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'Saved successfully')
            return redirect('all_production')
    else:
        form = EditProductionForm(instance=request.user)
    context = {
        'form':form
    }
    return render(request,'product/edit_production.html',context)


@login_required()
def all_production(request):
    production = Production.objects.all().order_by('-date')
    context = {
        'production':production
    }
    return render(request,'product/all_production.html',context)


def delete_production(request,pk):
    product = Production.objects.get(pk=pk)
    product.delete()
    return redirect('all_production')


@login_required()
def create_bom(request):
    purchase = PurchaseDept.objects.get(user=request.user)
    if request.method == 'POST':
        form = BillOfMaterialForm(request.POST)
        if form.is_valid():
            bom = form.save(commit=False)
            bom.user = purchase
            bom.save()
            return redirect('all_bom')
    else:
        form= BillOfMaterialForm()
    context = {
        'form': form
    }
    return redirect(request,'product/create_bom.html',context)


@login_required()
def add_material(request,pk):
    bill = BillOfMaterial.objects.get(pk=pk)
    if request.method == 'POST':
        form = BomMaterialForm(request.POST)
        if form.is_valid():
            bills = form.save(commit=False)
            bills.save()
            bill.material.add(form)
            bill.save()
            return redirect('bom_page')
    else:
        form = BomMaterialForm()
    context = {
        'form':form
    }
    return render(request,'add_material.html',context)


@login_required()
def view_bom(request,pk):
    bom = BillOfMaterial.objects.get(pk=pk)
    context = {
        'bom':bom
    }
    return render(request,'product/view_bom.html',context)


@login_required()
def bom_draft(request,pk):
    draft = BillOfMaterial.objects.get(pk=pk)
    draft.is_draft = True
    draft.save()
    return redirect('all_boms')