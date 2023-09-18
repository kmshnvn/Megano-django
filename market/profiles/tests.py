from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.test import TestCase, Client
from profiles.models import Profile


class ProfileViewTestCase(TestCase):
    fixtures = [
        "fixtures/01-user-fixtures.json",
        "fixtures/010-user-group-fixtures.json",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=2)
        cls.user_password = "admin27admin"

        cls.log_page = "http://127.0.0.1:8000/profile/login/"
        cls.reg_page = "http://127.0.0.1:8000/profile/registration/"

        cls.register_data = {
            "username": "test_name",
            "email": "test_email@email.com",
            "password1": "password1test",
            "password2": "password1test",
            "group": 1,
        }

    def setUp(self):
        self.client = Client()

    def test_get_login_page(self):
        response: TemplateResponse = self.client.get(self.log_page)

        self.assertEqual(200, response.status_code)
        self.assertIn("profiles/login.jinja2", response.template_name)

    def test_login_redirect(self):
        data = {
            "email": self.user.email,
            "password": self.user_password,
        }
        response: HttpResponseRedirect = self.client.post(self.log_page, data=data)

        self.assertEqual(302, response.status_code)
        self.assertEqual("/", response.url)

    def test_login_with_username(self):
        data = {
            "email": self.user.username,
            "password": self.user_password,
        }
        response: TemplateResponse = self.client.post(self.log_page, data=data)

        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context_data["form"].is_valid())

    def test_get_register_user_page(self):
        response: TemplateResponse = self.client.get(self.reg_page)

        self.assertEqual(200, response.status_code)
        self.assertIn("profiles/registr.jinja2", response.template_name)

    def test_register_user_profile(self):
        response: HttpResponseRedirect = self.client.post(self.reg_page, data=self.register_data)

        self.assertEqual(302, response.status_code)
        self.assertEqual("/profile/login/", response.url)

        self.assertTrue(User.objects.filter(email="test_email@email.com").exists())
        self.assertTrue(Profile.objects.filter(user__username="test_name").exists())

    def test_register_not_correct_email(self):
        self.register_data["email"] = "test_email@email"
        response: TemplateResponse = self.client.post(self.reg_page, data=self.register_data)

        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context_data["form"].is_valid())

    def test_register_not_correct_password(self):
        self.register_data["password2"] = "password2test"
        response: TemplateResponse = self.client.post(self.reg_page, data=self.register_data)

        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context_data["form"].is_valid())

    def test_register_without_group_password(self):
        self.register_data["group"] = ""
        response: TemplateResponse = self.client.post(self.reg_page, data=self.register_data)

        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context_data["form"].is_valid())


class ProfileModelTestCase(TestCase):
    fixtures = [
        "fixtures/01-user-fixtures.json",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=2)

        cls.data = {
            "user": cls.user,
            "address": "Test address",
            "phone": "+79882666636",
            "balance": 0,
        }

    def test_create_profile(self):
        profile = Profile.objects.create(**self.data)

        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.phone, self.data["phone"])
