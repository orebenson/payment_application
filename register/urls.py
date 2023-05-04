from django.urls import include, path
from . import views


urlpatterns = [
    path('user/', views.register_user, name='register user'),
    path('admin/', views.register_admin, name='register admin'),
]