from django.urls import path
from adminpanel.views import DashboardView, BookListView, CreateBookView, ReturnBookView, CategoryListView, \
    CreateCategoryView, LoanListView, CreateLoanView, DeleteBookView, ListAuthorView, CreateAuthorView, \
    DeleteAuthorView, DeleteCategoryView, UpdateAuthorView, UpdateCategoryView, BookUpdateView, CommentListView, \
    CommentDetailView, ApproveCommentView, DeleteCommentView

app_name = 'adminpanel'

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("book/", BookListView.as_view(), name="book_list"),
    path("book/add/", CreateBookView.as_view(), name="add_book"),
    path("book/<int:pk>/return/", ReturnBookView.as_view(), name="return_book"),
    path("book/<int:pk>/delete/", DeleteBookView.as_view(), name="delete_book"),
    path("book/<int:pk>/update/", BookUpdateView.as_view(), name="update_book"),
    path("category/", CategoryListView.as_view(), name="category_list"),
    path("category/add/", CreateCategoryView.as_view(), name="add_category"),
    path("category/<int:pk>/delete/", DeleteCategoryView.as_view(), name="delete_category"),
    path("category/<int:pk>/update/", UpdateCategoryView.as_view(), name="update_category"),
    path("loan/", LoanListView.as_view(), name="loan_list"),
    path("loan/add/", CreateLoanView.as_view(), name="add_loan"),
    path('author/', ListAuthorView.as_view(), name='author_list'),
    path('author/add/', CreateAuthorView.as_view(), name='add_author'),
    path('author/<int:pk>/delete/', DeleteAuthorView.as_view(), name='delete_author'),
    path('author/<int:pk>/update/', UpdateAuthorView.as_view(), name='update_author'),
    path('comment/', CommentListView.as_view(), name='comment_list'),
    path('comment/<int:pk>/detail/', CommentDetailView.as_view(), name='comment_detail'),
    path('comment/<int:pk>/approve/', ApproveCommentView.as_view(), name='approve_comment'),
    path('comment/<int:pk>/delete/', DeleteCommentView.as_view(), name='delete_comment'),
]


