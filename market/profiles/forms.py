from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms import models
from django.utils.translation import gettext_lazy as _

from profiles.models import Profile


class RegisterUserForm(UserCreationForm):
    """Форма регистрации пользователя"""

    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password1",
            "password2",
            "group",
            "email",
        )

    def clean_email(self):
        """Проверка email на уникальность"""

        email = self.cleaned_data.get("email").strip()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(_("Такая почта уже зарегистрированная"))

        return email


class EmailAuthenticationForm(forms.Form):
    """Форма аутентификации пользователя с помощью email"""

    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

    def clean(self):
        user = self.authenticate_email()
        if not user:
            raise forms.ValidationError(_("Вы ввели не корректные данные."))
        else:
            self.user = user
        return self.cleaned_data

    def authenticate_user(self):
        """Аутентификации пользователя"""

        return authenticate(username=self.user.email, password=self.cleaned_data.get("password"))

    def authenticate_email(self):
        """Возвращает объект пользователя, если он аутентифицирован, иначе None"""

        email = self.cleaned_data.get("email", None)
        if email:
            try:
                user = User.objects.get(email__iexact=email)  # получаем объект пользователя по email
                if user.check_password(self.cleaned_data.get("password", "")):
                    return user
            except ObjectDoesNotExist:
                return None
        return None


class ProfileUpdateForm(models.ModelForm):
    """
    Форма обновления данных профиля пользователя
    """
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    avatar = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "Profile-file form-input",
                                      "id": "avatar",
                                      "name": "avatar",
                                      "type": "file",
                                      "data-validate": "onlyImgAvatar"}),
        required=False,
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-input",
                                      "id": "name",
                                      "value": "",
                                      "type": "text",
                                      "data-validate": "require"}),
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-input",
                                      "id": "phone",
                                      "name": "phone",
                                      "type": "text",
                                      "value": "+70000000000"}),
        validators=[Profile.regex_phone],
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-input",
                                      "id": "mail",
                                      "name": "mail",
                                      "type": "text",
                                      "value": "send@test.test",
                                      "data-validate": "require"})
    )
    password = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-input",
                                      "id": "password",
                                      "name": "password",
                                      "type": "password",
                                      "value": "send@test.test",
                                      "placeholder": "Тут можно изменить пароль"}),
        required=False,
    )
    password_check = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-input",
                                      "id": "password_check",
                                      "name": "password_check",
                                      "type": "password",
                                      "placeholder": "Введите пароль повторно"}),
        required=False,
    )
