from django.contrib.auth import authenticate, login
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.db import transaction
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegisterUserForm, EmailAuthenticationForm
from .models import Profile
from market.config import settings


class ResetPasswordView(PasswordResetView):
    """Представление формы сброса пароля."""

    from_email = settings.EMAIL_HOST_USER
    template_name = "profiles/password-reset-form.jinja2"
    email_template_name = "profiles/email/password-reset-email.html"
    subject_template_name = "profiles/email/password_reset_subject.txt"
    success_url = reverse_lazy("profiles:password_reset_done")


class ResetPasswordDoneView(PasswordResetDoneView):
    """Представление вывода информации об успешной отправки ссылки для смены пароля."""

    template_name = "profiles/password-reset-done.jinja2"


class ResetPasswordConfirmView(PasswordResetConfirmView):
    """Представление регистрации нового пароля пользователя."""

    template_name = "profiles/password-reset-confirm.jinja2"
    success_url = reverse_lazy("profiles:password_reset_complete")


class ResetPasswordCompleteView(PasswordResetCompleteView):
    """Представление для вывода информации об успешной смени пароля"""

    template_name = "profiles/password-reset-complete.jinja2"


def email_login_view(request: HttpRequest) -> HttpResponse:
    """Представление авторизации пользователя."""

    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("/admin/")
        return render(request,
                      "profiles/login.jinja2",
                      {"form": EmailAuthenticationForm()}
                      )

    form = EmailAuthenticationForm(request.POST)

    if request.method == "POST" and form.is_valid():
        user = form.authenticate_user()
        login(request, user)  # авторизация

        return HttpResponseRedirect("/admin/")

    return render(
        request,
        "profiles/login.jinja2",
        {"form": form}
    )


class RegisterView(CreateView):
    """Представление регистрации пользователя на сайте"""

    form_class = RegisterUserForm
    template_name = "profiles/registr.jinja2"
    success_url = reverse_lazy("profiles:login")

    def form_valid(self, form):
        with transaction.atomic():
            response = super().form_valid(form)
            Profile.objects.create(user=self.object)  # создаем профиль пользователя

            username = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request=self.request, user=user)

        return response
