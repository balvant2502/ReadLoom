from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from django.http import HttpResponse
from .decorators import role_required
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            #prevent admin self registration 
            if user.user_type == 'admin':
                user.user_type = 'reader'

            user.save()

            login(request, user)
            return redirect_by_role(user)
    else:
        form = RegisterForm()

    return render(request, 'authentication/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect_by_role(user)
    else:
        form = LoginForm(request)
    return render(request, 'authentication/login.html', {'form': form})


@login_required
@role_required('reader')
def user_dashboard_view(request):
    return render(request, 'authentication/user_dashboard.html')

@login_required
@role_required('author')
def author_dashboard_view(request):
    return render(request, 'authentication/author_dashboard.html')

@login_required
def admin_dashboard_view(request):
    if not request.user.is_superuser:
        return redirect('login')
    return render(request, 'authentication/admin_dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def redirect_by_role(user):
    if user.is_superuser:
        return redirect('admin_dashboard')
    elif user.user_type == 'author':
        return redirect('author_dashboard')
    else:
        return redirect('user_dashboard')