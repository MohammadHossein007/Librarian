from django.db import models
from account.models import Member
from extensions.utils import jalali_converter


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
    category = models.ManyToManyField(Category, verbose_name='دسته بندی ها', related_name='book')
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


