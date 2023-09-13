from django.test import TestCase
from django.urls import reverse


class HistoryViewTestCase(TestCase):
    """Тест представления истории просмотров товара"""

    def setUp(self) -> None:
        self.get_response = self.client.get(reverse(viewname="history:view_history"))

    def test_url_view_exist(self):
        response = self.client.get("/history/")
        self.assertEqual(response.status_code, 200)

    def test_url_view_correct_template(self):
        self.assertEqual(self.get_response.status_code, 200)
        self.assertTemplateUsed(self.get_response, "history/view-histroy.jinja2")
