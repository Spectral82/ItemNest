from typing import List

from .product import Product


class Category:
    """
    Класс категории товаров.

    Атрибуты класса (общие для всех объектов):
        category_count (int): сколько всего категорий создано
        product_count (int): сколько всего карточек товаров во всех категориях

    Атрибуты экземпляра (через self):
        name (str): название категории
        description (str): описание категории
        products (List[Product]): список объектов товаров
    """

    # Объявление атрибутов класса — они существуют до создания любых объектов
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        # Сохраняем параметры как атрибуты ЭКЗЕМПЛЯРА (уникальные для каждой категории)
        self.name: str = name
        self.description: str = description
        self.products: List[Product] = products

        # Обновляем атрибуты КЛАССА (общие счётчики)
        Category.category_count += 1

        # Считаем длину списка товаров (количество карточек), как требовалось
        items_in_this_category = len(self.products)
        Category.product_count += items_in_this_category
