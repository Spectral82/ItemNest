from .category import Category
from .product import Product


def main() -> None:
    """Точка входа в демонстрационное приложение ItemNest.

    Выполняет полный сценарий работы интернет‑магазина:
      * сбрасывает счётчики категорий и товаров для чистой демонстрации;
      * создаёт тестовые товары и категории;
      * демонстрирует добавление товаров в категории;
      * проверяет логику слияния товаров (new_product_with_merge):
          - обновление количества при совпадении имени;
          - выбор максимальной цены;
      * тестирует валидацию цены (запрет нулевых/отрицательных значений);
      * показывает работу строковых представлений (__str__) для Product и Category;
      * выводит отчёт по товарам через свойство products;
      * отображает глобальную статистику (category_count, product_count);
      * рассчитывает и выводит суммарную стоимость товаров в категории;
      * детально демонстрирует работу магического метода __add__ для Product,
        включая пошаговую формулу расчёта общей стоимости на складе.
    """
    # Сбрасываем счётчики для чистой демонстрации
    Category.category_count = 0
    Category.product_count = 0

    print("=== Создание товаров (Product) ===")
    p1 = Product("Ноутбук X1", "16 ГБ ОЗУ, 512 ГБ SSD", 75000.50, 10)
    p2 = Product("Мышь беспроводная", "Эргономичная, Bluetooth", 2500.00, 50)
    p3 = Product("Клавиатура механическая", "RGB подсветка", 8900.99, 25)
    p4 = Product('Монитор 27"', "4K, IPS матрица", 35000.00, 8)

    print(f"Товар: {p1}")
    print(f"  Цена: {p1.price:.2f} ₽")
    print(f"  Количество: {p1.quantity} шт.")

    print("\n=== Создание категорий (Category) ===")
    electronics = Category(
        name="Электроника", description="Различные электронные устройства и аксессуары"
    )

    displays = Category(
        name="Мониторы и ТВ", description="Дисплеи разных размеров и разрешений"
    )

    electronics.add_product(p1)
    electronics.add_product(p2)
    electronics.add_product(p3)
    displays.add_product(p4)

    print(f"\nКатегория: {electronics.name}")
    print(f"Описание: {electronics.description}")
    print(f"Количество карточек товаров в категории: {electronics.product_quantity}")

    print(f"\nОтчёт по товарам в категории '{electronics.name}':")
    report = electronics.products
    if report:
        print(report, end="")
    else:
        print("(товаров нет)")

    print("\n" + "=" * 60)
    print("ТЕСТ ЗАДАЧИ: слияние товаров и логика цены")
    print("=" * 60)

    existing_products_list = [p1, p2, p3]

    p5_data = {
        "name": "Мышь беспроводная",
        "description": "Новая ревизия, улучшенный сенсор",
        "price": 3000.00,
        "quantity": 20,
    }

    print("\n--- Попытка добавить дубликат (Мышь беспроводная) ---")
    p5 = Product.new_product_with_merge(p5_data, existing_products_list)
    print(f"Результат: товар '{p5.name}' обновлён.")
    print(f"  Новое количество: {p5.quantity} шт. (было 50 + 20)")
    print(f"  Новая цена: {p5.price:.2f} руб. (взята максимальная)")

    p6_data = {
        "name": "Веб‑камера HD",
        "description": "1080p, встроенный микрофон",
        "price": 4500.00,
        "quantity": 30,
    }

    print("\n--- Попытка добавить новый товар (Веб‑камера HD) ---")
    p6 = Product.new_product_with_merge(p6_data, existing_products_list)
    print(f"Результат: создан новый товар '{p6.name}'.")

    electronics.add_product(p6)

    print("\n--- Проверка запрета нулевой/отрицательной цены ---")
    old_price = p6.price
    p6.price = -100.0
    print(
        f"Цена после попытки установить -100: {p6.price:.2f} руб. "
        f"(должна остаться прежней: {old_price:.2f})"
    )

    print("\n" + "-" * 60)
    print("ДЕМОНСТРАЦИЯ __str__")
    print("-" * 60)

    print(f"\nstr(p1): {p1}")
    print(f"str(electronics): {electronics}")
    print(f"str(displays): {displays}")

    print(
        f"\nФинальный отчёт по товарам в категории '{electronics.name}' "
        "(через products):"
    )
    final_report = electronics.products
    if final_report:
        print(final_report, end="")
    else:
        print("(товаров нет)")

    print(f"\nКатегория: {displays.name}")
    print("Отчёт по товарам:")
    report_displays = displays.products
    if report_displays:
        print(report_displays, end="")
    else:
        print("(товаров нет)")

    print("\n=== Глобальная статистика (атрибуты класса) ===")
    print(f"Всего категорий создано: {Category.category_count}")
    print(f"Всего товаров (карточек): {Category.product_count}")

    total_value = electronics.total_value()
    formatted_value = f"{total_value:,.2f}".replace(",", " ").replace(".", ",")
    print(
        f"\nОбщая стоимость товаров в категории '{electronics.name}': "
        f"{formatted_value} ₽"
    )

    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ МАГИЧЕСКОГО МЕТОДА __add__ ДЛЯ PRODUCT")
    print("=" * 60)

    a = Product("Ноутбук X1", "16 ГБ ОЗУ, 512 ГБ SSD", 75000.50, 10)
    b = Product("Мышь беспроводная", "Эргономичная, Bluetooth", 2500.00, 50)

    print("\nПример расчёта суммы стоимости двух товаров:")
    print(f"Ноутбук X1: цена = {a.price} руб., количество = {a.quantity} шт.")
    print(
        f"Мышь беспроводная: цена = {b.price} руб., " f"количество = {b.quantity} шт."
    )
    print()
    print("Логика сложения (a + b):")
    print(
        f"  Стоимость Ноутбук X1 на складе = {a.price} × {a.quantity} = "
        f"{a.price * a.quantity}"
    )
    print(
        f"  Стоимость Мышь беспроводная на складе = {b.price} × {b.quantity} = "
        f"{b.price * b.quantity}"
    )
    print()
    result = a + b
    print(
        "  Итоговая сумма (Общее количество Ноутбук Х1 + Общее количество "
        f"Мышь беспроводная) = {a.price * a.quantity} + {b.price * b.quantity} "
        f"= {result}"
    )
    print()
    print("Формула, которую реализует метод __add__:")
    print("  result = (self.price * self.quantity) + " "(other.price * other.quantity)")
    print()
    print(f"В коде это работает как: a + b = {result}")

    print("\nЕщё один пример на реальных товарах из категории 'Электроника':")
    x = p1  # Ноутбук
    y = p2  # Мышь
    sum_xy = x + y
    print(
        f"{x.name}: {x.price:.0f} руб × {x.quantity} шт = "
        f"{x.price * x.quantity:.0f}"
    )
    print(
        f"{y.name}: {y.price:.0f} руб × {y.quantity} шт = "
        f"{y.price * y.quantity:.0f}"
    )
    print(f"Сумма (x + y) = {sum_xy:.0f} руб.")


if __name__ == "__main__":
    main()
