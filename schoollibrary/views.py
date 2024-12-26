from django.shortcuts import render
from . models import Book,Category

def login(request):
    return render(request, 'login_index.html')


def main_page(request):
    return render(request, 'main_index.html')