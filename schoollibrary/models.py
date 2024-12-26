from django.db import models

class Member(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(null=False)
    membership_id = models.IntegerField(primary_key=True, null=False)

class Category(models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title

class Author(models.Model):
    name = models.CharField(max_length=128)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


class  Book(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    image = models.ImageField(default='no-image-available-icon-vector.jpg')
    placed_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    borrowed_on = models.DateField(auto_now_add=True)
    return_by = models.DateField()