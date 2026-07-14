from .category import Category
from .product import Product


def main() -> None:
    """
    Точка входа в приложение ItemNest: демонстрация работы системы учёта товаров и категорий.

    Сценарий работы:
      * создаются несколько объектов Product (товары) с разными характеристиками;
      * создаются категории Category и в них добавляются товары;
      * демонстрируется функционал слияния товаров через Product.new_product_with_merge:
          - обновление количества при совпадении имени;
          - выбор максимальной цены;
          - создание нового товара, если дубликата нет;
      * проверяется логика изменения цены (подтверждение при понижении, запрет на нулевые/отрицательные значения);
      * выводятся отчёты по категориям (список товаров, количество, суммарная стоимость);
      * показывается глобальная статистика (счётчики категорий и товаров).

    Особенности:
      * перед началом работы сбрасываются счётчики Category.category_count и Category.product_count
        для чистоты эксперимента при повторных запусках;
      * для демонстрации слияния используется временный список существующих товаров (existing_products_list);
      * предусмотрена защита от ошибки EOFError при вызове input() в средах, где ввод недоступен
        (например, некоторые CI/CD или IDE без консоли).

    Примеры ожидаемого поведения:
        * при попытке понизить цену выводится запрос подтверждения (y/n);
        * при установке отрицательной цены выводится предупреждение, значение не меняется;
        * при добавлении дубликата товара через new_product_with_merge количество суммируется,
          а цена устанавливается как максимум из старой и новой.
    """

    Category.category_count = 0
    Category.product_count = 0

    print("=== Создание товаров (Product) ===")
    p1 = Product("Ноутбук X1", "16 ГБ ОЗУ, 512 ГБ SSD", 75000.50, 10)
    p2 = Product("Мышь беспроводная", "Эргономичная, Bluetooth", 2500.00, 50)
    p3 = Product("Клавиатура механическая", "RGB подсветка", 8900.99, 25)
    p4 = Product('Монитор 27"', "4K, IPS матрица", 35000.00, 8)

    print(f"Товар: {p1.name}")
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
    print("ТЕСТ ЗАДАЧИ 4: слияние товаров и логика цены")
    print("=" * 60)

    existing_products_list = [p1, p2, p3]  #
    p5_data = {
        "name": "Мышь беспроводная",
        "description": "Новая ревизия, улучшенный сенсор",
        "price": 3000.00,
        "quantity": 20,
    }

    print("\n--- Попытка добавить дубликат (Мышь беспроводная) ---")
    p5 = Product.new_product_with_merge(p5_data, existing_products_list)

    print(f"Результат: товар '{p5.name}' обновлён.")
    print(f"  Новое количество: {p5.quantity} шт. (было 50)")
    print(f"  Новая цена: {p5.price:.2f} руб. (была 2500.00, взята максимальная)")

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

    print("\n--- Проверка логики изменения цены (понижение) ---")
    current_price = p1.price
    print(f"Текущая цена '{p1.name}': {current_price:.2f} руб.")

    try:
        p1.price = 50000.00
    except EOFError:

        print(
            "[INFO] В этой среде input() недоступен, пропуск интерактивного теста цены."
        )

    print("\n--- Проверка запрета нулевой/отрицательной цены ---")
    old_price = p6.price
    p6.price = -100.0
    print(
        f"Цена после попытки установить -100: {p6.price:.2f} руб. (должна остаться прежней: {old_price:.2f})"
    )

    print(f"\nФинальный отчёт по товарам в категории '{electronics.name}':")
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
        f"\nОбщая стоимость товаров в категории '{electronics.name}': {formatted_value} ₽"
    )


if __name__ == "__main__":
    main()
