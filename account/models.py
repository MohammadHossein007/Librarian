from django.db import models
from django.contrib.auth.models import AbstractUser
from extensions.utils import jalali_converter

class Member(AbstractUser):
    membership_id = models.IntegerField(primary_key=True, null=False, verbose_name='کد عضویت')
    membership_start_date = models.DateField(auto_now_add=True, null=True, verbose_name='تاریخ شروع عضویت')
    membership_end_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پایان عضویت')
    profile_image = models.ImageField(blank=True, verbose_name='تصویر پروفایل')

    class Meta:
        verbose_name = 'عضو'
        verbose_name_plural = 'اعضاء'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def jmembership_end_date(self):
            return jalali_converter(self.membership_end_date)
    jmembership_end_date.short_description = 'پایان عضویت'


    def jmembership_start_date(self):
            return jalali_converter(self.membership_end_date)
    jmembership_end_date.short_description = 'شروع عضویت'
