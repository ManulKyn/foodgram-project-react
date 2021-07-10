from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordResetView
)
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import (
    CreationForm, CustomAuthenticationForm, CustomPasswordChangeForm,
    CustomPasswordResetForm
)


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('index')
    template_name = 'templates/reg.html'


class Login(LoginView):
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy('index')
    template_name = 'templates/authForm.html'


class Logout(LogoutView):
    template_name = 'templates/registration/logout.html'


class PasswordReset(PasswordResetView):
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('index')
    template_name = 'templates/resetPassword.html'


class PasswordChange(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('index')
    template_name = 'templates/changePassword.html'
