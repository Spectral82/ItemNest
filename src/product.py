class Product:
    """
    Класс товара.

    Свойства (через self):
        name (str): название товара
        description (str): описание
        price (float): цена в рублях (с копейками)
        quantity (int): количество в штуках
    """

    def __init__(self, name: str, description: str, price: float, quantity: int):
        # Простая валидация
        if price < 0:
            raise ValueError("Цена не может быть отрицательной.")
        if quantity < 0:
            raise ValueError("Количество не может быть отрицательным.")

        self.name: str = name
        self.description: str = description
        self.price: float = price  # рубли (float — чтобы были копейки)
        self.quantity: int = quantity  # штуки (int)
