from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.template.base import kwarg_re
from account.models import Member
from library.models import Loan, Book


class CreateLoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['member', 'book']

    def __init__(self, *args, **kwargs):
        super(CreateLoanForm, self).__init__(*args, **kwargs)
        self.fields['book'].queryset = Book.objects.filter(~Q(loan__status__in =['b','o']))


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'w-full outline-none text-sm bg-transparent',
            'placeholder': 'نام کاربری'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'w-full outline-none text-sm bg-transparent',
            'placeholder': 'رمز عبور'
        })


class EmailPasswordForm(forms.Form):
    email = forms.EmailField()
    email.widget.attrs.update({
        'class': 'w-full outline-none text-sm bg-transparent',
        'placeholder' : 'ایمیل',
    })


class VerifyCodeForm(forms.Form):
    code = forms.CharField(label="کد تأیید", max_length=6)


class CompleteProfileForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class' : 'border rounded-lg px-4 py-2 w-full focus:ring-2 focus:ring-blue-400'
        }),
        label="رمز عبور",
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class' : 'border rounded-lg px-4 py-2 w-full focus:ring-2 focus:ring-blue-400'
        }),
        label="تکرار رمز عبور"
    )

    class Meta:
        model = Member
        fields = ['first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("رمز عبور و تکرار آن یکسان نیستند!")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs.update({
                'class': 'border rounded-lg px-4 py-2 w-full focus:ring-2 focus:ring-blue-400'
            })
