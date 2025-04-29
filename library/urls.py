from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    path('', views.MainPageView.as_view(), name='main_page'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_info'),
    path('book/<int:pk>/add_to_whishlist', views.AddToWishListView.as_view(), name='add_to_wishlist'),
    path('category/<int:pk>/', views.BooksInCategoryView.as_view(), name='books_by_category'),
]
