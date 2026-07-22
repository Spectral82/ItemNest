from typing import List


class Product:
    """Товар в интернет‑магазине.

    Предоставляет хранение основных характеристик товара, валидацию цены,
    создание из словаря, слияние с существующими товарами и базовые операции.
    """

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        """Инициализирует товар с заданными параметрами.

        Устанавливает название, описание и количество напрямую.
        Для цены используется сеттер с валидацией: значение должно быть положительным.

        Args:
            name: Название товара.
            description: Описание товара.
            price: Цена товара (должна быть > 0).
            quantity: Количество единиц товара на складе.
        """
        self.name = name
        self.description = description
        self.__price: float = 0.0
        self.price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Возвращает текущую цену товара.

        Returns:
            Цена товара в рублях.
        """
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
        """Устанавливает новую цену товара с валидацией.

        Цена должна быть строго больше нуля. Если передано значение <= 0,
        цена не обновляется, а в stdout выводится сообщение об ошибке.

        Args:
            value: Новое значение цены.
        """
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        self.__price = value

    def __add__(self, other: "Product") -> float:
        """Вычисляет суммарную стоимость двух товаров на складе.

        Сложение разрешено только между объектами ОДНОГО И ТОГО ЖЕ класса.
        Проверка осуществляется через type(self) == type(other).
        Если классы различаются, выбрасывается TypeError.

        Результат равен сумме произведений цены на количество для обоих товаров:
        (self.price * self.quantity) + (other.price * other.quantity).

        Если other не является экземпляром Product, возвращается NotImplemented.

        Args:
            other: Другой объект Product для сложения.

        Returns:
            Суммарная стоимость двух товаров в рублях.

        Raises:
            TypeError: Если self и other — экземпляры разных классов (например, Smartphone и LawnGrass).
        """
        if not isinstance(other, Product):
            return NotImplemented

        if type(self) != type(other):
            raise TypeError(
                f"Нельзя складывать товары разных классов: "
                f"{type(self).__name__} и {type(other).__name__}. "
                "Сложение разрешено только для одинаковых классов товаров."
            )

        return (self.price * self.quantity) + (other.price * other.quantity)

    def __str__(self) -> str:
        """Возвращает читаемое строковое представление товара.

        Формат: «Название товара, X руб. Остаток: X шт.».

        Returns:
            Строковое представление товара.
        """
        return f"{self.name}, {self.price:.0f} руб. Остаток: {self.quantity} шт."

    @classmethod
    def new_product(cls, data: dict) -> "Product":
        """Создаёт новый объект Product из словаря с данными.

        Ожидаемый формат словаря:
        {
            "name": str,
            "description": str,
            "price": float,
            "quantity": int
        }

        Args:
            data: Словарь с параметрами товара.

        Returns:
            Новый экземпляр Product.
        """
        return cls(
            name=data["name"],
            description=data["description"],
            price=data["price"],
            quantity=data["quantity"],
        )

    @classmethod
    def new_product_with_merge(
        cls, data: dict, existing_products: List["Product"]
    ) -> "Product":
        """Пытается обновить существующий товар или создать новый.

        Если товар с таким именем уже есть в списке existing_products,
        увеличивает его количество и обновляет цену (если новая цена выше).
        Если товара нет — создаёт и возвращает новый экземпляр.

        Args:
            data: Словарь с данными о товаре (name, price, quantity, description).
            existing_products: Список уже существующих объектов Product.

        Returns:
            Обновлённый существующий товар либо новый экземпляр Product.
        """
        name = data["name"]
        for prod in existing_products:
            if prod.name == name:
                prod.quantity += data["quantity"]
                new_price = data["price"]
                if new_price > prod.price:
                    prod.price = new_price
                return prod
        return cls.new_product(data)


class Smartphone(Product):
    """Смартфон — специализированный товар с дополнительными характеристиками."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        model: str,
        efficiency: float,
        memory: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.model = model
        self.efficiency = efficiency
        self.memory = memory
        self.color = color

    def __str__(self) -> str:
        return (
            f"{self.name} ({self.model}), {self.color}, "
            f"память: {self.memory} ГБ, производительность: {self.efficiency:.1f}, "
            f"{self.price:.0f} руб., остаток: {self.quantity} шт."
        )


class LawnGrass(Product):
    """Газонная трава — специализированный товар с агрономическими характеристиками."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self) -> str:
        return (
            f"{self.name}, цвет: {self.color}, страна: {self.country}, "
            f"срок прорастания: {self.germination_period} дней, "
            f"{self.price:.0f} руб., остаток: {self.quantity} шт."
        )
