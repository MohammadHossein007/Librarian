from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.urls import reverse
from account.models import Member
from extensions.utils import jalali_converter
from django.conf import settings


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


class Comment(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE , verbose_name="کاربر")
    book = models.ForeignKey('library.Book', on_delete=models.CASCADE, related_name='comments', verbose_name="کتاب")
    text = models.TextField(verbose_name='متن نظر')
    created_at = models.DateField(auto_now_add=True, verbose_name='تاریخ')
    is_approved = models.BooleanField(default=False, verbose_name='تاییدیه')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.user.username} on {self.book.title}'

    def jcreated_at(self):
        return jalali_converter(self.created_at)



class Book(models.Model):
    title = models.CharField(max_length=128, unique=True, verbose_name='عنوان')
    short_description = models.TextField(blank=True, verbose_name='معرفی کوتاه')
    full_description = models.TextField(verbose_name='توضیحات' , null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, verbose_name='نویسنده')
    category = models.ManyToManyField(Category, verbose_name='دسته بندی ها', related_name='book')
    image = models.ImageField(default='no-image-available-icon-vector.jpg', blank=True, verbose_name='تصویر')
    placed_at = models.DateField(auto_now=True, verbose_name='تاریخ اضافه شدن')

    class Meta:
        verbose_name = 'کتاب'
        verbose_name_plural = 'کتاب ها'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('account:books')

    def jplaced_at(self):
        return jalali_converter(self.placed_at)
    jplaced_at.short_description='تاریخ اضافه شدن'

    def get_category(self):
        return " | ".join([c.title for c in self.category.all()])

    def is_available(self):
        return not Loan.objects.filter(book=self, status__in=['b', 'o']).exists()


class Loan(models.Model):
    STATUS_CHOICES = [
        ('b', 'قرض گرفته شده'),
        ('r', 'برگردانده شده'),
        ('o', 'عقب افتاده'),
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='کتاب')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name='عضو')
    borrowed_on = models.DateField(default=timezone.now , verbose_name='تاریخ بردن')
    return_by = models.DateField(verbose_name='تاریخ برگشت')
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='b', verbose_name='وضعیت')

    class Meta:
        verbose_name = 'امانت'
        verbose_name_plural = 'امانت ها'


    def jreturn_by(self):
            return jalali_converter(self.return_by)
    jreturn_by.short_description = 'تاریخ برگشت'

    def jborrowed_on(self):
            return jalali_converter(self.borrowed_on)
    jborrowed_on.short_description = 'تاریخ بردن'

    def save(self, *args, **kwargs):
        if not self.return_by:
            self.return_by = self.borrowed_on + timedelta(days=7)
        super().save(*args, **kwargs)


class Wishlist(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name='عضو')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='کتاب')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ اضافه شدن')

    class Meta:
        verbose_name = 'لیست علاقه‌مندی'
        verbose_name_plural = 'لیست علاقه‌مندی‌ها'
        unique_together = ('member', 'book')

    def __str__(self):
        return f'{self.member.user.username} - {self.book.title}'
