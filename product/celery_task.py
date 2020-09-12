from celery.task import task
from django.core.mail import EmailMessage
from django.shortcuts import reverse
from django.template.loader import render_to_string
from .models import Requisition
from authenticate.models import Supplier


@task
def send_mail_rfq(req_id):
    req = Requisition.objects.get(pk=req_id)
    users = Supplier.objects.filter(category=req.category)
    url = 'http://localhost:8000/' + reverse("reqs:reqs")
    context = {
        'url':url
    }
#   user = list(users)
    for user in users:
        subject = 'Request For Quote'
        body = render_to_string('req_email_template.html',context)
        recipient = user.email
        msg = EmailMessage(
            subject=subject, body=body, to=recipient
        )
        msg.content_subtype = "html"
        msg.send()