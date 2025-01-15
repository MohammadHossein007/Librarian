from django.urls import path
from . import views


urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('book/?id=<int:book_id>', views.book_info, name='book_info'),
    path('category/?id=<int:category_id>', views.books_by_category, name='books_by_category')
]
