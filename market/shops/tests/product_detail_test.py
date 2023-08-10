from django.test import TestCase
from django.urls import reverse
from shops.models import (
    Offer,
    Shop,
)
from products.models import (
    Product,
    ProductDetail,
    Detail,
)


class ProductDetailTestCase(TestCase):
    def setUp(self) -> None:
        self.product = Product.objects.create(
            name="Product for test",
        )
        self.detail = Detail.objects.create(name="test_detail")
        self.product_detail = ProductDetail.objects.create(
            value="Test_detail", detail_id=self.detail.pk, product_id=self.product.pk
        )
        self.shop = Shop.objects.create(name="Test_shop")
        self.offer = Offer.objects.create(price=1200, product_id=self.product.pk, shop_id=self.shop.pk)

    def tearDown(self) -> None:
        self.product_detail.delete()
        self.offer.delete()
        self.shop.delete()
        self.detail.delete()
        self.product.delete()

    def test_product_detail(self) -> None:
        response = self.client.get(reverse("products:product_detail", kwargs={"pk": self.product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product-detail.jinja2")
        self.assertEqual(self.product.name, "Product for test")
        self.assertEqual(self.detail.name, "test_detail")
        self.assertEqual(self.product_detail.value, "Test_detail")
        self.assertContains(response, self.offer.price)
