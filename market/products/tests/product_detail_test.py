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
    Category
)


class ProductDetailTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.product = Product.objects.create(
            name="Product for test",
        )
        cls.detail = Detail.objects.create(name="test_detail")
        cls.category = Category.objects.create(name="test_category")
        cls.product_detail = ProductDetail.objects.create(
            value="Test_detail", category_id=cls.category.pk, detail_id=cls.detail.pk, product_id=cls.product.pk
        )
        cls.shop = Shop.objects.create(name="Test_shop")
        cls.offer = Offer.objects.create(price=1200, product_id=cls.product.pk, shop_id=cls.shop.pk)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.product_detail.delete()
        cls.offer.delete()
        cls.shop.delete()
        cls.detail.delete()
        cls.category.delete()
        cls.product.delete()

    def test_product_detail(self) -> None:
        response = self.client.get(reverse("products:product_detail", kwargs={"pk": self.product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product-detail.jinja2")
        self.assertEqual(self.product.name, "Product for test")
        self.assertEqual(self.detail.name, "test_detail")
        self.assertEqual(self.category.name, "test_category")
        self.assertEqual(self.product_detail.value, "Test_detail")
        self.assertContains(response, self.offer.price)
