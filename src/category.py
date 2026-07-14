from typing import List

from .product import Product


class Category:
    """
    Класс Category—категория товаров в системе учёта интернет‑магазина ItemNest.

    Обеспечивает:
      * группировку товаров по категориям;
      * инкапсулированное хранение списка товаров (через приватный атрибут `__products`);
      * контролируемое добавление товаров через метод `add_product`;
      * подсчёт количества категорий (`category_count`) и общего количества товаров (`product_count`);
      * формирование текстового отчёта по товарам через свойство `products`;
      * расчёт суммарной стоимости товаров категории через метод `total_value`.

    Примеры использования:
        >>> cat = Category("Электроника", "Устройства и гаджеты")
        >>> p = Product("Мышь", "Беспроводная", 2500.0, 50)
        >>> cat.add_product(p)
        >>> print(cat.products)
        Мышь, 2500 руб. Остаток: 50 шт.
        <BLANKLINE>
        >>> cat.product_quantity
        1
        >>> cat.total_value()
        125000.0
    """

    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str) -> None:
        """
        Создать новую категорию товаров.

        При инициализации:
          * создаётся приватный список товаров `self.__products`;
          * устанавливаются атрибуты `name` и `description`;
          * увеличивается глобальный счётчик категорий `Category.category_count`.

        Параметры
        ---------
        name : str
            Название категории.
        description : str
            Описание категории.
        """
        self.__products: List[Product] = []
        self.name = name
        self.description = description
        Category.category_count += 1

    def add_product(self, product: Product) -> None:
        """
        Добавить товар в категорию.

        Выполняет валидацию типа и обновляет внутренние состояния:
          * проверяет, что `product`—экземпляр класса `Product`;
          * добавляет товар в приватный список `self.__products`;
          * увеличивает глобальный счётчик товаров `Category.product_count`.

        Метод не возвращает значение (возвращает ``None``).

        Параметры
        ---------
        product : Product
            Товар, который нужно добавить в категорию.

        Raises
        ------
        TypeError
            Если переданный объект не является экземпляром класса `Product`.
        """
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product.")

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """
        Получить текстовый отчёт по всем товарам категории.

        Возвращает строку, где каждый товар представлен в формате:
            `"{name}, {price:.0f} руб. Остаток: {quantity} шт.\n"`

        Если в категории нет товаров, возвращается пустая строка.

        Возвращает
        ----------
        str
            Отчёт по товарам категории (каждый товар на отдельной строке).
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
        """
        Получить количество товаров в данной категории.

        Возвращает
        ----------
        int
            Число товаров, добавленных в категорию.
        """
        return len(self.__products)

    def total_value(self) -> float:
        """
        Рассчитать общую стоимость всех товаров в категории.

        Стоимость вычисляется как сумма произведений цены на количество
        для каждого товара в категории: `sum(price * quantity)`.

        Возвращает
        ----------
        float
            Суммарная стоимость товаров категории.
        """
        return sum(p.price * p.quantity for p in self.__products)
