from .views import (
    UserProfileView, CustomLoginView, RegisterView, VerifyCodeView, CompleteProfileView, EditProfileView,
    CustomChangePasswordView, MyBooksView, WishlistView, RemoveFromWishlistView
)
from django.urls import path
from django.contrib.auth import views
app_name = 'account'
urlpatterns = [
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
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("verify/", VerifyCodeView.as_view(), name="verify_code"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path('profile/complete/', CompleteProfileView.as_view(), name='complete_profile'),
    path("profile/<int:pk>/edit/", EditProfileView.as_view(), name="edit_profile"),
    path("password_change/", CustomChangePasswordView.as_view(), name="password_change"),
    path("books/", MyBooksView.as_view(), name="books"),
    path("wishlist/", WishlistView.as_view(), name="wishlist"),
    path('book/<int:pk>/remove_from_wishlist/', RemoveFromWishlistView.as_view(), name='remove_from_wishlist'),
]
