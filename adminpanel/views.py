from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.timezone import now, timedelta
from django.views import View
from django.views.generic import UpdateView, CreateView, ListView, TemplateView, DeleteView, DetailView
from adminpanel.forms import CreateLoanForm
from adminpanel.mixins import StaffRequiredMixin
from library.models import Loan, Category, Book, Author, Comment

User = get_user_model()

class DashboardView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'adminpanel/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['book_count'] = Book.objects.count()
        context['members_count'] = User.objects.filter(is_active=True).count()
        context['category_count'] = Category.objects.count()

        context['recent_users'] = User.objects.order_by('-date_joined')[:5]

        context['recent_comments'] = Comment.objects.select_related('user').order_by('-created_at')[:5]

        today = now().date()
        days = [(today - timedelta(days=i)) for i in reversed(range(7))]
        registration_counts = []
        for day in days:
            count = User.objects.filter(date_joined__date=day).count()
            registration_counts.append(count)

        context['registration_days'] = [day.strftime('%d/%m') for day in days]
        context['registration_data'] = registration_counts

        return context



class CommentListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Comment
    template_name = 'adminpanel/comment_list.html'

    def get_queryset(self):
        return Comment.objects.select_related('user','book').filter(is_approved=False)


class CommentDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = Comment
    template_name = 'adminpanel/comment_detail.html'
    context_object_name = 'comment'

    def get_queryset(self):
        return Comment.objects.select_related('user','book').filter(is_approved=False)


class ApproveCommentView(LoginRequiredMixin, StaffRequiredMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.is_approved = True
        comment.save()
        return redirect('adminpanel:comment_list')


class DeleteCommentView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Comment
    template_name = 'adminpanel/comment_confirm_delete.html'
    success_url = reverse_lazy('adminpanel:comment_list')


class CreateBookView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'short_description', 'full_description', 'author', 'category', 'image']
    template_name = 'adminpanel/book_form.html'
    success_url = reverse_lazy('adminpanel:book_list')


class DeleteBookView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Book
    template_name = 'adminpanel/book_confirm_delete.html'
    success_url = reverse_lazy('adminpanel:book_list')


class BookListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Book
    template_name = 'adminpanel/book_list.html'

    def get_queryset(self):
        return Book.objects.select_related('author').order_by('-placed_at')


class BookUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Book
    template_name = 'adminpanel/update_book.html'
    fields = ['title', 'short_description', 'full_description', 'author', 'category', 'image']
    success_url = reverse_lazy('adminpanel:book_list')


class CreateCategoryView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Category
    template_name = 'adminpanel/category_form.html'
    fields = ['title', 'image']
    success_url = reverse_lazy('adminpanel:category_list')


class CategoryListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Category
    template_name = 'adminpanel/category_list.html'
    def get_queryset(self):
        return Category.objects.annotate(books_num = Count('book'))


class DeleteCategoryView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Category
    template_name = 'adminpanel/category_confirm_delete.html'
    success_url =  reverse_lazy('adminpanel:category_list')


class UpdateCategoryView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Category
    template_name = 'adminpanel/update_category.html'
    fields = ['title', 'image']
    success_url = reverse_lazy('adminpanel:category_list')


class LoanListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Loan
    template_name = 'adminpanel/loan_list.html'

    def get_queryset(self):
        return Loan.objects.order_by("-borrowed_on")


class CreateLoanView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    form_class = CreateLoanForm
    template_name = 'adminpanel/loan_form.html'
    success_url = reverse_lazy('adminpanel:loan_list')

    def form_valid(self, form):
        member = form.cleaned_data['member']

        active_loans = Loan.objects.filter(
            member=member,
            status__in=['o' , 'b']
        ).count()

        if active_loans >= 2:
            form.add_error(None,"این عضو در حال حاضر دو کتاب قرض گرفته است. نمیتوان بیشتر از دو کتاب قرض گرفت")
            return self.form_invalid(form)

        messages.success(self.request, "کتاب با موفقیت قرض داده شد.")
        return super().form_valid(form)


class ReturnBookView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Loan
    template_name = 'adminpanel/return_book.html'
    fields = []

    def form_valid(self, form):
        loan = form.instance
        loan.status = 'r'
        loan.save()
        messages.success(self.request, "کتاب با موفقیت برگردانده شد")
        return redirect('adminpanel:loan_list')


class CreateAuthorView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Author
    template_name = 'adminpanel/author_form.html'
    success_url = reverse_lazy('adminpanel:author_list')
    fields = ['name', 'bio']


class ListAuthorView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Author
    template_name = 'adminpanel/author_list.html'

class DeleteAuthorView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Author
    template_name = 'adminpanel/author_confirm_delete.html'
    success_url =  reverse_lazy('adminpanel:author_list')


class UpdateAuthorView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Author
    template_name = 'adminpanel/update_author.html'
    fields = ['name', 'bio']
    success_url = reverse_lazy("adminpanel:author_list")
