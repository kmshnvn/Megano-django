from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegisterUserForm
from .models import Profile
from market.config import settings


def success_log(request: HttpRequest) -> HttpResponse:
    """Заглушка"""
    return HttpResponse(f"Success login! {request.META}")


class ResetPasswordView(PasswordResetView):
    """Представление формы сброса пароля."""

    from_email = settings.EMAIL_HOST_USER
    template_name = "profiles/password-reset-form.html"
    email_template_name = "profiles/password-reset-email.html"
    subject_template_name = "profiles/password_reset_subject.txt"
    success_url = reverse_lazy("profiles:password_reset_done")


class ResetPasswordDoneView(PasswordResetDoneView):
    """Представление вывода информации об успешной отправки ссылки для смены пароля."""

    template_name = "profiles/password-reset-done.html"


class ResetPasswordConfirmView(PasswordResetConfirmView):
    """Представление регистрации нового пароля пользователя."""

    template_name = "profiles/password-reset-confirm.html"
    success_url = reverse_lazy("profiles:password_reset_complete")


class ResetPasswordCompleteView(PasswordResetCompleteView):

    template_name = "profiles/password-reset-complete.html"


class LoginUserView(LoginView):
    """Представление авторизации пользователя."""

    form_class = AuthenticationForm
    template_name = "profiles/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        """Перенаправляем пользователя при успешной авторизации"""

        return reverse_lazy("profiles:page_test")


class RegisterView(CreateView):
    """Представление регистрации пользователя на сайте"""

    form_class = RegisterUserForm
    form = RegisterUserForm()
    template_name = "profiles/registration-user-form.html"

    def form_valid(self, form):
        response = super().form_valid(form)

        Profile.objects.create(user=self.object)  # создаем профиль пользователя

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(request=self.request, user=user)

        return response

    def get_success_url(self):
        return reverse_lazy("profiles:page_test")
