from typing import List

from .product import Product


class Category:
    """Категория товаров в интернет‑магазине.

    Хранит список товаров, поддерживает подсчёт количества карточек товаров,
    расчёт суммарной стоимости и строковое представление категории.
    """

    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str) -> None:
        """Инициализирует категорию с заданным именем и описанием.

        При создании автоматически увеличивает счётчик созданных категорий
        (Category.category_count) на 1.

        Args:
            name: Название категории.
            description: Описание категории.
        """
        self.__products: List[Product] = []
        self.name = name
        self.description = description
        Category.category_count += 1

    def add_product(self, product: object) -> None:
        """Добавляет товар в категорию.

        Проверяет, что переданный объект является экземпляром класса Product
        или любого его наследника (например, Smartphone, LawnGrass).
        Для этого используются issubclass и isinstance.

        При успешном добавлении увеличивает глобальный счётчик товаров
        (Category.product_count) на 1.

        Args:
            product: Объект товара для добавления.

        Raises:
            TypeError: Если переданный объект не является экземпляром Product
                       или его наследника.
        """
        if not issubclass(type(product), Product):
            raise TypeError(
                f"Нельзя добавить объект типа {type(product).__name__} в категорию. "
                "Разрешены только объекты Product и его наследники."
            )

        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product.")

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Возвращает строковый отчёт по всем товарам в категории.

        Каждый товар форматируется как:
        «Название продукта, X руб. Остаток: X шт.\n».

        Если товаров нет, возвращается пустая строка.

        Returns:
            Строка с перечнем товаров категории.
        """
        if not self.__products:
            return ""
        lines = [
            f"{p.name}, {p.price:.0f} руб. Остаток: {p.quantity} шт.\n"
            for p in self.__products
        ]
        return "".join(lines)

    @property
    def product_quantity(self) -> int:
        """Возвращает количество карточек товаров в категории.

        Не суммирует остатки товаров, а считает число добавленных объектов Product.

        Returns:
            Количество товаров (карточек) в категории.
        """
        return len(self.__products)

    def total_value(self) -> float:
        """Вычисляет суммарную стоимость всех товаров в категории.

        Для каждого товара берётся произведение цены на количество,
        затем значения суммируются.

        Returns:
            Суммарная стоимость товаров категории в рублях.
        """
        return sum(p.price * p.quantity for p in self.__products)

    def __str__(self) -> str:
        """Возвращает читаемое строковое представление категории.

        Формат: «Название категории, количество продуктов: X шт.»,
        где X — суммарное количество штук всех товаров категории.

        Returns:
            Строковое представление категории.
        """
        total_quantity = sum(p.quantity for p in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."
