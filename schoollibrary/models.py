from enum import unique
from operator import truediv
from pickle import TRUE
from django.db import models
from extensions.utils import jalali_converter
from django.forms import SlugField
from django.db.models.signals import post_save
from django.dispatch import receiver

# Models
class Member(models.Model):
    first_name = models.CharField(max_length=128, verbose_name='نام')
    last_name = models.CharField(max_length=128, verbose_name='نام خانوادگی')
    email = models.EmailField(null=False, unique=True, verbose_name='آدرس ایمیل')
    phone_number = models.CharField(max_length=11, blank=True, unique=True, verbose_name='شماره تلفن')
    membership_id = models.IntegerField(primary_key=True, null=False, verbose_name='کد عضویت')
    membership_start_date = models.DateField(auto_now_add=True, verbose_name='تاریخ شروع عضویت')
    membership_end_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پایان عضویت')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'عضو'
        verbose_name_plural = 'اعضاء'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def jmembership_start_date(self):
            return jalali_converter(self.membership_start_date)
    jmembership_start_date.short_description = 'شروع عضویت'

    def jmembership_end_date(self):
            return jalali_converter(self.membership_end_date)
    jmembership_end_date.short_description = 'پایان عضویت'

class Category(models.Model):
    title = models.CharField(max_length=128, verbose_name='عنوان')
    image = models.ImageField(default='no-image-available-icon-vector.jpg', blank=True, verbose_name='تصویر')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=128, verbose_name='نام نویسنده')
    bio = models.TextField(blank=True, verbose_name='بیوگرافی')

    class Meta:
        verbose_name = 'نویسنده'
        verbose_name_plural = 'نویسنده ها'

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=128, unique=True, verbose_name='عنوان')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, verbose_name='نویسنده')
    category = models.ManyToManyField(Category, verbose_name='دسته بندی ها')
    image = models.ImageField(default='no-image-available-icon-vector.jpg', blank=True, verbose_name='تصویر')
    placed_at = models.DateField(auto_now=True, verbose_name='تاریخ اضافه شدن')
    is_available = models.BooleanField(default=True, verbose_name='موجود')

    class Meta:
        verbose_name = 'کتاب'
        verbose_name_plural = 'کتاب ها'

    def __str__(self):
        return self.title

    def jplaced_at(self):
        return jalali_converter(self.placed_at)
    jplaced_at.short_description='تاریخ اضافه شدن'


class Loan(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'قرض گرفته شده'),
        ('returned', 'برگردانده شده'),
        ('overdue', 'عقب افتاده'),
    ]
    book = models.ForeignKey(Book, on_delete=models.PROTECT, verbose_name='کتاب')
    member = models.ForeignKey(Member, on_delete=models.PROTECT, verbose_name='عضو')
    borrowed_on = models.DateField(auto_now_add=True, verbose_name='تاریخ بردن')
    return_by = models.DateField(verbose_name='تاریخ برگشت')
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='borrowed', verbose_name='وضعیت')

    class Meta:
        verbose_name = 'امانت'
        verbose_name_plural = 'امانت ها'


    def jreturn_by(self):
            return jalali_converter(self.return_by)
    jreturn_by.short_description = 'تاریخ برگشت'

    def jborrowed_on(self):
            return jalali_converter(self.borrowed_on)
    jborrowed_on.short_description = 'تاریخ بردن'


# Signals
@receiver(post_save, sender=Loan)
def update_book_availability(sender, instance, created, **kwargs):
    book = instance.book
    if instance.status == 'returned':
        book.is_available = True
    else:
        book.is_available = False
    book.save()
