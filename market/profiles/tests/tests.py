from django.test import TestCase, Client

from django.contrib.auth.models import User
from django.urls import reverse


class ProfileTestCase(TestCase):
    """Тест представления детальной страницы товара"""

    fixtures = [
        "fixtures/01-user-fixtures.json",
        "fixtures/02-profile-fixtures.json",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.page_url = reverse("profiles:profile")
        cls.user = User.objects.get(pk=8)

    def test_get_method(self):
        """Тест ответа GET-запроса страницы"""

        response = self.client.get(self.page_url)
        self.assertEqual(200, response.status_code),
        self.assertIn("profiles/profile.jinja2", response.template_name)

    def test_post_method(self):
        """Тест ответа POST-запроса страницы"""

        response = self.client.post(self.page_url)
        query = response.context_data["object_list"]

        self.assertEqual(200, response.status_code)
        self.assertIn("profiles/profile.jinja2", response.template_name)
        self.assertQuerySetEqual(self.user, query, ordered=False)
