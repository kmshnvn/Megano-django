from django.db.models import Count
from django.template.response import TemplateResponse
from django.test import TestCase, Client
from products.models import Product


class CatalogListViewTest(TestCase):
    fixtures = [
        "fixtures/03-products-fixtures.json",
        "fixtures/04-shop-fixtures.json",
        "fixtures/05-category-fixtures.json",
        "fixtures/011-offers-fixtures.json",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.page_url = "http://127.0.0.1:8000/shops/catalog/"
        cls.products = Product.objects.prefetch_related("category", "offers")
        cls.data = {"price": "5;500"}

    def test_get_method(self):
        """Тест ответа GET-запроса страницы."""

        response = self.client.get(self.page_url)

        self.assertEqual(200, response.status_code),
        self.assertIn("shops/catalog.jinja2", response.template_name)

    def test_post_method_without_params(self):
        """Тест ответа POST-запроса страницы, без передачи дополнительных параметров."""

        response: TemplateResponse = self.client.post(self.page_url)
        query = response.context_data["object_list"]

        self.assertEqual(200, response.status_code)
        self.assertIn("shops/catalog.jinja2", response.template_name)
        self.assertQuerySetEqual(self.products, query, ordered=False)

    def test_filter_products_by_title_param(self):
        """
        Тест работы фильтра продукции на странице.
        Получения корректных, при фильтрации по полю - Название.
        """

        self.data["title"] = "Лопата"

        response = self.client.post(self.page_url, data=self.data)
        query = self.products.filter(name__icontains="Лопата").filter(offers__price__range=(5, 500))
        query_response = response.context_data["products"]

        self.assertQuerySetEqual(query, query_response, ordered=False)

    def test_get_price_error(self):
        """Тест отображения ошибки в шаблоне, форма фильтрации товаров."""

        self.data["price"] = "5;f"

        text_error = "Ошибка формы фильтр, поле - цена"
        response = self.client.post(self.page_url, self.data)

        self.assertIn(text_error, response.context_data["form"].errors["price"])

    def test_sort_by_price(self):
        """Тест отображения товаров сортированных по стоимости."""

        sort_price_url = self.page_url + "sort/price/"

        response = self.client.get(sort_price_url)
        query = self.products.order_by("offers__price")

        self.assertQuerySetEqual(query, response.context_data["products"])

    def test_sort_by_comments(self):
        """Тест отображения товаров сортированных по отзывам."""

        sort_price_url = self.page_url + "sort/comments/"

        response = self.client.get(sort_price_url)
        query = self.products.annotate(count=Count("comments")).order_by("count")

        self.assertQuerySetEqual(query, response.context_data["products"])
