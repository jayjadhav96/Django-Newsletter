from django import forms
from .models import NewletterUser
from django.core.exceptions import ValidationError

class SubscribeModelForm(forms.ModelForm):
    email = forms.EmailField(label='')
    class Meta:
        model = NewletterUser
        fields = ['email']

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        qs = NewletterUser.objects.filter(email__iexact=email)
        if qs.exists():
            raise ValidationError("This email already exists")
        return email

class UnsubscribeModelForm(forms.ModelForm):
    email = forms.EmailField(label='')
    class Meta:
        model = NewletterUser
        fields = ['email']

