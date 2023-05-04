from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from payapp.models import Cash
from common.convert import get_conversion

class RegisterUserForm(UserCreationForm): # Form for registering a user, including a chosen currency
    CURRENCIES = (
        ("1", "USD"),
        ("2", "GBP"),
        ("3", "EUR"),
    )
    email = forms.EmailField()
    currency = forms.ChoiceField(choices=CURRENCIES)

    class Meta:
        model = User
        fields = ["username", "currency", "email", "password1", "password2"]

    def save(self, *args, **kwargs):
        instance = super(RegisterUserForm, self).save(*args, **kwargs)
        currency = self.cleaned_data['currency']
        currency = dict(self.fields['currency'].choices)[currency]
        # Get conversion rate from RestAPI
        balance = get_conversion('GBP', currency, 1000)
        Cash.objects.create(user=instance, currency=currency, balance=balance)
        return instance

class RegisterAdminForm(UserCreationForm): # Form for registering a new admin
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "is_superuser"]

    def save(self, *args, **kwargs):
        instance = super(RegisterAdminForm, self).save(*args, **kwargs)
        # self.is_superuser = True
        return instance



