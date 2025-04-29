from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class StaffRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_staff:
            return redirect('account:login')
        return super().dispatch(request, *args, **kwargs)