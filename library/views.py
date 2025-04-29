from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy

from account.mixins import StaffRedirectMixin
from .forms import CommentForm
from django.views.generic import ListView, DetailView
from .models import Book, Category, Wishlist


class MainPageView(ListView):
    model = Category
    template_name = 'library/main_page.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get("q")
        not_empty_categories = Category.objects.prefetch_related('book__author').filter(book__isnull=False).distinct()
        context['not_empty_categories'] = not_empty_categories

        if search:
            books = Book.objects.select_related('author').filter(title__icontains=search)
            context['books'] = books
            context['search'] = search
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'library/book_info.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        categories = Category.objects.all()
        comments = book.comments.filter(is_approved=True)
        form = CommentForm()
        is_in_wishlist = Wishlist.objects.filter(member=self.request.user, book=book).exists()


        context['is_in_wishlist'] = is_in_wishlist
        context['categories'] = categories
        context['comments'] = comments
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        if not request.user.is_authenticated:
            return redirect('account:login')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.book = book
            comment.save()
            return redirect('library:book_info', pk=book.pk)

        return self.get(request, *args, **kwargs)


class BooksInCategoryView(ListView):
    model = Book
    template_name = 'library/category.html'
    context_object_name = 'books'

    def get_queryset(self):
        category = self.get_object()
        return category.book.prefetch_related('author').order_by("placed_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        all_categories = Category.objects.all()
        context['category'] = category
        context['all_categories'] = all_categories
        return context


class AddToWishListView(LoginRequiredMixin, StaffRedirectMixin, DetailView):
    model = Book
    template_name = 'library/book_info.html'
    staff_redirect_url = reverse_lazy('library:main_page')

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        member = request.user

        if not Wishlist.objects.filter(member=member, book=book).exists():
            Wishlist.objects.create(member=member, book=book)


        return redirect('library:book_info', pk=book.id)
