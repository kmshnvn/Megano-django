import os
import shutil
import sys
import uuid
from typing import Dict, List

import requests
from urllib.request import urlopen
import yaml
from PIL import Image

from django.db import transaction
from django.core.management.base import BaseCommand
from products.models import Category, Product, Detail, ProductDetail
from shops.models import Shop, Offer


class Command(BaseCommand):
    """
    Класс, реализует импорт товаров магазина из файла yaml и добавляет в БД
    """

    def add_arguments(self, parser) -> None:
        """
        Берет аргумент названия файла из командной строки, если есть.

        :param parser: объект парсера аргументов командной строки
        :return: None
        """
        parser.add_argument("--file", required=False)

    def create_product_and_offer(
        self,
        product_name: str,
        description: str,
        image_path: str,
        category: str,
        params: Dict[str, str],
        shop: Shop,
        price: float,
        remainder: int,
    ) -> None:
        """
        Создает запись о продукте и предложении в базе данных.

        :param product_name: Название продукта
        :param description: Описание продукта
        :param image_path: Уникальное имя изображения
        :param category: Категория продукта
        :param params: Параметры продукта
        :param shop: Магазин, к которому относится продукт
        :param price: Цена продукта
        :param remainder: Остаток продукта
        :return: None
        """
        try:
            with transaction.atomic():
                param_text = ""

                product = Product.objects.create(
                    name=product_name,
                    description=description,
                    preview=f"products/preview/{image_path}",
                    image=f"products/image/{image_path}",
                    category=category,
                )

                # Проход по параметрам продукта
                for param_name, param_value in params.items():
                    detail, created = Detail.objects.get_or_create(name=param_name)
                    ProductDetail.objects.create(
                        product=product,
                        detail=detail,
                        value=param_value,
                        category=category,
                    )
                    param_text += f"Создал характеристику товара: {param_name}\n"

                Offer.objects.create(
                    shop=shop,
                    product=product,
                    price=price,
                    remainder=remainder,
                )

                self.stdout.write(f'Создал товар: Артикул {product.pk} - "{product_name}"')
                self.stdout.write(f"{param_text}")
                self.stdout.write(self.style.SUCCESS(f"Создал предложение товара: {product_name}"))

        except Exception as e:
            self.stderr.write(f"Ошибка при создании товара: {e}")

    def create_image_paths(self, image_url: str, shop_id: int, offer_id: str) -> str:
        """
        Загружает изображение по указанной URL, сохраняет его на сервере и возвращает уникальное имя файла.

        :param image_url: URL изображения
        :param shop_id: Идентификатор магазина
        :param offer_id: Идентификатор товара
        :return: Уникальное имя файла изображения или пустая строка, если произошла ошибка
        """
        try:
            response = requests.get(image_url)

            if response.status_code == 200:
                unique_filename = f"{shop_id}_{offer_id}_{str(uuid.uuid4())[:7]}.webp"
                img_path = f"media/products/image/{unique_filename}"
                prev_path = f"media/products/preview/{unique_filename}"

                img = Image.open(urlopen(image_url))
                prev = img

                img.save(img_path, format="WEBP")
                prev.thumbnail(size=(300, 300))
                prev.save(prev_path, format="WEBP")

                return unique_filename

        except requests.exceptions.HTTPError as e:
            self.stderr.write(f"Ошибка HTTP при загрузке изображения: {e}")
        except requests.exceptions.RequestException as e:
            self.stderr.write(f"Ошибка запроса при загрузке изображения: {e}")
        except Exception as e:
            self.stderr.write(f"Ошибка при загрузке изображения: {e}")
        return ""

    def check_required_fields(self, offer_data: Dict) -> List[str]:
        """
        Проверяет, что обязательные поля данных о товаре присутствуют.

        :param offer_data: Данные о товаре
        :return: Список отсутствующих обязательных полей или пустой список, если все поля присутствуют
        """
        required_fields = ["name", "description", "image", "category", "price", "count", "params"]
        missing_variables = [field for field in required_fields if not offer_data.get(field)]
        return missing_variables

    def check_shop_id(self, shop_id: str):
        """
        Проверяет наличие ID магазина и его существование в базе данных.

        :param shop_id: Идентификатор магазина
        :return: Объект магазина (Shop) или None, если ID магазина отсутствует или магазин не найден
        """
        if shop_id is None:
            self.stderr.write("Не указан ID магазина")

        try:
            shop_query = Shop.objects.get(id=shop_id)
            return shop_query
        except Shop.DoesNotExist:
            self.stderr.write(
                f"Магазина с ID {shop_id} еще нет в нашей базе. Создайте магазин или укажите правильный ID"
            )
        except Exception as e:
            self.stderr.write(f"Возникла ошибка при получении магазина: {e}")

    def import_file(self, file_path: str) -> None:
        """
        Импортирует данные из файла YAML и добавляет товары и предложения в базу данных.

        :param file_path: Путь к файлу YAML
        :return: None
        """
        with open(file_path, "r") as yaml_file:
            data = yaml.safe_load(yaml_file)

        shop = data.get("yml_catalog").get("shop")
        shop_id = shop.get("shopID")

        shop_query = self.check_shop_id(shop_id)
        if shop_query is None:
            return

        offers = shop.get("offers")

        if offers:
            category_list = [elem for elem in Category.objects.filter(parent__isnull=False)]

            for offer_id, offer_data in offers.items():
                product_name = offer_data.get("name")
                description = offer_data.get("description")
                image_url = offer_data.get("image")
                category = offer_data.get("category")
                price = offer_data.get("price")
                remainder = offer_data.get("count")
                params = offer_data.get("params")

                missing_variables = self.check_required_fields(offer_data)
                if missing_variables:
                    error_message = (
                        f"Нужно добавить следующие значения в импорт товара "
                        f"{offer_id}: {', '.join(missing_variables)}"
                    )
                    self.stderr.write(error_message)
                    continue

                category_name = [elem for elem in category_list if elem.name in category.split("/")]

                if len(category_name) > 1:
                    self.stderr.write("Должна быть только 1 категория у товара")
                    continue
                elif category_name:
                    category_name = category_name[0]
                    self.stdout.write(f"Получил категорию товара - {category_name}")
                else:
                    self.stderr.write(f"Категория товара {offer_id} не относится к существующей")
                    continue

                unique_filename = self.create_image_paths(image_url, shop_id, offer_id)

                shop_product_query = Offer.objects.filter(shop=shop_id).filter(product__name=product_name)
                if not shop_product_query:
                    self.create_product_and_offer(
                        product_name=product_name,
                        description=description,
                        image_path=unique_filename,
                        category=category_name,
                        params=params,
                        shop=shop_query,
                        price=price,
                        remainder=remainder,
                    )
                else:
                    self.stderr.write(f'Товар "{product_name}" уже есть в вашем списке')
                    continue

    def handle(self, *args, **options):
        """
        Обработчик команды. Импортирует данные из файлов YAML и добавляет товары и предложения в базу данных.

        :param args: Позиционные аргументы
        :param options: Опциональные аргументы
        :return: None
        """
        try:
            folder_path = "import_data/to_import"
            success_folder = "import_data/success"
            error_folder = "import_data/failed"

            args = options["file"]

            yaml_files = [filename for filename in os.listdir(folder_path) if filename.endswith(".yaml")]
            if args:
                if args in yaml_files:
                    yaml_files = [args]
                else:
                    self.stderr.write(f"Файл {args} не найден")
                    sys.exit(1)

            for filename in yaml_files:
                file_path = os.path.join(folder_path, filename)
                self.import_file(file_path)
                shutil.move(file_path, os.path.join(success_folder, filename))

        except Exception as e:
            shutil.move(file_path, os.path.join(error_folder, filename))
            self.stderr.write(f"Ошибка при выполнении команды: {e}")
