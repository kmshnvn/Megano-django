from products.models import Product, ProductDetail, Detail, Category
from shops.models import Shop, Offer
from django.contrib.auth.models import User


def create_product():
    """Функция для создания продукта в БД для тестов"""

    return Product.objects.create(
        name="product_name",
        description="product_description",
        category=Category.objects.create(
            name="category_name",
            description="category_description",
        ),
    )


def create_offer(shop: Shop, product: Product):
    """Функция для создания предложения продукта в БД для тестов"""

    return Offer.objects.create(price=1200, product=product, shop=shop)


def create_shop():
    """Функция для создания магазина продукта в БД для тестов"""

    return Shop.objects.create(
        name="Test_shop",
    )


def create_user():
    """Функция для создания пользователя продукта в БД для тестов"""

    return User.objects.create_user(username="Test_name", email="test_email@mail.ru", password="test_password")


def crerate_product_detail(product: Product, detail: Detail, category: Category):
    """Функция для создания деталей продукта в БД для тестов"""

    return ProductDetail.objects.create(product=product, detail=detail, value="test_value", category=category)


def create_category():
    """Функция для создания категорий продуктов в БД для тестов"""

    return Category.objects.create(name="test_category")


def create_detail():
    """Функция для создания характеристик продукта в БД для тестов"""

    return Detail.objects.create(name="Test_detail1")
