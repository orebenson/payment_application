from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from payapp.models import Cash

class RegisterUserForm(UserCreationForm):
    CURRENCIES = (
        ("1", "USD"),
        ("2", "GBP"),
        ("3", "EUR"),
    )
    email = forms.EmailField()
    currency = forms.ChoiceField(choices=CURRENCIES)
    balance = forms.IntegerField()

    class Meta:
        model = User
        fields = ["username", "currency", "email", "password1", "password2"]

    def save(self, *args, **kwargs):
        instance = super(RegisterUserForm, self).save(*args, **kwargs)
        currency = self.cleaned_data['currency']
        currency = dict(self.fields['currency'].choices)[currency]
        Cash.objects.create(user=instance, currency=currency, balance=self.balance)
        return instance

class RegisterAdminForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        # model.is_superuser = True
        fields = ["username", "email", "password1", "password2", "is_superuser"]

    def save(self, *args, **kwargs):
        instance = super(RegisterAdminForm, self).save(*args, **kwargs)
        # self.is_superuser = True
        return instance



