from typing import Dict, Any, List


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if hasattr(self, "_Product__price"):
            old_price = self.price
            if value < old_price:
                confirm = input(f"Цена понижается с {old_price:.2f} до {value:.2f}. Подтвердить (y/n)? ")
                if confirm.lower() != "y":
                    print("Изменение цены отменено.")
                    return

        self.__price = value

    @classmethod
    def new_product(cls, data: Dict[str, Any]) -> "Product":
        """Создаёт продукт из словаря (без проверки на дубли)."""
        return cls(
            name=data["name"],
            description=data["description"],
            price=data["price"],
            quantity=data["quantity"],
        )

    @classmethod
    def new_product_with_merge(
        cls, data: Dict[str, Any], existing_products: List["Product"]
    ) -> "Product":
        """
        Создаёт товар из словаря. Если товар с таким именем уже есть в existing_products,
        то вместо создания нового объекта:
          - суммирует количество (старое + новое)
          - выбирает максимальную цену из старой и новой.
        Возвращает найденный (обновлённый) или новый объект.
        """
        name = data["name"]

        for prod in existing_products:
            if prod.name == name:
                prod.quantity += data["quantity"]

                new_price = data["price"]
                if new_price > prod.price:
                    prod.price = new_price
                if new_price > prod.price:
                    prod.__price = new_price

                return prod

        return cls.new_product(data)