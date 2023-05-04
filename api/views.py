from django.http import JsonResponse, HttpResponse

def Conversion(request, curr1, curr2, amount): # return curr2 amount after conversion
    if curr1 not in {'GBP', 'USD', 'EUR'} or curr2 not in {'GBP', 'USD', 'EUR'}:
        return HttpResponse(status=400)
    else: # Match the relevant currency 1 and currency 2 and get exchange rate
        match curr1:
            case 'GBP':
                match curr2:
                    case 'USD': conversion = 1.26
                    case 'EUR': conversion = 1.14
                    case 'GBP': conversion = 1
            case 'USD':
                match curr2:
                    case 'GBP': conversion = 0.8
                    case 'EUR': conversion = 0.91
                    case 'USD': conversion = 1
            case 'EUR':
                match curr2:
                    case 'USD': conversion = 1.1
                    case 'GBP': conversion = 0.88
                    case 'EUR': conversion = 1
        dst_amount = amount * conversion
        return JsonResponse({
            'rate': conversion,
            'amount': dst_amount
                             })
