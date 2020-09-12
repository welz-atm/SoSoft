from django.shortcuts import render
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from authenticate.models import Department
from .models import Email,Task
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import poplib
from email import parser
from email.header import decode_header

@login_required()
def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST,request.FILES)
        if form.is_valid():
            mail = form.save(commit=False)
            mail.author = request.user
            mail.is_out = True
            mail.save()
            email = send_mail(mail.subject,mail.message,mail.from_email,[mail.to_email])
            email.content_subtype = 'html'
            if mail.attachment is not None:
                email.attach(mail.attachment.name,mail.attachment.read(), mail.attachment.content_type)
                email.send(fail_silently=False)
                return redirect('all_req')
            else:
                email.send(fail_silently=False)
                return redirect('all_req')
        else:
            form = EmailForm()
        context = {
            'form':form
        }
        return render(request,'product/create_email.html',context)


@login_required()
def incoming_email(request):
    department = Department.objects.get(user=request.user)
    if department.is_member is True:
        pop3 = poplib.POP3_SSL(department.username, department.password, department.server, str(department.port))
        messages = [pop3.retr(i) for i in range(1, len(pop3.list()[1]) + 1)]
        messages = ["\n".join(m[1]) for m in messages]
        messages = [parser.Parser().parsestr(m) for m in messages]
        for message in messages:
            mail_list = {}
            for item in message.items():
                mail_list['subject'] = item.Subject
                mail_list['from_email'] = item.From
                mail_list['to_email'] = item.To
                mail_list['message'] = item.Body

                for mail in mail_list():
                    email = Email.objects.create(to_email=mail.to_email,from_email=mail.from_email,
                                                 subject=mail.subject,message=mail.message,is_inc=True)
                    email.save()

            for part in message.walk():
                # find the attachment part - so skip all the other parts
                if part.get_content_maintype() == 'multipart': continue
                if part.get_content_maintype() == 'text': continue
                if part.get('Content-Disposition') == 'inline': continue
                if part.get('Content-Disposition') is None: continue

                # get filename
                filename = part.get_filename()
                filenames_list = []
                # this is for encoding other than latin-letter-languages
                if decode_header(filename)[0][1] is not None:
                    filename = str(decode_header(filename[0][0]).decode(decode_header(filename)[0][1]))
                    filenames_list.append(filename)
                    mail_list['attachment'] = filenames_list
                    for mail in mail_list():
                        email.attachment = mail.attachment
                        email.save()

        email_list = Email.objects.filter(to_email__is_member=True,is_inc=True).order_by('-date').select_related('department','author')

        context = {
            'mail_list':mail_list,
            'email_list':email_list,
                }
        return render(request,'product/incoming_email.html',context)
    else:
        return HttpResponse('You are not a member of this department. Kindly contact Administrator')


@login_required()
def outgoing_email(request):
    dept = Department.objects.get(user=request.user)
    out_email = Email.objects.filter(is_out=True,from_email=dept.username).order_by('-time_sent').\
                                     select_related('department','author')
    context = {
        'out_email':out_email
    }
    return render(request,'product/outgoing_emails.html',context)


@login_required()
def view_email(request,pk):
    email = Email.objects.get(pk=pk)
    form = EmailForm(instance=email)
    context = {
        'form': form
    }
    return render(request,'product/view_email.html',context)


@login_required()
def create_task_from_email(request,pk):
    email = Email.objects.get(pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.email = email
            task.save()
            form = EmailForm(instance=email)
            context = {'form':form}
            return render(request,'product/view_email.html',context)
    else:
        form = TaskForm()
    context = {
        'form':form
    }
    return render(request,'product/create_task',context)


@login_required()
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        comment = CommentForm(request.POST)
        if form.is_valid() and comment.is_valid():
            task = form.save(commit=False)
            comment = comment.save(commit=False)
            comment.user = request.user
            task.user = request.user
            comment.save()
            task.comment.add(comment)
            task.save()
            return redirect('incoming_emails')
    else:
        form = TaskForm()
    context = {
        'form':form
    }
    return render(request,'product/cr+eate_task',context)


@login_required()
def view_task(request,pk):
    task = Task.objects.get(pk=pk).select_related('email')
    context = {
        'task': task
    }
    return render(request,'product/view_task.html',context)


@login_required()
def my_task(request):
    tasks = Task.objects.filter(user=request.user).select_related('email')
    context = {
        'tasks': tasks
    }
    return render(request,'product/my_task.html',context)


@login_required()
def all_tasks(request):
    tasks = Task.objects.all().order_by('-date').select_related('user','email')
    context = {
        'tasks':tasks
    }
    return render(request,'product/all_tasks.html',context)


@login_required()
def edit_task(request,pk):
    edit = Task.objects.get(pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST,instance=edit)
        comment = CommentForm(request.POST)
        if form.is_valid() and comment.is_valid():
            task = form.save(commit=False)
            com = comment.save(commit=False)
            task.comment = com
            com.user = request.user
            com.save()
            task.user=request.user
            task.save()
            return redirect('all_tasks')
    else:
        form = TaskForm(instance=edit)
    context = {
        'form': form
    }
    return render(request,'product/edit_task.html',context)
