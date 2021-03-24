from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required

from .models import NewletterUser

from .forms import SubscribeModelForm, UnsubscribeModelForm
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string


# Create your views here.
# def subscribe(request):
#     form = SubscribeModelForm
#     if request.method == 'POST':
#         form = SubscribeModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/')
#         else:
#             form = SubscribeModelForm
#     return render(request, 'letterapp/subscribe.html', {'form': form})


class SubscribeView(SuccessMessageMixin, CreateView):
    form_class = SubscribeModelForm
    template_name = 'letterapp/subscribe.html'
    success_url = '/'
    success_message = "Thank you for subscribing us."

    # def get_success_url(self):
    #     messages.success(self.request, 'Your Email unsubscribed successfully')

def unsubscribe(request, *args, **kwargs):
    form = UnsubscribeModelForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if NewletterUser.objects.filter(email=instance.email).exists():
            NewletterUser.objects.filter(email=instance.email).delete()
            form = UnsubscribeModelForm()
            messages.success(request, 'Your Email unsubscribed successfully')
        else:
            messages.warning(request, "Oops, We didn't find this email address")

    context = {
        'form': form,
    }

    return render(request, 'letterapp/unsubscribe.html', context)




# Sending Actual Email 
@login_required
def send_mail_view(request):

    emails =  NewletterUser.objects.all()
    
    if request.method == 'POST':
        message_email = 'hello' #request.POST['email'] 
        subject = request.POST['subject']
        message = request.POST['message']

        template = render_to_string('email_template.html', {'message': message}) 

        msg = EmailMessage(
            subject, # Subject
            template, # Body
            'B2C <jay.jadhav@somaiya.edu>', #From Email
            bcc=emails, # To Email in BCC
        )

        msg.content_subtype = "html"
        msg.fail_silently=False
        msg.send()
        return render(request, 'letterapp/sendmail.html')
    

    return render(request, 'letterapp/sendmail.html')