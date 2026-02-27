from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'category', 'book_file', 'cover_image', 'total_pages']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter book title'}),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Enter book description',
                'rows': 4
            }),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'book_file': forms.FileInput(attrs={'accept': '.pdf'}),
            'cover_image': forms.FileInput(attrs={'accept': 'image/*'}),
            'total_pages': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Enter total pages'}),
        }
