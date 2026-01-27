from django.shortcuts import render, redirect
from django.core.validators import validate_email, ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.db import IntegrityError
from .models import CustomUser

# Create your views here.

def login_request(request):
    return render(request, 'authentication/login.html', {})


def register_request(request):
    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

    
        if not username:
            errors['username'] = 'Username is required.'
        if not email:
            errors['email'] = 'Email is required.'
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors['email'] = 'Invalid email format.'
        if not password:
            errors['password'] = 'Password is required.'
        if password != confirm_password:
            errors['confirm_password'] = 'Passwords do not match.'

        if not errors:
            try:
                CustomUser.objects.create(
                    username=username,
                    email=email,
                    password=make_password(password),
                    user_type='reader'  
                )
                messages.success(request, 'Account created successfully! Please log in.')
                return redirect('login')
            except IntegrityError as e:
                error_message = str(e)
                if 'username' in error_message:
                    errors['username'] = 'Username already exists.'
                if 'email' in error_message:
                    errors['email'] = 'Email already exists.'
                else:
                    errors['general'] = 'An error occurred during registration.'

    return render(request, 'authentication/register.html', {'errors': errors})
        

def home(request):
    return render(request, 'home_app/home.html')