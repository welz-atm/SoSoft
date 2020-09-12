from django.shortcuts import render
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .models import Skill,Education,Experience,Candidate,Leave,Document
from authenticate.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required()
def submit_credentials(request):
    if request.method == 'POST':
        candidate_form = CandidateForm(request.POST)
        skill_form = SkillForm(request.POST)
        experience_form = ExperienceForm(request.POST)
        education_form = EducationForm(request.POST)
        if candidate_form.is_valid() and skill_form.is_valid() and experience_form.is_valid() and education_form.is_valid():
            candidate = candidate_form.save(commit=False)
            skill_form.save()
            experience_form.save()
            education_form.save()
            candidate.experience.add(experience_form)
            candidate.education.add(education_form)
            candidate.skill.add(skill_form)
            candidate.save()
            return redirect('thank_you.html')
    else:
        candidate_form = CandidateForm()
        skill_form = SkillForm()
        experience_form = ExperienceForm()
        education_form = EducationForm()
    context = {
        'candidate_form': candidate_form,
        'skill_form': skill_form,
        'experience_form': experience_form,
        'education_form': education_form
    }
    return render(request,'submit_credential.html',context)


@login_required()
def all_candidates(request):
    candidates = Candidate.objects.all()
    context = {
        'candidates': candidates
    }
    return render(request,'all_candidates.html',context)


@login_required()
def post_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST,request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.user = request.user
            doc.save()
            return redirect('all_docs')
    else:
        form = DocumentForm()
    context = {
        'form': form
    }
    return render(request,'product/post_doc.html',context)


@login_required()
def all_documents(request):
    all_docs = Document.objects.all().order_by('-date_created').select_related('user')
    context = {
        'all_docs': all_docs
    }
    return render(request,'product/all_docs.html',context)


@login_required()
def my_documents(request):
    my_docs = Document.objects.filter(can_access=request.user,user=request.user).order_by('-date_created').select_related('user')
    context = {
        'my_docs':my_docs
    }
    return render(request,'product/my_docs.html',context)


@login_required()
def request_for_leave(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            if leave.start_date > leave.end_date:
                messages.success(request,'The start date should be lower than end date')
            elif leave.end_date < leave.start_date:
                messages.warning(request,'The end_date should be greater than start_date')
            else:
                leave.user = request.user
                leave.save()
                return redirect('home')
    else:
        form = LeaveForm()
    context = {
        'form':form
    }
    return render(request,'product/request_4_leave.html',context)


@login_required()
def approve_leave(request,pk):
    leave = Leave.objects.get(pk=pk)
    if request.method == 'POST':
        form = LeaveForm(request.POST,instance=leave)
        approval_form = ApprovalForm(request.POST)
        if form.is_valid() and approval_form.is_valid():
            leave_form = form.save(commit=False)
            approve = approval_form.save(commit=False)
            approve.approver = request.user
            approve.save()
            leave_form.approval = approve
            leave_form.save()
            return redirect('all_leave')
    else:
        form = LeaveForm()
        approval_form = ApprovalForm()
    context = {
        'form':form,
        'approval_form':approval_form
    }
    return render(request,'product/request_4_leave.html',context)