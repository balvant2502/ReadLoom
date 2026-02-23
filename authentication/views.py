from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from django.http import HttpResponse

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if(user.user_type == 'reader'):
                return redirect('user_dashboard')
            elif(user.user_type == 'author'):
                return redirect('author_dashboard')
            return redirect('admin_dashboard')
    else:
        form = RegisterForm()

    return render(request, 'authentication/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if(user.user_type == 'reader'):
                return redirect('user_dashboard')
            elif(user.user_type == 'author'):
                return redirect('author_dashboard')
            return redirect('admin_dashboard')
    else:
        form = LoginForm()
    return render(request, 'authentication/login.html', {'form': form})


@login_required
def user_dashboard_view(request):
    return render(request, 'authentication/user_dashboard.html')

@login_required
def author_dashboard_view(request):
    return render(request, 'authentication/author_dashboard.html')

@login_required
def admin_dashboard_view(request):
    return render(request, 'authentication/admin_dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('login')