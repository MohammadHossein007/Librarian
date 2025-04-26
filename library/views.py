from django.shortcuts import get_object_or_404, render
from .models import Book, Category


def main_page(request):
    search = request.GET.get("q")
    if search:
        books = Book.objects.select_related('author').filter(title__icontains=search)
        context = {
            'books': books,
            'search': search,
        }
        return render(request, 'library/search_result.html', context)

    categories = Category.objects.all()
    not_empty_categories = Category.objects.prefetch_related('book__author').filter(book__isnull=False).distinct()
    context = {
        'categories': categories,
        'not_empty_categories': not_empty_categories,
    }

    return render(request, 'library/main_page.html', context)


def book_info(request, pk):
    book = get_object_or_404(Book, id=pk)
    categories = Category.objects.all()
    context = {
        'book': book,
        'categories': categories,
    }

    return render(request, 'library/book_info.html', context)


def books_in_category(request, pk):
    category = get_object_or_404(Category.objects.prefetch_related("book"), id=pk)
    books = category.book.prefetch_related('author').order_by("placed_at")
    all_categories = Category.objects.all()
    context = {
        'category': category,
        'books': books,
        'all_categories': all_categories,
    }

    return render(request, 'library/category.html', context)
