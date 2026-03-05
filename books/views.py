from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from authentication.decorators import role_required
from .forms import BookForm
from django.shortcuts import get_object_or_404
from .models import Book, ReadingProgress, BookRating
from django.db.models import Q
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import HttpResponse, Http404, StreamingHttpResponse
import os
from django.http import JsonResponse
from django.views.decorators.http import require_POST
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

            return redirect('author_dashboard')
    else:
        form = BookForm()

    return render(request, 'books/upload_book.html', {'form': form})




def book_detail(request, slug):
    completed_count = 0
    try:
        book = Book.objects.get(slug=slug)
    except Book.DoesNotExist:
        raise Http404("Book not found")

    if book.status != 'approved':
        messages.error(request, "Unapproved books cannot be displayed.")
        return redirect('author_dashboard')

    user_rating = None
    locked = False
    if request.user.is_authenticated:
        # reading progress logic (already correct)
        if not ReadingProgress.objects.filter(user=request.user, book=book).exists():
            ReadingProgress.objects.create(user=request.user, book=book)
            book.reads += 1
            book.save(update_fields=['reads'])

        # ⭐ RATING LOGIC
        if request.method == "POST" and 'rating' in request.POST:
            rating_value = int(request.POST['rating'])

            rating_obj, created = BookRating.objects.update_or_create(
                user=request.user,
                book=book,
                defaults={'rating': rating_value}
            )

            book.update_average_rating()  # 🔥 THIS FIXES 0.0

            return redirect('book_detail', slug=slug)

        user_rating = BookRating.objects.filter(
            user=request.user,
            book=book
        ).first()

        # Book unlock feature logic
        
        completed_count = ReadingProgress.objects.filter(
            user=request.user,
            is_finished=True
        ).count()

        if completed_count < book.unlock_after_books and request.user.user_type == 'reader':
            locked = True
        else:
            locked = False
    else:
        locked = True
    return render(request, 'books/book_detail.html', {
        'book': book,
        'user_rating': user_rating,
        'locked': locked,
        'completed_count': completed_count
    })


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

@require_POST
def save_progress(request, slug):

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Login required'}, status=401)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    page = int(data.get('page', 1))
    total = int(data.get('total', 0))

    if total <= 0:
        return JsonResponse({'error': 'Invalid total pages'}, status=400)

    book = get_object_or_404(Book, slug=slug)

    
    # prevent invalid values
    page = min(page, total)


    progress = (page / total) * 100
    progress = round(progress, 2)


    obj, created = ReadingProgress.objects.update_or_create(
        user=request.user,
        book=book,
        defaults={
            'last_page': page,
            'total_pages': total,
            'progress': progress,
            'is_finished': progress >= 100
        }
    )

    return JsonResponse({
        'status': 'saved',
        'page': page,
        'progress': progress
    })


def browse_books(request):

    books = Book.objects.filter(status='approved')

    query = request.GET.get('q')
    category = request.GET.get('category')

    # SEARCH MODE
    if query or category:

        if query:
            books = books.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(author__first_name__icontains=query)
            )

        if category:
            books = books.filter(category=category)

        return render(request, 'books/browse.html', {
            'search_results': books,
            'is_search': True,
            'categories': Book.CATEGORY_CHOICES
        })

    # DEFAULT BROWSE MODE
    trending_books = Book.objects.filter(
        status='approved',
        is_featured=False
    ).order_by('-reads')[:10]
    recent_books = Book.objects.filter(
        status='approved',
        is_featured=False
    ).order_by('-created_at')[:10]
    featured_books = Book.objects.filter(
        status='approved',
        is_featured=True
    ).order_by('-created_at')[:10]

    return render(request, 'books/browse.html', {
        'trending_books': trending_books,
        'recent_books': recent_books,
        'featured_books': featured_books,
        'is_search': False,
        'categories': Book.CATEGORY_CHOICES
    })