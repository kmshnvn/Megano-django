from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    LogoutView,
)
from django.db import transaction
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView
from django.utils.translation import gettext_lazy as _

from config import settings
from .forms import RegisterUserForm, EmailAuthenticationForm, UserForm
from .models import Profile


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


class LoginEmailView(FormView):
    """Представление авторизации пользователя."""

    form_class = EmailAuthenticationForm
    template_name = "profiles/login.jinja2"
    success_url = reverse_lazy("shops:main-page")

    def dispatch(self, request, *args, **kwargs):
        """Если пользователь авторизован, делаем редирект"""

        if self.request.user.is_authenticated:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.authenticate_user()
        login(self.request, user)  # авторизация

        return super().form_valid(form)


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


class ProfileLogoutView(LogoutView):
    next_page = reverse_lazy("profiles:login")


class ProfileDetailView(LoginRequiredMixin, TemplateView):
    """Представление для редактирования страницы личного кабинета пользователя"""

    model = User
    template_name = "profiles/profile.jinja2"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.get(user=self.request.user)
        context["form"] = UserForm(
            instance=self.request.user,
            initial={
                "avatar": context["profile"].avatar,
                "phone": context["profile"].phone,
            },
        )
        return context

    def post(self, request: HttpRequest) -> HttpResponse:
        form = UserForm(instance=self.request.user, data=request.POST, files=request.FILES)

        if form.is_valid():
            with transaction.atomic():
                avatar = form.cleaned_data.get("avatar")
                phone = form.cleaned_data.get("phone")
                Profile.objects.filter(user=self.request.user).update(
                    avatar=avatar,
                    phone=phone,
                )
                #
                # FIXME Сброс пароля реализован выше - смотри представления ResetPassword. Поэтому поля для
                # FIXME нужно удалить из формы
                #
                # username = form.cleaned_data.get("username")
                # password1 = form.cleaned_data.get("password1")
                # password2 = form.cleaned_data.get("password2")
                # if password1 == password2:
                #     user = authenticate(username=username, password=password1)
                #     login(request, user)
                #     messages.success(request, _("Пароль успешно обновлен"))
                #     return redirect('profiles:profile')
                # else:
                #     if password1 != password2:
                #         messages.success(request, _("Пароли не совпадают. Попробуйте снова."))
                #         return redirect('profiles:profile')
                form.save()
                messages.success(request, _("Данные успешно обновлены"))
                return redirect("profiles:profile")

        else:
            print(form.errors)

        context = self.get_context_data()
        return render(request, "profiles/profile.jinja2", context=context)
