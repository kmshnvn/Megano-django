from django.test import TestCase
from django.urls import reverse
from services_for_test.services_for_test import (
    create_shop,
    create_offer,
    create_product,
    create_detail,
    crerate_product_detail,
    create_category,
)


class ProductDetailTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.product = create_product()
        cls.category = create_category()
        cls.shop = create_shop(product=cls.product)
        cls.offer = create_offer(shop=cls.shop, product=cls.product)
        cls.detail = create_detail()
        cls.product_detail = crerate_product_detail(product=cls.product, detail=cls.detail, category=cls.category)

    def test_product_detail(self) -> None:
        response = self.client.get(reverse("products:product_detail", kwargs={"pk": self.product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product-detail.jinja2")
        self.assertEqual(self.product.name, "product_name")
        self.assertEqual(self.detail.name, "Test_detail1")
        self.assertEqual(self.category.name, "test_category")
        self.assertEqual(self.product_detail.value, "test_value")
        self.assertContains(response, self.offer.price)
