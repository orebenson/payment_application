from urllib.request import urlopen
import json

def get_conversion(curr1, curr2, amount):# Send conversion get request to api/conversion/{currency1}/{currency2}/{amount_of_currency1}
    URL = f"http://127.0.0.1:8000/api/conversion/{curr1}/{curr2}/{amount}"
    response = urlopen(URL)
    data = response.read()
    curr2 = json.loads(data)['amount'] # return curr2 amount
    return curr2