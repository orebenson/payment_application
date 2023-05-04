from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('makepayment/', views.makepayment, name='makepayment'),
    path('transactions/', views.transactions, name='transactions'),
    path('request/', views.request, name='request'),
    path('requests/', views.requests, name='requests'),
    path('requests/accept/<int:id>', views.accept, name='accept'),
    path('requests/reject/<int:id>', views.reject, name='reject'),
]
