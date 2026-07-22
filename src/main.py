from .category import Category
from .product import LawnGrass, Product, Smartphone


def main() -> None:
    """Точка входа в демонстрационное приложение ItemNest.

    Выполняет полный сценарий работы интернет‑магазина, включая:
      * сброс счётчиков для чистой демонстрации;
      * создание базовых товаров и категорий;
      * демонстрацию добавления товаров в категории;
      * проверку логики слияния товаров (new_product_with_merge);
      * валидацию цены;
      * работу строковых представлений (__str__) для Product и Category;
      * отчёты по товарам и глобальную статистику;
      * расчёт суммарной стоимости товаров в категории;
      * демонстрацию магического метода __add__ для Product (с ограничением по классам);
      * демонстрацию специализированных товаров: Smartphone и LawnGrass;
      * тесты защиты add_product: запрет на добавление нетоваров и посторонних объектов.
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

    print("\nПример расчёта суммы стоимости двух товаров (одинаковый класс Product):")
    result = a + b
    print(f"a + b = {result:.0f} руб.")

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

    # ==========================================================================
    # ДЕМОНСТРАЦИЯ СПЕЦИАЛИЗИРОВАННЫХ ТОВАРОВ (Smartphone и LawnGrass)
    # ==========================================================================
    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ СПЕЦИАЛИЗИРОВАННЫХ ТОВАРОВ")
    print("=" * 60)

    phone = Smartphone(
        name="Смартфон UltraX",
        description="Флагманский смартфон с камерой 200 МП",
        price=89990.0,
        quantity=15,
        model="UltraX Pro",
        efficiency=9.8,
        memory=256,
        color="графитовый",
    )
    print(f"\n{phone}")

    grass = LawnGrass(
        name="Трава газонная GreenLawn",
        description="Смесь для быстрого озеленения",
        price=1200.0,
        quantity=50,
        country="Россия",
        germination_period=7,
        color="ярко-зелёная",
    )
    print(f"{grass}")

    print(f"\nСмартфон - это уникальный проукт? {isinstance(phone, Product)}")
    print(f"Трава - это уникальный продукт? {isinstance(grass, Product)}")

    electronics.add_product(phone)
    displays.add_product(grass)

    print("\nОтчёт по категории 'Электроника' (теперь включает смартфон):")
    print(electronics.products, end="")

    print("\nОтчёт по категории 'Мониторы и ТВ' (теперь включает газонную траву):")
    print(displays.products, end="")

    print("\n=== Обновлённая глобальная статистика ===")
    print(f"Всего категорий создано: {Category.category_count}")
    print(f"Всего товаров (карточек): {Category.product_count}")

    new_total_value_electronics = electronics.total_value()
    formatted_new_value = f"{new_total_value_electronics:,.2f}".replace(
        ",", " "
    ).replace(".", ",")
    print(
        f"\nОбновлённая общая стоимость товаров в категории '{electronics.name}': "
        f"{formatted_new_value} ₽"
    )

    # ==========================================================================
    # ТЕСТ НОВОЙ ЛОГИКИ СЛОЖЕНИЯ: только одинаковые классы
    # ==========================================================================
    print("\n" + "=" * 60)
    print("ТЕСТ: сложение товаров РАЗНЫХ классов (должно вызвать ошибку)")
    print("=" * 60)

    try:
        total_mixed = phone + grass  # phone — Smartphone, grass — LawnGrass
        print(f"Суммарная стоимость (неожиданно): {total_mixed}")
    except TypeError as e:
        print("Перехвачена ожидаемая ошибка:")
        print(e)

    print("\nТест: сложение товаров ОДНОГО класса (должно работать)")
    phone2 = Smartphone(
        name="Смартфон UltraX Mini",
        description="Компактная версия",
        price=79990.0,
        quantity=10,
        model="UltraX Mini",
        efficiency=9.5,
        memory=128,
        color="серебристый",
    )
    total_same = phone + phone2
    print(f"Суммарная стоимость двух смартфонов: {total_same:.0f} руб.")

    grass2 = LawnGrass(
        name="Трава газонная GreenLawn Extra",
        description="Улучшенная смесь",
        price=1300.0,
        quantity=40,
        country="Россия",
        germination_period=6,
        color="изумрудная",
    )
    total_grass_same = grass + grass2
    print(f"Суммарная стоимость двух видов травы: {total_grass_same:.0f} руб.")

    # ==========================================================================
    # ТЕСТ ЗАЩИТЫ add_product (issubclass / isinstance)
    # ==========================================================================
    print("\n" + "=" * 60)
    print("ТЕСТ: ЗАЩИТА МЕТОДА add_product")
    print("=" * 60)

    print("\n--- Тест: попытка добавить обычную строку вместо товара ---")
    try:
        electronics.add_product("Просто строка вместо товара")
    except TypeError as e:
        print("Перехвачена ожидаемая ошибка:")
        print(e)

    print("\n--- Тест: попытка добавить произвольный объект (FakeItem) ---")

    class FakeItem:
        pass

    fake = FakeItem()
    try:
        electronics.add_product(fake)
    except TypeError as e:
        print("Ещё одна ожидаемая ошибка:")
        print(e)

    print("\n--- Тест: попытка добавить словарь вместо товара ---")
    try:
        electronics.add_product({"name": "Плохой товар", "price": 100})
    except TypeError as e:
        print("Ожидаемая ошибка для словаря:")
        print(e)

    print(
        "\n--- Тест: добавление корректного наследника (Smartphone) — должно пройти ---"
    )
    phone3 = Smartphone(
        name="Смартфон TestPhone",
        description="Тестовый смартфон",
        price=50000.0,
        quantity=5,
        model="TestModel",
        efficiency=8.5,
        memory=128,
        color="чёрный",
    )
    electronics.add_product(phone3)
    print("Успешно добавлен ещё один смартфон!")
    print(
        f"Теперь товаров в категории 'Электроника': {electronics.product_quantity} шт."
    )

    print("\nФинальный отчёт по категории 'Электроника':")
    print(electronics.products, end="")

    final_total = electronics.total_value()
    formatted_final = f"{final_total:,.2f}".replace(",", " ").replace(".", ",")
    print(
        f"\nИтоговая стоимость товаров в категории '{electronics.name}': "
        f"{formatted_final} ₽"
    )


if __name__ == "__main__":
    main()
