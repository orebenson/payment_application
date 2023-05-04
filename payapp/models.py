
from django.db import models
from django.contrib.auth.models import User

class Cash(models.Model): # Model that stores all user balances and chosen currencies
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=5)
    balance = models.IntegerField()

    def __str__(self):
        details = ''
        details += f'User : {self.user}\n'
        details += f'Currency : {self.currency}\n'
        details += f'Balance : {self.balance}\n'
        return details

class CashTransfers(models.Model): # Model that stores all user transfers
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transfers_users')
    other_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='transfers_other_users')
    amount = models.IntegerField()
    time = models.DateTimeField(auto_now=True)
    direction = models.CharField(max_length=15)

    def __str__(self):
        details = ''
        details += f'Amount : {self.amount}\n'
        details += f'Direction : {self.direction}\n'
        details += f'User : {self.other_user}\n'
        return details


class CashRequests(models.Model): # Model that stores all user cash requests
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests_users')
    amount = models.IntegerField()
    other_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='requests_other_users')
    def __str__(self):
        details = ''
        details += f'Amount : {self.amount}\n'
        details += f'Requested by : '
        details += f'User : {self.other_user}\n'
        return details