from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView, LogoutView,
)
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, DetailView

from config import settings
from .forms import RegisterUserForm, EmailAuthenticationForm, ProfileUpdateForm
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
    success_url = reverse_lazy("profiles:profile")

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


class MyLogoutView(LogoutView):
    """ Представление для разлогинивания пользователя"""
    next_page = reverse_lazy("profiles:login")


class ProfileDetailView(DetailView):
    """ Представление для редактирования страницы личного кабинета пользователя"""

    form_class = ProfileUpdateForm
    model = User
    template_name = "profiles/profile-update-form.jinja2"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_data = Profile.objects.get(user=self.object)
        context = ProfileUpdateForm(instance=self.object,
                                    initial={"data": profile_data})
        if request.method == "POST":
            form = ProfileUpdateForm(request.POST)
            with transaction.atomic():
                if form.is_valid():
                    # user = form.save()
                    avatar = form.cleaned_data.get("avatar")
                    name = form.cleaned_data.get("name")
                    phone = form.cleaned_data.get("phone")
                    email = form.cleaned_data.get("email")
                    # if Profile.regex_phone[phone]:
                    Profile.objects.update(
                        user=self.object.pk,
                        avatar=avatar,
                        name=name,
                        phone=phone,
                        email=email
                    )
                    # else:
                    #     messages.warning(request, 'Ошибка ввода данных. Номер телефона указан неверно')

                    password = form.cleaned_data.get('password', "")
                    password_check = form.cleaned_data.get('password_check', "")
                    if password == password_check:
                        username = form.cleaned_data.get('username')
                        user = authenticate(username=username, password=password)
                        login(request, user)
                        messages.success(request, "Данные успешно сохранены!")
                    else:
                        messages.warning(request, 'Ошибка ввода данных. Пароли не совпадают')
                    return redirect('profile', pk=self.object.pk)
                else:
                    print(form.errors)
        else:
            form = ProfileUpdateForm()
            return render(request, 'profiles/profile-update-form.jinja2', {'form': form})
        return context

    def post(self, request):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

    def get_success_url(self):
        return reverse_lazy("profiles:profile", kwargs={"pk": self.object.pk})

    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     user_form = context['form']
    #     # avatar = context['avatar']
    #     with transaction.atomic():
    #         if all([form.is_valid(), user_form.is_valid()]):
    #             user_form.save()
    #             form.save()
    #         else:
    #             context.update({'form': user_form})
    #             return self.render_to_response(context)
    #     return super(ProfileUpdateView, self).form_valid(form)
