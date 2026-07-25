from abc import ABC, abstractmethod
from typing import List


class LoggingInitMixin:
    """
    Простой и надёжный миксин для логирования.
    Выводит в консоль конструктор объекта с аргументами.
    ВАЖНО: чтобы в логе были красивые названия параметров (name=..., price=...),
    создавай объекты, передавая аргументы по именам.
    """

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
    """Абстрактный базовый класс для всех продуктов."""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def price(self) -> float:
        pass

    @property
    @abstractmethod
    def quantity(self) -> int:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    def total_cost(self) -> float:
        return self.price * self.quantity

    def __add__(self, other: "BaseProduct") -> float:
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
    """Основной класс товара."""

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        self._name = name
        self.description = description
        self.__price: float = 0.0
        self.price = price
        self._quantity = quantity

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        self.__price = value

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        if value < 0:
            print("Количество не может быть отрицательным")
            return
        self._quantity = value

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
        Если товара нет — создаёт и возвращает новый экземпляр.

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
