import pytest

from src.category import Category
from src.product import Product


class TestProduct:

    def test_product_initialization_sets_all_attributes(self) -> None:
        p = Product("Ноутбук X1", "16 ГБ ОЗУ", 75000.50, 10)
        assert p.name == "Ноутбук X1"
        assert p.description == "16 ГБ ОЗУ"
        assert p.price == 75000.50
        assert p.quantity == 10

    def test_price_is_private_attribute(self) -> None:
        p = Product("Товар", "Описание", 100.0, 5)
        assert not hasattr(p, "__price")
        assert hasattr(p, "_Product__price")

    def test_price_getter_returns_value(self) -> None:
        p = Product("Товар", "Описание", 99.99, 3)
        assert p.price == 99.99

    def test_price_setter_accepts_positive_value_and_updates(self) -> None:
        p = Product("Товар", "Описание", 100.0, 5)
        p.price = 200.0
        assert p.price == 200.0

    def test_price_setter_rejects_non_positive_values( self, capsys: pytest.CaptureFixture[str]) -> None:
        p = Product("Товар", "Описание", 100.0, 5)
        old_price = p.price

        p.price = -10.0
        assert p.price == old_price

        p.price = 0.0
        assert p.price == old_price

        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out

    def test_price_setter_does_not_return_value(self) -> None:
        p = Product("Товар", "Описание", 100.0, 5)
        p.price = 150.0
        assert p.price == 150.0

    def test_add_two_products_returns_total_value(self) -> None:
        a = Product("A", "Desc", 10.0, 2)  # 20
        b = Product("B", "Desc", 5.0, 3)  # 15
        result = a + b
        assert result == 35.0

    def test_add_with_non_product_returns_not_implemented(self) -> None:
        p = Product("A", "Desc", 10.0, 2)
        result = p.__add__("string")
        assert result is NotImplemented

    def test_new_product_from_dict(self) -> None:
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

    def test_merge_existing_product_updates_quantity_and_price(self) -> None:
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
        existing = [Product("Товар", "Описание", 1000.0, 10)]

        lower_data = {"name": "Товар", "price": 900.0, "quantity": 5}
        Product.new_product_with_merge(lower_data, existing)
        assert existing[0].price == 1000.0

        higher_data = {"name": "Товар", "price": 1100.0, "quantity": 5}
        Product.new_product_with_merge(higher_data, existing)
        assert existing[0].price == 1100.0


class TestCategory:

    @pytest.fixture(autouse=True)
    def reset_counters(self) -> None:
        Category.category_count = 0
        Category.product_count = 0
        yield

    def test_category_initialization_sets_name_and_description(self) -> None:
        cat = Category("Электроника", "Устройства")
        assert cat.name == "Электроника"
        assert cat.description == "Устройства"

    def test_products_list_is_private(self) -> None:
        cat = Category("Тестовая", "Описание")
        assert not hasattr(cat, "__products")
        assert hasattr(cat, "_Category__products")

    def test_category_count_increases_on_init(self) -> None:
        assert Category.category_count == 0
        Category("Cat1", "Desc1")
        assert Category.category_count == 1
        Category("Cat2", "Desc2")
        assert Category.category_count == 2

    def test_add_product_accepts_self_and_product(self) -> None:
        cat = Category("Тестовая", "Описание")
        p = Product("Товар", "Описание", 100.0, 10)
        cat.add_product(p)
        assert cat.product_quantity == 1

    def test_add_product_uses_append_to_add_to_private_list(self) -> None:
        cat = Category("Тестовая", "Описание")
        p1 = Product("Товар1", "Описание1", 100.0, 10)
        p2 = Product("Товар2", "Описание2", 200.0, 5)
        cat.add_product(p1)
        cat.add_product(p2)
        assert cat.product_quantity == 2
        products_list = getattr(cat, "_Category__products")
        assert len(products_list) == 2
        assert products_list[0] is p1
        assert products_list[1] is p2

    def test_add_product_does_not_return_value(self) -> None:
        cat = Category("Тестовая", "Описание")
        p = Product("Товар", "Описание", 100.0, 10)
        cat.add_product(p)
        assert cat.product_quantity == 1
        products_list = getattr(cat, "_Category__products")
        assert products_list[0] is p

    def test_add_product_increments_product_count(self) -> None:
        assert Category.product_count == 0
        cat1 = Category("Cat1", "Desc1")
        cat2 = Category("Cat2", "Desc2")

        p1 = Product("Товар1", "Описание1", 100.0, 10)
        p2 = Product("Товар2", "Описание2", 200.0, 5)

        cat1.add_product(p1)
        assert Category.product_count == 1

        cat2.add_product(p2)
        assert Category.product_count == 2

    def test_add_product_raises_type_error_for_non_product(self) -> None:
        cat = Category("Тестовая", "Описание")
        with pytest.raises(TypeError):
            cat.add_product("не продукт")

    def test_products_getter_is_property(self) -> None:
        cat = Category("Тестовая", "Описание")
        result = cat.products
        assert isinstance(result, str)

    def test_products_getter_name_is_products(self) -> None:
        cat = Category("Тестовая", "Описание")
        assert hasattr(cat, "products")

    def test_products_getter_returns_string(self) -> None:
        cat = Category("Тестовая", "Описание")
        p1 = Product("Товар1", "Описание1", 100.0, 10)
        p2 = Product("Товар2", "Описание2", 200.0, 5)
        cat.add_product(p1)
        cat.add_product(p2)

        report = cat.products
        assert isinstance(report, str)
        assert "Товар1" in report
        assert "Товар2" in report

    def test_products_getter_format_matches_template(self) -> None:
        cat = Category("Тестовая", "Описание")
        p1 = Product("Товар1", "Описание1", 100.0, 10)
        p2 = Product("Товар2", "Описание2", 200.0, 5)
        cat.add_product(p1)
        cat.add_product(p2)

        report = cat.products
        lines = report.splitlines(keepends=True)  # сохраняем \n
        assert len(lines) == 2

        expected_line1 = f"{p1.name}, {p1.price:.0f} руб. Остаток: {p1.quantity} шт.\n"
        expected_line2 = f"{p2.name}, {p2.price:.0f} руб. Остаток: {p2.quantity} шт.\n"

        assert lines[0] == expected_line1
        assert lines[1] == expected_line2

    def test_products_getter_returns_empty_string_if_no_products(self) -> None:
        cat = Category("Пустая", "Описание")
        assert cat.products == ""

    def test_total_value_calculates_correctly(self) -> None:
        cat = Category("Тестовая", "Описание")
        p1 = Product("Товар1", "Описание1", 100.0, 10)  # 1000
        p2 = Product("Товар2", "Описание2", 200.0, 5)  # 1000
        cat.add_product(p1)
        cat.add_product(p2)

        assert cat.total_value() == 2000.0

    def test_str_representation_of_category(self) -> None:
        cat = Category("Электроника", "Описание")
        p1 = Product("Товар1", "Описание1", 100.0, 10)
        p2 = Product("Товар2", "Описание2", 200.0, 5)
        cat.add_product(p1)
        cat.add_product(p2)

        result = str(cat)
        total_quantity = p1.quantity + p2.quantity
        expected = f"Электроника, количество продуктов: {total_quantity} шт."
        assert result == expected
