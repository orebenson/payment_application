from django import forms

class MakePaymentForm(forms.Form):
    other_user = forms.CharField(label="Transfer to user: ", max_length=100)
    amount = forms.IntegerField(label="Amount: ")

class MakePaymentRequestForm(forms.Form):
    other_user = forms.CharField(label="Request from user: ", max_length=100)
    amount = forms.IntegerField(label="Amount: ")

