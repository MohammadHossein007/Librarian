from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.mail import send_mail
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, UpdateView, ListView, CreateView, DetailView, DeleteView, View
from account.forms import EmailForm, VerifyCodeForm, CompleteProfileForm, CustomLoginForm
from datetime import datetime, timedelta
import random

from account.mixins import MembershipPermissionMixin, StaffRedirectMixin
from library.models import Loan, Comment, Wishlist, Book

User = get_user_model()

class UserProfileView(LoginRequiredMixin, StaffRedirectMixin, TemplateView):
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        member = user

        context['user'] = user
        context['recent_loans'] = Loan.objects.filter(member=member).order_by('-borrowed_on')[:5]
        context['recent_comments'] = Comment.objects.filter(user=user, is_approved=True).order_by('-created_at')[:5]
        context['active_loans'] = Loan.objects.filter(member=member, status='b')
        context['wishlist'] = Wishlist.objects.filter(member=member).select_related('book')

        return context


class RegisterView(FormView):
    template_name = 'account/register.html'
    form_class = EmailForm
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
            f'کد تایید شما برای ثبت نام در سایت کتابدار. آن را در اختیار هیچ کس قرار ندهید.{code}',
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
            return reverse_lazy("adminpanel:dashboard")
        return reverse_lazy("account:profile")


class EditProfileView(LoginRequiredMixin, MembershipPermissionMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'profile_image']
    template_name = 'account/edit_profile.html'
    success_url = reverse_lazy('account:profile')


class CustomChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'account/change_password.html'
    success_url = reverse_lazy('account:profile')


class MyBooksView(LoginRequiredMixin, StaffRedirectMixin, ListView):
    model = Book
    template_name = 'account/books.html'
    context_object_name = 'books'

    def get_queryset(self):
        return Book.objects.filter(loan__member=self.request.user).distinct()


class WishlistView(LoginRequiredMixin, StaffRedirectMixin, ListView):
    model = Wishlist
    template_name = 'account/wishlist.html'
    context_object_name = 'wishlist_items'

    def get_queryset(self):
        return Wishlist.objects.select_related('book').filter(member=self.request.user)


class RemoveFromWishlistView(LoginRequiredMixin, StaffRedirectMixin, View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        if request.user.is_authenticated:
            member = request.user

            wishlist_item = Wishlist.objects.filter(member=member, book=book)
            if wishlist_item.exists():
                wishlist_item.delete()

        next_page = request.POST.get('next', 'library:main_page')
        return redirect(next_page)
