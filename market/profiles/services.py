from .models import BrowsingHistory


class HistoryService:
    @staticmethod
    def add_product_to_history(user, good):
        """
        Добавление товара в историю просмотров
        :param user:
        :param good:
        :return:
        """

        try:
            history_object = BrowsingHistory.objects.get(id=user, product_id=good)
            history_object.delete()
            BrowsingHistory.objects.create(id=user, product_id=good)
        except BrowsingHistory.DoesNotExist:
            BrowsingHistory.objects.create(id=user, product_id=good)

    @staticmethod
    def delete_viewed_product(user, good):
        """
        Удаление продукта из истории
        :param user:
        :param product:
        :return:
        """

        history_object = BrowsingHistory.objects.get(id=user, product_id=good)
        history_object.delete()

    def get_last_viewed(user):
        """
        Получение списка продуктов истории
        :return:
        """
        history_objects = BrowsingHistory.objects.filter(id=user).all()
        return history_objects
