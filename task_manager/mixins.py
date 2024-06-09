from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class UserLoginRequiredMixin:
    login_message = _('You are not logged in! Please log in.')
    login_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:

            messages.add_message(request, messages.ERROR, self.login_message)
            return redirect(self.login_page)

        else:
            return super().dispatch(request, *args, **kwargs)
