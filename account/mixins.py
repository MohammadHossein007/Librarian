from django.shortcuts import redirect
from django.urls import reverse_lazy

class MembershipPermissionMixin:
    redirect_url = 'account:profile'

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'membership_id') or request.user.membership_id != kwargs.get('pk'):
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)


class StaffRedirectMixin:
    staff_redirect_url = reverse_lazy('adminpanel:dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return redirect(self.staff_redirect_url)
        return super().dispatch(request, *args, **kwargs)
