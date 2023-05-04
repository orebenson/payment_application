from django.shortcuts import render, redirect
from .forms import MakePaymentForm, MakePaymentRequestForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Cash, CashRequests, CashTransfers
from django.db import transaction
from django.views.decorators.csrf import requires_csrf_token

# Create your views here.
def home(request):
    balances = []
    if request.user.is_superuser:
        balances = list(Cash.objects.all())
    else:
        balances = list(Cash.objects.filter(user=request.user))
    return render(request, "payapp/home.html", {'balances': balances})

def transactions(request):
    transactions = []
    if request.user.is_superuser:
        transactions = list(CashTransfers.objects.all())
    else:
        transactions = list(CashTransfers.objects.filter(user=request.user))
    return render(request, "payapp/transactions.html", {'transactions': transactions})

    return render(request, "payapp/transactions.html")
    # view all transactions received and sent
    # if user is admin, view all transactions from every user

@requires_csrf_token
def makepayment(request):
    # send money to another user
    form = MakePaymentForm()
    if request.method == 'POST':
        form = MakePaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            src_user = request.user
            dst_user = User.objects.get(username=form.cleaned_data['other_user'])

            if dst_user: #check if destination user exists
                src_cash = Cash.objects.get(user=src_user)
                dst_cash = Cash.objects.get(user=dst_user)

                if src_cash.balance > amount: #check if user has sufficient funds
                    src_curr = src_cash.currency
                    dst_curr = dst_cash.currency

                    dst_amount = amount #* multiplied by conversion rate src > dst from RestAPI

                    with transaction.atomic(): # make transaction using atomic to remove amount from sender and add to receiver in Cash models
                        src_cash.balance = src_cash.balance - amount #multiplied by conversion
                        src_cash.save()
                        dst_cash.balance = dst_cash.balance + dst_amount #multiplied by conversion
                        dst_cash.save()

                    src_transfers = CashTransfers(user=src_user, other_user=dst_user, amount=amount, direction='Sent to')
                    dst_transfers = CashTransfers(user=dst_user, other_user=src_user, amount=dst_amount, direction='Received from')
                    src_transfers.save()
                    dst_transfers.save()

                    messages.success(request, 'Payment complete')
                    form = MakePaymentForm()
                else:
                    messages.error(request, 'Insufficient funds')
            else:
                messages.error(request, 'User invalid')
        else:
            messages.error(request, 'Form invalid')
    return render(request, "payapp/makepayment.html", {'payment_form': form})

def requests(request):
    # view all payment requests
    # accept/reject payment requests
    # when accepted, do transaction
    # when rejected, delete request
    # if user is admin, view all requests
    return render(request, "payapp/requests.html")

def request(request):
    # make a payment request to a user
    # add request to receiver in CashRequests model
    return render(request, "payapp/request.html")

