from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from authentication.decorators import role_required
from .forms import BookForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Book
from .models import BookRead
from django.db.models import Q

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
    book = get_object_or_404(Book, slug=slug, status='approved')

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