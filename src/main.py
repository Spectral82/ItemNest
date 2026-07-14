from src.category import Category
from src.product import Product


def main() -> None:
    # Сброс счётчиков для чистоты эксперимента (если запускаешь несколько раз подряд)
    Category.category_count = 0
    Category.product_count = 0

    print("=== Создание товаров (Product) ===")
    p1 = Product("Ноутбук X1", "16 ГБ ОЗУ, 512 ГБ SSD", 75000.50, 10)
    p2 = Product("Мышь беспроводная", "Эргономичная, Bluetooth", 2500.00, 50)
    p3 = Product("Клавиатура механическая", "RGB подсветка", 8900.99, 25)
    p4 = Product("Монитор 27\"", "4K, IPS матрица", 35000.00, 8)

    print(f"Товар: {p1.name}")
    print(f"  Цена: {p1.price:.2f} ₽")
    print(f"  Количество: {p1.quantity} шт.")

    print("\n=== Создание категорий (Category) ===")
    electronics = Category(
        name="Электроника",
        description="Различные электронные устройства и аксессуары",
        products=[p1, p2, p3]   # 3 карточки товаров
    )

    displays = Category(
        name="Мониторы и ТВ",
        description="Дисплеи разных размеров и разрешений",
        products=[p4]           # 1 карточка товара
    )

    print(f"\nКатегория: {electronics.name}")
    print(f"Описание: {electronics.description}")
    print(f"Количество карточек товаров в категории: {len(electronics.products)}")

    print(f"\nКатегория: {displays.name}")
    print(f"Количество карточек товаров: {len(displays.products)}")

    print("\n=== Глобальная статистика (атрибуты класса) ===")
    print(f"Всего категорий создано: {Category.category_count}")

    # Теперь это именно длина списков: 3 + 1 = 4 (карточки товаров)
    print(f"Всего товаров (карточек): {Category.product_count}")

    # Дополнительная проверка: расчёт общей стоимости категории (не влияет на счётчики)
    total_value = sum(item.price * item.quantity for item in electronics.products)
    print(f"\nОбщая стоимость товаров в категории '{electronics.name}': {total_value:,.2f} ₽".replace(",", " ").replace(".", ","))


if __name__ == "__main__":
    main()
