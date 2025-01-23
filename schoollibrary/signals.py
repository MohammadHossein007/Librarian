from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import Loan


@receiver(post_save, sender=Loan)
def update_book_availability(sender, instance, created, **kwargs):
    book = instance.book
    if instance.status == 'returned':
        book.is_available = True
    else:
        book.is_available = False
    book.save()