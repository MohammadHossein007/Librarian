from .views import (
    profile,
    CustomLoginView,
    BookListView,
    CreateBookView,
    DashboardView,
    CreateCategoryView,
    CategoryListView,
    LoanListView, CreateLoanView, ReturnBookView, RegisterView,VerifyCodeView, CompleteProfileView
)
from django.urls import path
from django.contrib.auth import views
app_name = 'account'
urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    # path(
    #     "password_change/", views.PasswordChangeView.as_view(), name="password_change"
    # ),
    # path(
    #     "password_change/done/",
    #     views.PasswordChangeDoneView.as_view(),
    #     name="password_change_done",
    # ),
    # path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    # path(
    #     "password_reset/done/",
    #     views.PasswordResetDoneView.as_view(),
    #     name="password_reset_done",
    # ),
    # path(
    #     "reset/<uidb64>/<token>/",
    #     views.PasswordResetConfirmView.as_view(),
    #     name="password_reset_confirm",
    # ),
    # path(
    #     "reset/done/",
    #     views.PasswordResetCompleteView.as_view(),
    #     name="password_reset_complete",
    # ),
]

urlpatterns += [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify/", VerifyCodeView.as_view(), name="verify_code"),
    path("profile/", profile, name="profile"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("book/", BookListView.as_view(), name="book_list"),
    path("book/add", CreateBookView.as_view(), name="add_book"),
    path("book/return/<int:pk>", ReturnBookView.as_view(), name="return_book"),
    path("category/", CategoryListView.as_view(), name="category_list"),
    path("category/add", CreateCategoryView.as_view(), name="add_category"),
    path("loan/", LoanListView.as_view(), name="loan_list"),
    path("loan/add", CreateLoanView.as_view(), name="add_loan"),
    path('profile/complete', CompleteProfileView.as_view(), name='complete_profile'),
]
