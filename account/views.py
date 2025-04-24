from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, FormView
from account.forms import CreateLoanForm, EmailPasswordForm, VerifyCodeForm, CompleteProfileForm, CustomLoginForm
from account.mixins import StaffRequiredMixin
from account.models import Member
from library.models import Book, Category, Loan
from datetime import datetime, timedelta
import random

User = get_user_model()

@login_required
def profile(request):
    return render(request, 'account/profile.html')

class DashboardView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'account/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_count'] = Book.objects.count()
        context['category_count'] = Category.objects.count()
        context['members_count'] = Member.objects.count()
        return context


class RegisterView(FormView):
    template_name = 'account/register.html'
    form_class = EmailPasswordForm
    success_url = reverse_lazy('account:verify_code')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        code = random.randint(100000, 999999)

        if User.objects.filter(email=email).exists():
            messages.error(self.request, 'ایمیل وارد شده قبلا ثبت شده است')
            return self.form_invalid(form)

        self.request.session['code'] = code
        self.request.session['email'] = email
        self.request.session['code_expiry'] = (datetime.now() + timedelta(minutes=2)).isoformat()

        send_mail(
            'کد تایید.',
            f'کد تایید شما {code}',
            'mohammadi.hoseein2007@gmail.com',
            [email],
            fail_silently=False,
        )
        self.request.session['email_sent'] = True
        return super().form_valid(form)


class VerifyCodeView(FormView):
    template_name = 'account/verify_code.html'
    form_class = VerifyCodeForm
    success_url = reverse_lazy('account:complete_profile')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.session.get('email_sent'):
            return redirect('account:register')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user_code = form.cleaned_data['code']
        session_code = self.request.session.get('code')

        expiry_str = self.request.session.get('code_expiry')
        if expiry_str:
            expiry_time = datetime.fromisoformat(expiry_str)
            if datetime.now() > expiry_time:
                messages.error(self.request, "مهلت وارد کردن کد به پایان رسیده است. لطفاً دوباره درخواست کد دهید.")
                return redirect('account:register')

        if str(user_code) == str(session_code):
            self.request.session['verified'] = True
            return super().form_valid(form)
        else:
            messages.error(self.request, "کد تایید اشتباه است!")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.request.session.get('email')
        return context


class CompleteProfileView(FormView):
    template_name = 'account/complete_profile.html'
    form_class = CompleteProfileForm
    success_url = reverse_lazy('account:login')

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('verified'):
            return redirect('account:register')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        print(form.errors)
        email = self.request.session.get('email')
        if not email:
            return redirect('account:register')

        password = form.cleaned_data.get('password')

        member = form.save(commit=False)
        member.email = email
        member.username = email

        member.set_password(password)
        member.save()

        for key in ['email', 'code', 'verified', 'email_sent', 'code_expiry']:
            self.request.session.pop(key, None)

        messages.success(self.request, "حساب شما با موفقیت ساخته شد! لطفاً وارد شوید.")
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = "account/login.html"
    redirect_authenticated_user = True
    authentication_form = CustomLoginForm

    def get_success_url(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return reverse_lazy("account:dashboard")
        return reverse_lazy("account:profile")


class CreateBookView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'description', 'author', 'category', 'image']
    template_name = 'account/book_form.html'
    success_url = reverse_lazy('account:book_list')


class BookListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Book
    template_name = 'account/book_list.html'

    def get_queryset(self):
        return Book.objects.select_related('author').order_by('-placed_at')


class CreateCategoryView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Category
    template_name = 'account/category_form.html'
    fields = ['title', 'image']
    success_url = reverse_lazy('account:category_list')


class CategoryListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Category
    template_name = 'account/category_list.html'
    def get_queryset(self):
        return Category.objects.annotate(books_num = Count('book'))


class LoanListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Loan
    template_name = 'account/loan_list.html'


class CreateLoanView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    form_class = CreateLoanForm
    template_name = 'account/loan_form.html'
    success_url = reverse_lazy('account:loan_list')


class ReturnBookView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Loan
    template_name = 'account/return_book.html'
    fields = []

    def form_valid(self, form):
        loan = form.instance
        loan.status = 'r'
        loan.save()
        return redirect('account:loan_list')

