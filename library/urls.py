from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('book/<int:pk>', views.book_info, name='book_info'),
    path('category/<int:pk>', views.books_in_category, name='books_by_category'),
]
