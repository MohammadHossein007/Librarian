from django.shortcuts import get_object_or_404, render, redirect, get_list_or_404
from .models import Book, Category


def main_page(request):
    categories = Category.objects.all()
    not_empty_categories = Category.objects.prefetch_related('book_set').filter(book__isnull=False).distinct()
    context = {
        'categories': categories,
        'not_empty_categories': not_empty_categories,
    }

    return render(request, 'main_index.html', context)


def book_info(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    context = {
        'book': book,
    }

    return render(request, 'book_info.html', context)


def books_by_category(request, category_id):
    # books = get_list_or_404(Category, id=category_id)
    # category = get_object_or_404(Category, id=category_id)
    category = get_object_or_404(Category, id=category_id)
    books = category.book_set.all()
    all_categories = Category.objects.all()
    context = {
        'category': category,
        'books': books,
        'all_categories': all_categories,
    }

    return render(request, 'category.html', context)
