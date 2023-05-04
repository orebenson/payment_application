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
    # view all transactions received and sent
    # if user is admin, view all transactions from every user
    transactions = []
    if request.user.is_superuser:
        transactions = list(CashTransfers.objects.all())
    else:
        transactions = list(CashTransfers.objects.filter(user=request.user))
    return render(request, "payapp/transactions.html", {'transactions': transactions})


@requires_csrf_token
def makepayment(request):
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

                    # Get conversion rate from RestAPI
                    # conversion = get_conversion(src_curr, dst_curr)

                    dst_amount = amount #* conversion

                    with transaction.atomic(): # make transaction using atomic to remove amount from sender and add to receiver in Cash models
                        src_cash.balance = src_cash.balance - amount
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
@requires_csrf_token
def requests(request):
    if request.method == 'GET':
        requests = []
        if request.user.is_superuser:
            requests = list(CashRequests.objects.all())
        else:
            requests = list(CashRequests.objects.filter(user=request.user))
    return render(request, "payapp/requests.html", {'requests': requests})

@requires_csrf_token
def accept(request, id):
    # accept request containing the request id and do transaction
    src_user = request.user
    dst_user = CashRequests.objects.get(id=id).other_user
    amount = CashRequests.objects.get(id=id).amount

    src_cash = Cash.objects.get(user=src_user)
    dst_cash = Cash.objects.get(user=dst_user)

    if src_cash.balance > amount: #check if user has sufficient funds
        src_curr = src_cash.currency
        dst_curr = dst_cash.currency

        # Get conversion rate from RestAPI
        # conversion = get_conversion(src_curr, dst_curr)

        dst_amount = amount #* conversion

        with transaction.atomic(): # make transaction using atomic to remove amount from sender and add to receiver in Cash models
            src_cash.balance = src_cash.balance - amount
            src_cash.save()
            dst_cash.balance = dst_cash.balance + dst_amount #multiplied by conversion
            dst_cash.save()

        src_transfers = CashTransfers(user=src_user, other_user=dst_user, amount=amount, direction='Sent to')
        dst_transfers = CashTransfers(user=dst_user, other_user=src_user, amount=dst_amount, direction='Received from')
        src_transfers.save()
        dst_transfers.save()

        CashRequests.objects.filter(id=id).delete()

        messages.success(request, 'Request accepted, payment complete')
    else:
        messages.error(request, 'Insufficient funds')
    return redirect('requests')

@requires_csrf_token
def reject(request, id):
    # delete request containing the request id
    CashRequests.objects.filter(id=id).delete()
    messages.success(request, 'Request rejected')
    return redirect('requests')
@requires_csrf_token
def request(request):
    form = MakePaymentRequestForm()
    if request.method == 'POST':
        form = MakePaymentRequestForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            src_user = request.user
            dst_user = User.objects.get(username=form.cleaned_data['other_user'])
            if dst_user: #check if destination user exists
                src_cash = Cash.objects.get(user=src_user)
                dst_cash = Cash.objects.get(user=dst_user)

                src_curr = src_cash.currency
                dst_curr = dst_cash.currency

                # Get conversion rate from RestAPI
                # conversion = get_conversion(src_curr, dst_curr)

                dst_amount = amount #* conversion

                dst_requests = CashRequests(user=dst_user, amount=dst_amount, other_user=src_user)
                dst_requests.save()

                messages.success(request, 'Request sent')
                form = MakePaymentRequestForm()

            else:
                messages.error(request, 'User invalid')
        else:
            messages.error(request, 'Form invalid')

    return render(request, "payapp/request.html", {'request_form': form})

