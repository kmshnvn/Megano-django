from django.test import TestCase
from profiles.models import Profile
from django.urls import reverse
from django.contrib.auth.models import User


class MakeOrderStepOneTestCase(TestCase):
    """
    Тест оформления заказа
    """

    fixtures = [
        "fixtures/01-user-fixtures.json",
        "fixtures/02-profile-fixtures.json",
        "fixtures/03-products-fixtures.json",
        "fixtures/05-category-fixtures.json",
        "fixtures/04-shop-fixtures.json",
        "fixtures/011-offers-fixtures.json",
    ]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.get(pk=2)
        cls.profile = Profile.objects.get(user=cls.user)
        cls.profile.balance = 9999

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_added_data(self) -> None:
        """
        Тест для добавления данных в сессии корзины и заказа
        :return: None
        """
        get_response = self.client.get(path="/order/step_1/")
        self.client.get(reverse("basket:add_product", kwargs={"product_pk": 33, "offer_pk": 3}))
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, "order/make-order-step1.jinja2")

        response = self.client.post(
            "/order/step_1/",
            data={
                "customer": "Штирлиц",
                "phone": "+79999999999",
                "email": "test@mail.ru",
            },
        )
        self.assertRedirects(response, expected_url="/order/step_2/")
        self.assertEqual(response.status_code, 302)

        response = self.client.post(
            "/order/step_2/",
            data={
                "delivery_type": "Обычная доставка",
                "address": "ул. Курганова, дом.54, кв.7",
                "city": "Брянск",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url="/order/step_3/")

        response = self.client.post(
            "/order/step_3/",
            data={
                "pay": "Онлайн картой",
            },
        )

        self.assertRedirects(response, expected_url="/order/step_4/")
        self.assertEqual(len(self.client.session.get("basket")), 1)
        self.assertEqual(len(self.client.session.get("order")), 3)
        self.assertEqual(response.status_code, 302)

    def test_error_page(self):
        """Тест для рендреа страницы ошибки оформления заказа"""

        response = self.client.get("/order/step_4/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Получено недостаточно данных для оформления заказа!")
        self.assertEqual(self.client.session.get("basket"), None)
        self.assertEqual(self.client.session.get("order"), {})
