from comments.models import Comment
from django.contrib.auth.models import User
from django.test import TestCase
from products.models import Product


class CommentModelTestCase(TestCase):
    """Класс тестов модели Comment."""

    fixtures = [
        "fixtures/01-user-fixtures.json",
        "fixtures/03-products-fixtures.json",
        "fixtures/05-category-fixtures.json",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=2)
        cls.product = Product.objects.get(pk=1)
        cls.comment = Comment.objects.create(author=cls.user, product=cls.product, text="Хороший товар")

        cls.text = "Хороший товар"

    @classmethod
    def tearDownClass(cls):
        cls.comment.delete()

    def test_correct_add_comment(self):
        """Проверяем работу добавления записи в таблицу отзывов о продукте."""

        new_test_comment = Comment.objects.create(author=self.user, product=self.product, text=self.text)

        self.assertEqual(self.text, new_test_comment.text)
        self.assertTrue(Product.objects.filter(comments=new_test_comment).exists())
        self.assertTrue(User.objects.filter(comments=new_test_comment).exists())

    def test_method_get_number_comments(self):
        """Тестируем работу метода получения количества отзывов для товара."""

        count = Comment.get_number_comments(product_pk=1)

        self.assertEqual(count, 1)

    def test_method_glist_comments(self):
        """Тестируем работу метода получения список отзывов к товару."""

        first_query = Comment.objects.filter(product=self.product)
        second_query = Comment.get_list_comments(product_pk=1)

        self.assertQuerySetEqual(first_query, second_query)
