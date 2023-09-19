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
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView, TemplateView
from django.utils.translation import gettext_lazy as _


from config import settings
from .forms import RegisterUserForm, EmailAuthenticationForm, UserForm, ProfileForm
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

    # form_class = ProfileUpdateForm
    model = User
    template_name = "profiles/profile-update-form.jinja2"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        profile_data = {
            'profile': Profile.objects.get(user=self.request.user),
            'name': User.get_full_name(self.request.user),
            'user': User.objects.select_related('Profile')
        }
        for e, v in data.items():
            print(e, v)

        profile_data['user_form'] = UserForm(instance=self.request.user, initial=profile_data)
        profile_data['profile_form'] = ProfileForm(instance=self.request.user, initial=profile_data)

        return profile_data

    def post(self, request):
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        with transaction.atomic():
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                # data = {
                #     "avatar": profile_form.cleaned_data.get("avatar"),
                #     "name": user_form.cleaned_data.get("name"),
                #     "phone": profile_form.cleaned_data.get("phone"),
                #     "email": user_form.cleaned_data.get("email"),
                # }
                messages.success(request, _('Ваш профиль был успешно обновлен!'))
            else:
                user_form = UserForm(instance=request.user)
                profile_form = ProfileForm(instance=request.user.profile)
            return render(request, 'profiles/profile-update-form.jinja2', {
                'user_form': user_form,
                'profile_form': profile_form
            })

        # password = form.cleaned_data.get('password', "")
        # password_check = form.cleaned_data.get('password_check', "")
        #
        # if password == password_check:
        #     username = form.cleaned_data.get('username')
        #     user = authenticate(username=username, password=password)
        #     login(request, user)
        #     form.save()
        #     messages.success(request, _('Ваш профиль был успешно обновлен!'))
        #     return redirect('profiles:profile')
        # else:
        #     messages.warning(request, _('Ошибка ввода данных. Пароли не совпадают'))


        #
        # else:
        #     form = ProfileUpdateForm()
        #     return render(request, 'profiles/profile-update-form.jinja2', {'form': form})
