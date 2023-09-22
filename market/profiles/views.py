from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, FormView, TemplateView

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


class ProfileDetailView(TemplateView):
    """ Представление для редактирования страницы личного кабинета пользователя"""

    model = User
    template_name = "profiles/profile-update-form.jinja2"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data = {"profile": Profile.objects.get(user=self.request.user)}
        data['form'] = UserForm(instance=self.request.user,
                                initial={"avatar": data['profile'].avatar,
                                         "phone": data['profile'].phone,
                                         "name": User.get_full_name(self.request.user)
                                         })

        return data

    def post(self, request):
        form = UserForm(request.POST)
        with transaction.atomic():
            if form.is_valid():
                form.save()
                avatar = form.cleaned_data.get('avatar')
                phone = form.cleaned_data.get('phone')
                name = form.cleaned_data.get('name')
                email = form.cleaned_data.get('email')
                Profile.objects.filter(user=self.request.user).update(
                    avatar=avatar,
                    phone=phone,
                )
                User.objects.filter(id=self.request.user.id).update(
                    first_name=name.split()[0],
                    last_name=name.split()[1],
                    email=email,
                )
                # password = form.cleaned_data.get('password')
                # password_check = form.cleaned_data.get('password_check')
                # if password == password_check and password != "":
                #     username = form.cleaned_data.get('username')
                #     user = authenticate(username=username, password=password)
                #     login(request, user)
                #     form.save()
                #     messages.success(request, _('Ваш профиль был успешно обновлен!'))
                # else:
                #     messages.warning(request, _('Ошибка ввода данных. Пароли не совпадают'))
                # return redirect('profiles:profile')
            else:
                data = self.get_context_data()
                UserForm(instance=request.user, initial=data)
        return render(request, 'profiles/profile-update-form.jinja2', {
            'form': form,
        })
