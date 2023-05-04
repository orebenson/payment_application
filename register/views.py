from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import RegisterUserForm, RegisterAdminForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth.models import User

@requires_csrf_token
def register_admin(request): # Register a new admin account with relevant details
    form = RegisterAdminForm()
    if not request.user.is_superuser:
        return redirect('login')
    if request.method == 'POST':
        form = RegisterAdminForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Admin account created')
        else:
            messages.error(request, 'Form invalid')
    return render(request, 'register/registeradmin.html', {'register_form': form})

@requires_csrf_token
def register_user(request): # Register a new user with relevant details
    form = RegisterUserForm()
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created')
            return redirect('login')
        messages.error(request, 'Form invalid')
    return render(request, 'register/register.html', {'register_form': form})

@requires_csrf_token
def login_user(request): # Login a user/admin, if user exists
    form = AuthenticationForm()
    if request.method == 'POST':
        print(request.POST)
        form = AuthenticationForm(request, request.POST)
        print(form.data)
        if form.is_valid():
            user = authenticate(request, username=form.data['username'], password=form.data['password'])
            print(user)
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid login')
    return render(request, 'register/login.html', {'form': form})

def logout_user(request): # Logout a user/admin
    logout(request)
    messages.success(request, 'Logout successful')
    return redirect('login')



