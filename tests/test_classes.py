import pytest

from src.category import Category
from src.product import Product


class TestProductInitialization:
    """Тесты на корректную инициализацию Product."""

    def test_product_initialization_sets_all_attributes(self):
        p = Product("Ноутбук X1", "16 ГБ ОЗУ", 75000.50, 10)

        assert p.name == "Ноутбук X1"
        assert p.description == "16 ГБ ОЗУ"
        assert p.price == 75000.50
        assert p.quantity == 10

    def test_product_price_and_quantity_types(self):
        p = Product("Товар", "Описание", 100.0, 5)

        assert isinstance(p.price, float)
        assert isinstance(p.quantity, int)

    def test_negative_price_raises_error(self):
        with pytest.raises(ValueError):
            Product("Товар", "Описание", -10.0, 5)

    def test_negative_quantity_raises_error(self):
        with pytest.raises(ValueError):
            Product("Товар", "Описание", 100.0, -5)


class TestCategoryInitialization:
    """Тесты на корректную инициализацию Category."""

    @pytest.fixture
    def products(self):
        return [
            Product("A", "Desc A", 10.0, 2),
            Product("B", "Desc B", 20.0, 3),
        ]

    def test_category_initialization_sets_all_attributes(self, products):
        cat = Category("Электроника", "Устройства", products)

        assert cat.name == "Электроника"
        assert cat.description == "Устройства"
        assert cat.products is products  # тот же список
        # или, если нужно проверить содержимое:
        assert len(cat.products) == 2
        assert cat.products[0].name == "A"
        assert cat.products[1].name == "B"

    def test_products_list_must_contain_product_objects(self, products):
        # Создаём категорию — если там не Product, логика сломается на типизации
        cat = Category("Тестовая", "Тестовая категория", products)
        for item in cat.products:
            assert isinstance(item, Product)


class TestCategoryCounters:
    """Тесты на автоматические счётчики Category.category_count и Category.product_count."""

    @pytest.fixture(autouse=True)
    def reset_counters(self):
        """Сбрасываем счётчики перед каждым тестом — это важно для изолированности."""
        Category.category_count = 0
        Category.product_count = 0
        yield
        # можно сбросить ещё раз после теста, но autouse + начало теста достаточно
        Category.category_count = 0
        Category.product_count = 0

    def test_category_count_increases_by_one_per_category(self):
        assert Category.category_count == 0

        Category("Cat1", "Desc1", [])
        assert Category.category_count == 1

        Category("Cat2", "Desc2", [])
        assert Category.category_count == 2

        Category("Cat3", "Desc3", [])
        assert Category.category_count == 3

    def test_product_count_increases_by_length_of_products_list(self):
        # product_count должен считать длину списка (карточки), а не сумму quantity
        assert Category.product_count == 0

        # 2 карточки товаров
        Category("Cat1", "Desc1", [
            Product("A", "Desc", 10.0, 100),  # quantity=100 — не должно влиять
            Product("B", "Desc", 20.0, 200),  # quantity=200 — не должно влиять
        ])
        assert Category.product_count == 2  # длина списка

        # Ещё 1 карточка
        Category("Cat2", "Desc2", [
            Product("C", "Desc", 30.0, 300),
        ])
        assert Category.product_count == 3  # 2 + 1

    def test_multiple_categories_sum_their_products_lengths(self):
        # Cat1: 3 карточки, Cat2: 1 карточка → итого 4
        Category("Cat1", "Desc1", [
            Product("A", "", 10.0, 1),
            Product("B", "", 10.0, 1),
            Product("C", "", 10.0, 1),
        ])

        Category("Cat2", "Desc2", [
            Product("D", "", 10.0, 1),
        ])

        assert Category.category_count == 2
        assert Category.product_count == 4  # 3 + 1 = 4

    def test_empty_products_list_does_not_increase_product_count(self):
        Category("Empty", "No items", [])

        assert Category.category_count == 1
        assert Category.product_count == 0  # len([]) == 0
