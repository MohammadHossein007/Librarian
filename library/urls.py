from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('book/<int:book_id>', views.book_info, name='book_info'),
    path('category/<int:category_id>', views.books_in_category, name='books_by_category')
]
