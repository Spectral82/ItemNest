import pytest

from src.category import Category
from src.product import BaseProduct, LawnGrass, Product, Smartphone


class TestProductInitializationAndValidation:
    """Инициализация, валидация quantity=0 (запрещено при создании), цена/количество."""

    def test_creation_with_zero_quantity_raises_value_error(self) -> None:
        with pytest.raises(ValueError) as exc_info:
            Product(name="Плохой товар", description="", price=100.0, quantity=0)
        assert "не может быть добавлен" in str(exc_info.value)

    def test_price_setter_rejects_non_positive(self, capsys):
        p = Product(name="Товар", description="", price=200.0, quantity=3)
        old_price = p.price

        p.price = -10
        assert p.price == old_price
        p.price = 0
        assert p.price == old_price

        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out

    def test_quantity_setter_allows_zero_but_rejects_negative(self, capsys):
        p = Product(name="Товар", description="", price=500.0, quantity=10)
        p.quantity = 0
        assert p.quantity == 0

        old_qty = p.quantity
        p.quantity = -5
        assert p.quantity == old_qty

        captured = capsys.readouterr()
        assert "Количество не может быть отрицательным" in captured.out


class TestProductStrAndTotalCost:
    """__str__, total_cost, включая edge-case с нулевым количеством."""

    def test_str_representation_normal(self) -> None:
        p = Product(name="Фляга", description="Фляга", price=1200, quantity=2)
        assert str(p) == "Фляга, 1200 руб. Остаток: 2 шт."

    def test_str_representation_zero_quantity(self) -> None:
        p = Product(name="Пустой товар", description="", price=500, quantity=1)
        p.quantity = 0
        assert str(p) == "Пустой товар, 500 руб. Остаток: 0 шт."

    def test_total_cost_normal_and_zero(self) -> None:
        p1 = Product(name="A", description="", price=10.5, quantity=3)
        assert p1.total_cost() == pytest.approx(31.5)

        p2 = Product(name="B", description="", price=10.5, quantity=5)
        p2.quantity = 0
        assert p2.total_cost() == pytest.approx(0.0)


class TestProductAddOperator:
    """Тестирование __add__: одинаковые классы, разные классы, NotImplemented."""

    def test_add_same_class_products(self) -> None:
        a = Product(name="A", description="", price=10, quantity=2)  # 20
        b = Product(name="B", description="", price=5, quantity=3)  # 15
        result = a + b
        assert result == pytest.approx(35.0)

    def test_add_different_subclasses_raises_type_error(self) -> None:
        p = Product(name="Обычный", description="", price=10, quantity=1)
        s = Smartphone(
            name="Смартфон",
            description="",
            price=500,
            quantity=1,
            model="X",
            efficiency=0.9,
            memory=128,
            color="чёрный",
        )
        with pytest.raises(TypeError):
            _ = p + s

    def test_add_between_same_subclass_works(self) -> None:
        phone1 = Smartphone(
            "Смартфон 1", "Описание", 20000.0, 5, "Pro", 9.5, 256, "чёрный"
        )
        phone2 = Smartphone(
            "Смартфон 2", "Описание", 22000.0, 4, "Lite", 9.0, 128, "белый"
        )
        total = phone1 + phone2
        expected = phone1.price * phone1.quantity + phone2.price * phone2.quantity
        assert total == pytest.approx(expected)


class TestCategoryBasic:
    """Категория: счётчики, add_product, products, total_value, average_price."""

    @pytest.fixture(autouse=True)
    def reset_counters(self) -> None:
        Category.category_count = 0
        Category.product_count = 0
        yield

    def test_category_initialization_increments_counter(self) -> None:
        assert Category.category_count == 0
        cat = Category(name="Электроника", description="Устройства")
        assert Category.category_count == 1
        assert cat.name == "Электроника"

    def test_add_product_increments_product_count(self) -> None:
        cat = Category(name="Тестовая", description="Описание")
        p = Product(name="Товар", description="", price=100.0, quantity=10)
        cat.add_product(p)
        assert Category.product_count == 1

    def test_add_product_rejects_non_product_objects(self) -> None:
        cat = Category(name="Защита", description="Проверка")
        for bad_obj in ["строка", {"name": "dict"}, object()]:
            with pytest.raises(TypeError):
                cat.add_product(bad_obj)

    def test_products_property_formatting(self) -> None:
        cat = Category(name="Категория", description="Товары")
        p1 = Product(name="Товар 1", description="", price=100, quantity=2)
        p2 = Product(name="Товар 2", description="", price=200, quantity=1)
        cat.add_product(p1)
        cat.add_product(p2)

        report = cat.products
        assert isinstance(report, str)
        assert "Товар 1, 100 руб. Остаток: 2 шт.\n" in report
        assert "Товар 2, 200 руб. Остаток: 1 шт.\n" in report

    def test_empty_category_products_returns_empty_string(self) -> None:
        cat = Category(name="Пустая", description="Нет товаров")
        assert cat.products == ""

    def test_total_value_correct_calculation(self) -> None:
        cat = Category(name="Стоимость", description="Расчёт")
        p1 = Product(name="A", description="", price=10, quantity=2)  # 20
        p2 = Product(name="B", description="", price=5, quantity=4)  # 20
        cat.add_product(p1)
        cat.add_product(p2)
        assert cat.total_value() == pytest.approx(40.0)

    def test_average_price_normal_and_empty(self) -> None:
        cat = Category(name="Средняя", description="Средняя цена")
        p1 = Product(name="A", description="", price=100, quantity=1)
        p2 = Product(name="B", description="", price=200, quantity=1)
        cat.add_product(p1)
        cat.add_product(p2)
        assert cat.average_price() == pytest.approx(150.0)

        empty_cat = Category(name="Пустая", description="Пусто")
        assert empty_cat.average_price() == 0.0

    def test_str_representation_of_category(self) -> None:
        cat = Category(name="Электроника", description="Все товары")
        p1 = Product(name="Товар1", description="", price=100, quantity=10)
        p2 = Product(name="Товар2", description="", price=200, quantity=5)
        cat.add_product(p1)
        cat.add_product(p2)

        result = str(cat)
        total_qty = p1.quantity + p2.quantity
        expected = f"Электроника, количество продуктов: {total_qty} шт."
        assert result == expected


class TestInheritanceAndSpecializedProducts:
    """Smartphone, LawnGrass: наследование, __str__, корректность типов."""

    def test_smartphone_is_product_and_has_correct_str(self) -> None:
        s = Smartphone(
            name="Смартфон X",
            description="Флагман",
            price=70000,
            quantity=1,
            model="Pro",
            efficiency=0.95,
            memory=512,
            color="серебристый",
        )
        assert isinstance(s, Product) and isinstance(s, BaseProduct)
        assert "Смартфон X (Pro)" in str(s)
        assert "память: 512 ГБ" in str(s)

    def test_lawn_grass_is_product_and_has_correct_str(self) -> None:
        g = LawnGrass(
            name="Газонная трава",
            description="Смесь",
            price=900,
            quantity=5,
            country="Беларусь",
            germination_period=10,
            color="тёмно-зелёная",
        )
        assert isinstance(g, Product) and isinstance(g, BaseProduct)
        assert "Газонная трава" in str(g)
        assert "срок прорастания: 10 дней" in str(g)


class TestFactoryMethods:
    """new_product и new_product_with_merge: корректность работы."""

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
        existing = [Product(name="Мышь", description="", price=2500.0, quantity=50)]
        new_data = {
            "name": "Мышь",
            "description": "Новое описание",
            "price": 3000.0,
            "quantity": 20,
        }
        merged = Product.new_product_with_merge(new_data, existing)
        assert merged is existing[0]
        assert merged.quantity == 70
        assert merged.price == 3000.0

    def test_merge_keeps_higher_price(self) -> None:
        existing = [Product(name="Товар", description="", price=1000.0, quantity=10)]

        lower_data = {"name": "Товар", "price": 900.0, "quantity": 5}
        Product.new_product_with_merge(lower_data, existing)
        assert existing[0].price == 1000.0

        higher_data = {"name": "Товар", "price": 1100.0, "quantity": 5}
        Product.new_product_with_merge(higher_data, existing)
        assert existing[0].price == 1100.0

    def test_merge_creates_new_if_not_exists(self) -> None:
        existing = []
        data = {
            "name": "Тарелка глубокая",
            "description": "Тарелка",
            "price": 400.0,
            "quantity": 2,
        }
        new_prod = Product.new_product_with_merge(data, existing)
        assert len(existing) == 0
        assert new_prod.name == "Тарелка глубокая"


class TestProduct:
    """Тесты для базового класса Product и его наследников."""

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

    def test_price_setter_rejects_non_positive_values(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        p = Product("Товар", "Описание", 100.0, 5)
        old_price = p.price

        p.price = -10.0
        assert p.price == old_price

        p.price = 0.0
        assert p.price == old_price

        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out

    def test_add_two_products_returns_total_value(self) -> None:
        a = Product("A", "Desc", 10.0, 2)  # 20
        b = Product("B", "Desc", 5.0, 3)  # 15
        result = a + b
        assert result == 35.0

    def test_add_with_non_product_returns_not_implemented(self) -> None:
        p = Product("A", "Desc", 10.0, 2)
        result = p.__add__("string")
        assert result is NotImplemented

    def test_add_between_different_subclasses_raises_type_error(self) -> None:
        phone = Smartphone(
            "Смартфон", "Описание", 20000.0, 5, "Pro", 9.5, 256, "чёрный"
        )
        grass = LawnGrass("Трава", "Описание", 1200.0, 50, "Россия", 7, "зелёная")
        with pytest.raises(TypeError):
            _ = phone + grass

    def test_add_between_same_subclass_works(self) -> None:
        phone1 = Smartphone(
            "Смартфон 1", "Описание", 20000.0, 5, "Pro", 9.5, 256, "чёрный"
        )
        phone2 = Smartphone(
            "Смартфон 2", "Описание", 22000.0, 4, "Lite", 9.0, 128, "белый"
        )
        total = phone1 + phone2
        expected = phone1.price * phone1.quantity + phone2.price * phone2.quantity
        assert total == expected

    def test_add_between_two_lawn_grass_works(self) -> None:
        grass1 = LawnGrass("Трава 1", "Описание", 1200.0, 50, "Россия", 7, "зелёная")
        grass2 = LawnGrass("Трава 2", "Описание", 1300.0, 40, "Россия", 6, "изумрудная")
        total = grass1 + grass2
        expected = grass1.price * grass1.quantity + grass2.price * grass2.quantity
        assert total == expected

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

    def test_quantity_setter_rejects_negative_values(self) -> None:
        p = Product("Товар", "Описание", 100.0, 10)
        old_qty = p.quantity

        p.quantity = -5
        assert p.quantity == old_qty

    def test_quantity_can_be_zero(self) -> None:
        p = Product("Товар", "Описание", 100.0, 10)
        p.quantity = 0
        assert p.quantity == 0

    def test_quantity_setter_allows_zero_after_creation(self, capsys):
        p = Product(name="Товар", description="Описание", price=500.0, quantity=10)

        p.quantity = 0
        assert p.quantity == 0

        assert p.total_cost() == 0.0

        assert str(p) == "Товар, 500 руб. Остаток: 0 шт."


class TestCategory:
    """Тесты для класса Category."""

    @pytest.fixture(autouse=True)
    def reset_counters(self):
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
        result = cat.add_product(p)
        assert result is None
        assert cat.product_quantity == 1

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

    def test_add_product_rejects_string(self) -> None:
        cat = Category("Тестовая", "Описание")
        with pytest.raises(TypeError) as exc_info:
            cat.add_product("просто строка")
        msg = str(exc_info.value).lower()
        assert "нельзя добавить объект типа" in msg
        assert "разрешены только объекты product" in msg

    def test_add_product_rejects_dict(self) -> None:
        cat = Category("Тестовая", "Описание")
        with pytest.raises(TypeError) as exc_info:
            cat.add_product({"name": "Плохой товар", "price": 100})
        assert "dict" in str(exc_info.value)

    def test_add_product_rejects_custom_class(self) -> None:
        class FakeItem:
            pass

        fake = FakeItem()
        cat = Category("Тестовая", "Описание")
        with pytest.raises(TypeError) as exc_info:
            cat.add_product(fake)
        assert "FakeItem" in str(exc_info.value)

    def test_add_product_accepts_smartphone_as_subclass(self) -> None:
        cat = Category("Тестовая", "Описание")
        phone = Smartphone(
            "Смартфон", "Описание", 20000.0, 5, "Pro", 9.5, 256, "чёрный"
        )
        cat.add_product(phone)
        assert cat.product_quantity == 1
        assert Category.product_count == 1

    def test_add_product_accepts_lawn_grass_as_subclass(self) -> None:
        cat = Category("Тестовая", "Описание")
        grass = LawnGrass("Трава", "Описание", 1200.0, 50, "Россия", 7, "зелёная")
        cat.add_product(grass)
        assert cat.product_quantity == 1
        assert Category.product_count == 1

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

        @pytest.fixture
        def category(self) -> None:
            return Category(name="Электроника", description="Все электронные товары")

        @pytest.fixture
        def products(self):
            return [
                Product(
                    name="Наушники", description="Наушники", price=5000.0, quantity=2
                ),
                Smartphone(
                    name="Смартфон Z",
                    description="Смартфон Z",
                    price=55000.0,
                    quantity=1,
                    model="Z1",
                    efficiency=0.97,
                    memory=256,
                    color="серый",
                ),
            ]


class TestProductBasic:
    """Тесты базового класса Product: инициализация, свойства, валидация, __str__."""

    def test_product_initialization_and_properties(self) -> None:
        p = Product(
            name="Чайник",
            description="Электрический чайник",
            price=2990.0,
            quantity=5,
        )
        assert p.name == "Чайник"
        assert p.description == "Электрический чайник"
        assert p.price == 2990.0
        assert p.quantity == 5

    def test_price_validation_negative(self, capsys) -> None:
        p = Product(
            name="Тостер",
            description="Тостер",
            price=-100.0,
            quantity=3,
        )
        assert p.price == 0.0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out

    def test_quantity_validation_negative(self, capsys) -> None:
        p = Product(
            name="Кофеварка",
            description="Кофеварка",
            price=4500.0,
            quantity=3,
        )
        p.quantity = -2
        assert p.quantity == 3
        captured = capsys.readouterr()
        assert "Количество не может быть отрицательным" in captured.out

    def test_str_representation(self) -> None:
        p = Product(name="Фляга", description="Фляга", price=1200.5, quantity=2)
        s = str(p)
        assert s.startswith("Фляга, ")
        assert s.endswith(" руб. Остаток: 2 шт.")
        import re

        match = re.search(r"\d+", s)
        assert match is not None

    def test_total_cost(self) -> None:
        p = Product(name="Кружка", description="Кружка", price=350.0, quantity=4)
        assert p.total_cost() == 1400.0

    def test_add_same_class_products(self) -> None:
        p1 = Product(name="Тарелка", description="Тарелка", price=200.0, quantity=3)
        p2 = Product(name="Чашка", description="Чашка", price=150.0, quantity=2)
        result = p1 + p2
        assert result == (p1.total_cost() + p2.total_cost())

    def test_add_different_classes_raises_type_error(self) -> None:
        p = Product(name="Ложка", description="Ложка", price=50.0, quantity=10)
        s = Smartphone(
            name="Смартфон X",
            description="Смартфон",
            price=30000.0,
            quantity=2,
            model="X10",
            efficiency=0.95,
            memory=256,
            color="чёрный",
        )
        with pytest.raises(TypeError):
            _ = p + s


class TestInheritanceAndSubclasses:
    """Проверка наследования, isinstance/issubclass, фабричных методов."""

    def test_smartphone_is_product(self) -> None:
        s = Smartphone(
            name="Смартфон Y",
            description="Смартфон Y",
            price=40000.0,
            quantity=1,
            model="Y20",
            efficiency=0.98,
            memory=512,
            color="белый",
        )
        assert isinstance(s, Product)
        assert issubclass(type(s), Product)

    def test_lawn_grass_is_product(self) -> None:
        g = LawnGrass(
            name="Газонная трава",
            description="Газон",
            price=1200.0,
            quantity=10,
            country="Россия",
            germination_period=14,
            color="зелёный",
        )
        assert isinstance(g, Product)
        assert issubclass(type(g), Product)

    def test_factory_new_product(self) -> None:
        data = {
            "name": "Кастрюля",
            "description": "Кастрюля из нержавейки",
            "price": 2500.0,
            "quantity": 3,
        }
        p = Product.new_product(data)
        assert p.name == "Кастрюля"
        assert p.price == 2500.0
        assert p.quantity == 3

    def test_factory_merge_existing_product(self) -> None:
        existing = [Product(name="Вилка", description="Вилка", price=100.0, quantity=5)]
        data = {
            "name": "Вилка",
            "description": "Вилка новая",
            "price": 110.0,
            "quantity": 3,
        }
        merged = Product.new_product_with_merge(data, existing)
        assert merged is existing[0]
        assert merged.quantity == 8  # 5 + 3
        assert merged.price == 110.0

    def test_factory_create_new_when_not_exists(self) -> None:
        existing = []
        data = {
            "name": "Тарелка глубокая",
            "description": "Тарелка",
            "price": 400.0,
            "quantity": 2,
        }
        new_prod = Product.new_product_with_merge(data, existing)
        assert len(existing) == 0
        assert new_prod.name == "Тарелка глубокая"


class TestEdgeCasesAndLogic:
    """Краевые случаи и логика, специфичная для твоего кода."""

    def setup_method(self) -> None:
        Category.category_count = 0
        Category.product_count = 0

    def test_empty_category_products_returns_empty_string(self) -> None:
        cat = Category("Пустая", "Пустая категория")
        assert cat.products == ""

    def test_empty_category_total_value_zero(self) -> None:
        cat = Category("Пустая", "Пустая категория")
        assert cat.total_value() == 0.0

    def test_multiple_additions_and_counters(self) -> None:
        cat = Category("Спорт", "Спортивные товары")
        p1 = Product(name="Мяч", description="Мяч", price=1000.0, quantity=3)
        p2 = Product(name="Гантель", description="Гантель", price=2500.0, quantity=2)

        cat.add_product(p1)
        cat.add_product(p2)

        assert Category.product_count == 2
        assert cat.product_quantity == 2
        assert cat.total_value() == (1000 * 3 + 2500 * 2)
