from django import forms

class MakePaymentForm(forms.Form): # Form for making direct payments to another user
    other_user = forms.CharField(label="Transfer to user: ", max_length=100)
    amount = forms.IntegerField(label="Amount: ")

class MakePaymentRequestForm(forms.Form): # Form for making payment requests to another user
    other_user = forms.CharField(label="Request from user: ", max_length=100)
    amount = forms.IntegerField(label="Amount: ")

