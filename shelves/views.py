from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from authentication.decorators import role_required
from .models import Shelf, ShelfBook
from django.http import JsonResponse
from books.models import Book
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

@login_required
@role_required('reader')
@require_POST
def delete_shelf(request, shelf_id):
    shelf = get_object_or_404(
        Shelf,
        id=shelf_id,
        user=request.user
    )

    shelf.delete()

    return JsonResponse({'success': True})


@login_required
@role_required('reader')
def shelves_page(request):
    shelves = Shelf.objects.filter(user=request.user).order_by('created_at')
    return render(request, 'shelves/shelves.html', {
        'shelves': shelves
    })


@login_required
@role_required('reader')
def create_shelf(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()

        if not name:
            return JsonResponse({'error': 'Shelf name required'}, status=400)

        shelf, created = Shelf.objects.get_or_create(
            user=request.user,
            name=name
        )

        if not created:
            return JsonResponse({'error': 'Shelf already exists'}, status=400)

        return JsonResponse({
            'id': shelf.id,
            'name': shelf.name
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@role_required('reader')
def shelf_books(request, shelf_id):
    shelf = get_object_or_404(Shelf, id=shelf_id, user=request.user)

    books = Book.objects.filter(
        shelfbook__shelf=shelf
    ).select_related('author')

    data = []
    for book in books:
        data.append({
            'title': book.title,
            'author': book.author.first_name,
            'cover': book.cover_image.url,
            'slug': book.slug
        })

    return JsonResponse({
        'shelf': shelf.name,
        'books': data
    })

@login_required
@role_required('reader')
def add_to_shelf_page(request, slug):
    book = get_object_or_404(Book, slug=slug, status='approved')

    shelves = Shelf.objects.filter(user=request.user)

    # POST → add book to shelf
    if request.method == "POST":
        shelf_id = request.POST.get("shelf_id")

        if not shelf_id:
            messages.error(request, "Please select a shelf.")
            return redirect('add_to_shelf', slug=slug)

        shelf = get_object_or_404(
            Shelf,
            id=shelf_id,
            user=request.user
        )

        ShelfBook.objects.get_or_create(
            shelf=shelf,
            book=book
        )

        messages.success(request, f"Book added to '{shelf.name}'")
        return redirect('shelves')

    return render(request, 'shelves/add_to_shelf.html', {
        'book': book,
        'shelves': shelves
    })