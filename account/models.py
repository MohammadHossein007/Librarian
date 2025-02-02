from django.db import models
from django.contrib.auth.models import AbstractUser
from extensions.utils import jalali_converter

class Member(AbstractUser):
    membership_id = models.IntegerField(primary_key=True, null=False, verbose_name='کد عضویت')
    phone_number = models.CharField(max_length=11, blank=True, unique=True, verbose_name='شماره تلفن')
    membership_end_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پایان عضویت')

    class Meta:
        verbose_name = 'عضو'
        verbose_name_plural = 'اعضاء'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def jmembership_end_date(self):
            return jalali_converter(self.membership_end_date)
    jmembership_end_date.short_description = 'پایان عضویت'