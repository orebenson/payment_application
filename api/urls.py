from django.urls import path
from . import views

# Match get url currencies and amount
urlpatterns = [
    path('conversion/<slug:curr1>/<slug:curr2>/<int:amount>/', views.Conversion, name='conversion')
]
