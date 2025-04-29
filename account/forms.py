from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from account.models import Member
import re


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


class EmailForm(forms.Form):
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
        help_text="رمز عبور باید حداقل 8 کاراکتر باشد، شامل حروف بزرگ، کوچک، عدد و کاراکتر ویژه مانند @ یا # باشد."
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

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise ValidationError('رمز عبور باید حداقل ۸ کاراکتر باشد.')

        if not re.search(r'[A-Z]', password):
            raise ValidationError('رمز عبور باید حداقل یک حرف بزرگ داشته باشد.')

        if not re.search(r'[a-z]', password):
            raise ValidationError('رمز عبور باید حداقل یک حرف کوچک داشته باشد.')

        if not re.search(r'[0-9]', password):
            raise ValidationError('رمز عبور باید حداقل یک عدد داشته باشد.')

        if not re.search(r'[@#$%^&+=!.]', password):
            raise ValidationError('رمز عبور باید حداقل یک کاراکتر ویژه مانند @ یا # داشته باشد.')

        return password

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
