from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy


def profile(request):
    return HttpResponse("hello")

# class CreatBookView(LoginRequiredMixin ,CreateView):
#     model = Book
#     fields = ['title', 'author']

def admin(request):
    return render(request, "account/admin.html")

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        elif user.is_staff:
            return reverse_lazy("account:account")
        return reverse_lazy("account:profile")
