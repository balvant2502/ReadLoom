from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from django.http import HttpResponse
from .decorators import role_required
from books.models import Book, ReadingProgress,ReadingStreak
from django.db.models import Avg, Prefetch, Sum
from .models import UserBadge

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

    streak, _ = ReadingStreak.objects.get_or_create(user=request.user)
    badges = UserBadge.objects.filter(
        user=request.user
    ).select_related("badge")
    total_reading_seconds = ReadingProgress.objects.filter(
        user=request.user
    ).aggregate(total=Sum('reading_seconds'))['total'] or 0
    total_reading_hours = round(total_reading_seconds / 3600, 1)

    # only user's active reading records
    progress_qs = ReadingProgress.objects.filter(
        user=request.user,
        is_finished=False
    )

    current_books = Book.objects.filter(
        readingprogress__user=request.user,
        readingprogress__is_finished=False,
        status='approved'
    ).prefetch_related(
        Prefetch(
            'readingprogress_set',
            queryset=progress_qs,
            to_attr='user_progress'
        )
    ).distinct()

    return render(request, 'authentication/reader_dashboard.html', {
        'current_books': current_books,
        'streak': streak,
        'total_reading_hours': total_reading_hours,
        'badges':badges
    })

@login_required
@role_required('author')
def author_dashboard_view(request):
        books = Book.objects.filter(author=request.user)

        total_books = books.count()
        total_reads = books.aggregate(total=Sum('reads'))['total'] or 0
        avg_rating = books.aggregate(avg=Avg('average_rating'))['avg'] or 0
    
        context = {
            'books': books,
            'total_books': total_books,
            'total_reads': total_reads,
            'avg_rating': round(avg_rating, 2)
        }
    
        return render(request, 'authentication/author_dashboard.html', context)

@login_required
@role_required('admin')
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
        return redirect('dashboard')
    
@login_required
def profile_update_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect_by_role(request.user)
    else:
        form = ProfileUpdateForm(instance=request.user, user=request.user)

    return render(request, 'authentication/profile_update.html', {'form': form})



        