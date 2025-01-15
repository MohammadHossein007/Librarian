from enum import unique
from operator import truediv
from pickle import TRUE
from django.db import models
from django.forms import SlugField

class Member(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(null=False, unique=True)
    phone_number = models.CharField(max_length=11, blank=True, unique=True)
    membership_id = models.IntegerField(primary_key=True, null=False)
    membership_start_date = models.DateField(auto_now_add=True)
    membership_end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Category(models.Model):
    title = models.CharField(max_length=128)
    image = models.ImageField(default='no-image-available-icon-vector.jpg', blank=True)

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=128)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


class  Book(models.Model):
    title = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    category = models.ManyToManyField(Category)
    image = models.ImageField(default='no-image-available-icon-vector.jpg', blank=True)
    placed_at = models.DateField(auto_now=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    # def get_category(self):
    #     return ' | '.join([c.title for c in self.category.all()])


class Loan(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ]
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    borrowed_on = models.DateField(auto_now_add=True)
    return_by = models.DateField()
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='borrowed')
