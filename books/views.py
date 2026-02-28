from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from authentication.decorators import role_required
from .forms import BookForm
from django.shortcuts import get_object_or_404
from .models import Book, BookRead, ReadingProgress
from django.db.models import Q
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import HttpResponse, Http404, StreamingHttpResponse
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib import messages

@login_required
@role_required('author')
def upload_book(request):

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)

        if form.is_valid():
            book = form.save(commit=False)
            book.author = request.user
            book.status = 'pending'
            book.save()

            return redirect('author_books')
    else:
        form = BookForm()

    return render(request, 'books/upload_book.html', {'form': form})

def author_books(request):
    return HttpResponse("Author Books Page Working")


def book_list(request):
        books = Book.objects.filter(status='approved')

        # Search
        query = request.GET.get('q')
        if query:
            books = books.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
       
        # Category filter
        category = request.GET.get('category')
        if category:
            books = books.filter(category=category)
       
        return render(request, 'books/book_list.html', {
            'books': books,
            'categories': Book.CATEGORY_CHOICES
        })


@login_required
def book_detail(request, slug):
    # Try to get the book first
    try:
        book = Book.objects.get(slug=slug)
    except Book.DoesNotExist:
        raise Http404("Book not found")
    
    # Check if book is approved
    if book.status != 'approved':
        # If not approved, show error message
        messages.error(request, "Unapproved books cannot be displayed.")
        return redirect('author_dashboard')

    # Check if user already read this book
    already_read = BookRead.objects.filter(
        user=request.user,
        book=book
    ).exists()

    if not already_read:
        BookRead.objects.create(
            user=request.user,
            book=book
        )
        book.reads += 1
        book.save()
    return render(request, 'books/book_detail.html', {'book': book})



@login_required
@role_required('author')
def edit_book(request, slug):

    book = get_object_or_404(Book, slug=slug, author=request.user)

    # To Prevent editing if approved
    if book.status == 'approved':
        messages.warning(request, "Approved books cannot be edited.")
        return redirect('author_dashboard')

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book uploaded successfully and is pending approval.")
            return redirect('author_dashboard')
    else:
        form = BookForm(instance=book)

    return render(request, 'books/edit_book.html', {'form': form})


@login_required
@role_required('author')
def delete_book(request, slug):

    book = get_object_or_404(Book, slug=slug, author=request.user)

    if request.method == "POST":
        book.delete()

    return redirect('author_dashboard')


@login_required
def book_reader(request, slug):
    book = get_object_or_404(Book, slug=slug, status='approved')

    if not book.book_file:
        return HttpResponse("No PDF file available for this book.", status=404)
    progress = ReadingProgress.objects.filter(
    user=request.user,
    book=book
    ).first()

    last_page = progress.last_page if progress else 1
    return render(request, 'books/reader.html', {'book': book, 'last_page': last_page})

def stream_pdf(request, slug):
    book = get_object_or_404(Book, slug=slug)

    response = HttpResponse(
        book.book_file.open('rb'),
        content_type='application/pdf'
    )
    response['Content-Disposition'] = 'inline'
    return response

@csrf_exempt
def save_progress(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')

    data = json.loads(request.body)

    page = data.get('page')
    total = data.get('total')

    book = get_object_or_404(Book, slug=slug)

    progress = (page / total) * 100

    obj, created = ReadingProgress.objects.update_or_create(
        user=request.user,
        book=book,
        defaults={
            'last_page': page,
            'total_pages': total,
            'progress': progress
        }
    )

    return JsonResponse({
        'status': 'saved',
        'page': page,
        'progress': round(progress, 2)
    })
