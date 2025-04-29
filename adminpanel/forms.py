from django import forms
from django.db.models import Q

from library.models import Loan, Book

class CreateLoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['member', 'book']

    def __init__(self, *args, **kwargs):
        super(CreateLoanForm, self).__init__(*args, **kwargs)
        self.fields['book'].queryset = Book.objects.filter(~Q(loan__status__in =['b','o']))
