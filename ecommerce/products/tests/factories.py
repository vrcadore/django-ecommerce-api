import factory
from factory.django import DjangoModelFactory, ImageField

from ecommerce.products.models import (
    Attribute,
    Brand,
    Category,
    Product,
    ProductAttribute,
    ProductImage,
    ProductLine,
)
from ecommerce.users.tests.factories import UserFactory
from ecommerce.utils.factories import RelatedFactoryVariableList


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ["slug"]

    name = factory.Sequence(lambda i: f"Category {i}")
    slug = factory.Sequence(lambda i: f"categ{i}")
    is_active = True

    lft = 1
    rgt = 2
    tree_id = factory.Faker("pyint", min_value=100, max_value=10000)
    depth = 1

    created_by = factory.SubFactory(UserFactory, username="admin_factory")
    updated_by = factory.SelfAttribute("created_by")


class BrandFactory(DjangoModelFactory):
    class Meta:
        model = Brand
        django_get_or_create = ["slug"]

    name = factory.Sequence(lambda i: f"Brand {i}")
    slug = factory.Sequence(lambda i: f"brand{i}")
    description = factory.Faker("text", max_nb_chars=200)
    is_active = True

    created_by = factory.SubFactory(UserFactory, username="admin_factory")
    updated_by = factory.SelfAttribute("created_by")


class AttributeFactory(DjangoModelFactory):
    class Meta:
        model = Attribute
        django_get_or_create = ["slug"]

    name = factory.Sequence(lambda i: f"Attribute {i}")
    slug = factory.Sequence(lambda i: f"attr{i}")
    description = factory.Faker("text", max_nb_chars=200)
    is_active = True

    created_by = factory.SubFactory(UserFactory, username="admin_factory")
    updated_by = factory.SelfAttribute("created_by")


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product
        django_get_or_create = ["slug"]

    name = factory.Sequence(lambda i: f"Product {i}")
    slug = factory.Sequence(lambda i: f"prod{i}")
    description = factory.Faker("text", max_nb_chars=200)
    is_active = True

    category = factory.SubFactory(CategoryFactory)
    brand = factory.SubFactory(BrandFactory)

    owner = factory.SubFactory(UserFactory, username="admin_factory")
    created_by = factory.SelfAttribute("owner")
    updated_by = factory.SelfAttribute("owner")

    product_lines = RelatedFactoryVariableList(
        "ecommerce.products.tests.factories.ProductLineFactory",
        factory_related_name="product",
        size=2,
    )

    images = RelatedFactoryVariableList(
        "ecommerce.products.tests.factories.ProductImageFactory",
        factory_related_name="product",
        size=2,
    )


class ProductLineFactory(DjangoModelFactory):
    class Meta:
        model = ProductLine

    price = factory.Faker("pydecimal", right_digits=2, min_value=1, max_value=100)
    sku = factory.Faker("bothify", text="????-########")
    stock_quantity = factory.Faker("pyint", min_value=1, max_value=100)
    is_active = True

    created_by = factory.SubFactory(UserFactory, username="admin_factory")
    updated_by = factory.SelfAttribute("created_by")

    product = factory.SubFactory(ProductFactory)

    attributes = RelatedFactoryVariableList(
        "ecommerce.products.tests.factories.ProductAttributeFactory",
        factory_related_name="product_line",
        size=2,
    )


class ProductImageFactory(DjangoModelFactory):
    class Meta:
        model = ProductImage

    image = ImageField(color=factory.Faker("hexify", text="#^^^^^^"))
    alt_text = factory.Faker("text", max_nb_chars=100)

    created_by = factory.SubFactory(UserFactory, username="admin_factory")
    updated_by = factory.SelfAttribute("created_by")

    product = factory.SubFactory(ProductFactory)


class ProductAttributeFactory(DjangoModelFactory):
    class Meta:
        model = ProductAttribute

    value = factory.Faker("text", max_nb_chars=100)

    created_by = factory.SubFactory(UserFactory, username="admin_factory")
    updated_by = factory.SelfAttribute("created_by")

    product_line = factory.SubFactory(ProductLineFactory)
    attribute = factory.SubFactory(AttributeFactory)
