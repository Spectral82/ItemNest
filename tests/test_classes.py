import pytest

from src.category import Category
from src.product import Product


class TestProductInitialization:
    """Тесты для класса Product: инициализация, валидация, методы создания и слияния."""

    def test_product_initialization_sets_all_attributes(self) -> None:
        """
        Проверяет, что при создании Product корректно устанавливаются все атрибуты:
        name, description, price, quantity.
        """
        p = Product("Ноутбук X1", "16 ГБ ОЗУ", 75000.50, 10)
        assert p.name == "Ноутбук X1"
        assert p.description == "16 ГБ ОЗУ"
        assert p.price == 75000.50
        assert p.quantity == 10

    def test_product_price_and_quantity_types(self) -> None:
        """
        Проверяет типы атрибутов price (float) и quantity (int) после инициализации.
        """
        p = Product("Товар", "Описание", 100.0, 5)
        assert isinstance(p.price, float)
        assert isinstance(p.quantity, int)

    def test_price_setter_rejects_negative_values(self) -> None:
        """
        Проверяет, что установка отрицательной цены или нуля отклоняется:
        значение остаётся прежним.
        """
        p = Product("Тест", "Описание", 100.0, 10)
        p.price = -10.0  # должно отклонить
        assert p.price == 100.0
        p.price = 0.0
        assert p.price == 100.0

    def test_price_setter_accepts_positive_values(self) -> None:
        """
        Проверяет, что установка положительного значения цены корректно применяется.
        """
        p = Product("Тест", "Описание", 100.0, 10)
        p.price = 200.0
        assert p.price == 200.0

    def test_price_decrease_requires_confirmation(self, monkeypatch) -> None:
        """
        Проверяет логику подтверждения при снижении цены:
        * при вводе 'y' цена меняется;
        * при вводе 'n' цена остаётся прежней.
        Для имитации ввода используется monkeypatch.
        """
        p = Product("Тест", "Описание", 100.0, 10)

        # Имитируем подтверждение
        monkeypatch.setattr("builtins.input", lambda x: "y")
        p.price = 50.0
        assert p.price == 50.0

        # Имитируем отказ
        monkeypatch.setattr("builtins.input", lambda x: "n")
        p.price = 30.0
        assert p.price == 50.0

    def test_new_product_from_dict(self) -> None:
        """
        Проверяет создание товара через метод new_product из словаря.
        Убеждается, что все поля корректно извлекаются и устанавливаются.
        """
        data = {
            "name": "Продукт",
            "description": "Описание",
            "price": 500.0,
            "quantity": 15,
        }
        p = Product.new_product(data)
        assert p.name == "Продукт"
        assert p.price == 500.0
        assert p.quantity == 15

    def test_merge_existing_product(self) -> None:

        """
        Проверяет слияние нового товара с существующим:
        * количество суммируется;
        * цена обновляется на новую (в этом тесте она выше).
        """
        existing = [Product("Мышь", "Описание", 2500.0, 50)]
        new_data = {
            "name": "Мышь",
            "description": "Новое описание",
            "price": 3000.0,
            "quantity": 20,
        }
        merged = Product.new_product_with_merge(new_data, existing)
        assert merged.quantity == 70
        assert merged.price == 3000.0

    def test_merge_keeps_higher_price(self) -> None:
        """
        Проверяет правило выбора максимальной цены при слиянии:
        * если новая цена ниже — сохраняется старая;
        * если новая цена выше — устанавливается новая.
        """
        existing = [Product("Товар", "Описание", 1000.0, 10)]

        # Новая цена ниже
        lower_data = {"name": "Товар", "price": 900.0, "quantity": 5}
        Product.new_product_with_merge(lower_data, existing)
        assert existing[0].price == 1000.0

        # Новая цена выше
        higher_data = {"name": "Товар", "price": 1100.0, "quantity": 5}
        Product.new_product_with_merge(higher_data, existing)
        assert existing[0].price == 1100.0


class TestCategoryInitialization:
    """Тесты для класса Category: счётчики, добавление товаров, отчёты и расчёты."""

    @pytest.fixture(autouse=True)
    def reset_counters(self) -> None:
        """Сброс счётчиков Category.category_count и Category.product_count перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0
        yield

    def test_category_initialization_sets_all_attributes(self) -> None:

        """Проверяет, что при создании Category корректно устанавливаются name и description."""
        cat = Category("Электроника", "Устройства")
        assert cat.name == "Электроника"
        assert cat.description == "Устройства"

    def test_category_counters(self) -> None:
        """
        Проверяет корректность работы счётчиков категорий:
        каждый новый экземпляр увеличивает Category.category_count.
        """
        assert Category.category_count == 0
        assert Category.product_count == 0

        Category("Cat1", "Desc1")
        assert Category.category_count == 1

        Category("Cat2", "Desc2")
        assert Category.category_count == 2

    def test_add_product_method(self) -> None:
        """
        Проверяет метод add_product:
        * товар добавляется в категорию;
        * обновляются локальный счётчик product_quantity и глобальный Category.product_count.
        """
        cat = Category("Тестовая", "Описание")
        p = Product("Товар", "Описание", 100.0, 10)
        cat.add_product(p)
        assert cat.product_quantity == 1
        assert Category.product_count == 1

    def test_products_getter(self) -> None:
        """
        Проверяет свойство products:
        возвращает строку с отчётом по всем товарам в формате:
        'Название, X руб. Остаток: Y шт.\n'.
        """
        cat = Category("Тестовая", "Описание")
        p1 = Product("Товар1", "Описание1", 100.0, 10)
        p2 = Product("Товар2", "Описание2", 200.0, 5)
        cat.add_product(p1)
        cat.add_product(p2)

        report = cat.products
        expected = (
            "Товар1, 100 руб. Остаток: 10 шт.\n" "Товар2, 200 руб. Остаток: 5 шт.\n"
        )
        assert report == expected

    def test_total_value(self) -> None:
        """
        Проверяет метод total_value:
        корректно считает общую стоимость товаров в категории как сумму (цена × количество).
        """
        cat = Category("Тестовая", "Описание")
        p1 = Product("Товар1", "Описание", 100.0, 10)
        p2 = Product("Товар2", "Описание", 200.0, 5)
        cat.add_product(p1)
        cat.add_product(p2)

        assert cat.total_value() == 100 * 10 + 200 * 5  # 2000.0
