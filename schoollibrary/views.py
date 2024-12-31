from django.shortcuts import render
from . models import Book,Category

def login(request):
    return render(request, 'login_index.html')


def main_page(request):
    categories = Category.objects.filter(book__isnull=False).distinct()
    books = Book.objects.all()
    return render(request, 'main_index.html', {'categories' : categories, 'books' : books})