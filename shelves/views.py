from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from authentication.decorators import role_required

# Create your views here.
@login_required
@role_required('reader')
def shelves_view(request):
    return render(request, 'shelves/shelves.html')