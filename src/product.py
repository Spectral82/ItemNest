from abc import ABC, abstractmethod
from typing import List


class LoggingInitMixin:
    """Миксин для логирования: выводит в консоль имя класса и аргументы."""

    def __init__(self, *args, **kwargs) -> None:
        cls = self.__class__

        if kwargs:
            kwargs_repr = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
            print(f"{cls.__name__}({kwargs_repr})")
        else:
            args_repr = ", ".join(repr(a) for a in args)
            print(f"{cls.__name__}({args_repr})")

        super().__init__(*args, **kwargs)


class BaseProduct(ABC):
    """Абстрактный базовый класс товара: обязательные свойства и базовые операции."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Название товара."""
        pass

    @property
    @abstractmethod
    def price(self) -> float:
        """Цена за единицу товара."""
        pass

    @property
    @abstractmethod
    def quantity(self) -> int:
        """Количество единиц товара на складе."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Строковое представление товара в читаемом формате."""
        pass

    def total_cost(self) -> float:
        """Возвращает общую стоимость товара (цена × количество)."""
        return self.price * self.quantity

    def __add__(self, other: "BaseProduct") -> float:
        """Складывает общую стоимость двух товаров одного класса."""
        if not isinstance(other, BaseProduct):
            return NotImplemented

        if type(self) != type(other):
            raise TypeError(
                f"Нельзя складывать товары разных классов: "
                f"{type(self).__name__} и {type(other).__name__}. "
                "Сложение разрешено только для одинаковых классов товаров."
            )

        return self.total_cost() + other.total_cost()


class Product(LoggingInitMixin, BaseProduct):
    """Базовый класс товара с валидацией цены и количества."""

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        """Инициализирует товар с проверкой корректности цены и количества.

        ВАЖНО: по требованию задания при попытке создать товар с quantity == 0
        выбрасывается ValueError, прерывая создание экземпляра.
        """
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")

        self._name = name
        self.description = description
        self.__price: float = 0.0
        self.price = price
        self._quantity = quantity

    @property
    def name(self) -> str:
        """Возвращает название товара."""
        return self._name

    @property
    def price(self) -> float:
        """Возвращает текущую цену товара."""
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
        """Устанавливает цену, если она положительная."""
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        self.__price = value

    @property
    def quantity(self) -> int:
        """Возвращает текущее количество товара."""
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        """Устанавливает количество, если оно неотрицательное.

        Обратите внимание: этот сеттер НЕ запрещает quantity == 0,
        потому что запрет на ноль действует только при создании (__init__).
        После создания товара количество может уменьшаться вплоть до 0.
        """
        if value < 0:
            print("Количество не может быть отрицательным")
            return
        self._quantity = value

    def __str__(self) -> str:
        """Читаемое представление: «Название, X руб. Остаток: X шт.»"""
        return f"{self.name}, {self.price:.0f} руб. Остаток: {self.quantity} шт."

    @classmethod
    def new_product(cls, data: dict) -> "Product":
        """Создаёт товар из словаря с данными (name, description, price, quantity)."""
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
        """Обновляет существующий товар по имени или создаёт новый."""
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
    """Товар типа «смартфон» с характеристиками: модель, память, цвет и т.д."""

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
        """Инициализирует смартфон, передавая базовые параметры в родительский класс."""
        super().__init__(name, description, price, quantity)
        self.model = model
        self.efficiency = efficiency
        self.memory = memory
        self.color = color

    def __str__(self) -> str:
        """Читаемое представление смартфона с техническими характеристиками."""
        return (
            f"{self.name} ({self.model}), {self.color}, "
            f"память: {self.memory} ГБ, производительность: {self.efficiency:.1f}, "
            f"{self.price:.0f} руб., остаток: {self.quantity} шт."
        )


class LawnGrass(Product):
    """Товар типа «газонная трава» с агрономическими характеристиками."""

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
        """Инициализирует газонную траву, передавая параметры в родительский класс."""
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self) -> str:
        """Читаемое представление газонной травы с агрономическими параметрами."""
        return (
            f"{self.name}, цвет: {self.color}, страна: {self.country}, "
            f"срок прорастания: {self.germination_period} дней, "
            f"{self.price:.0f} руб., остаток: {self.quantity} шт."
        )
