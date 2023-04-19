import random
from typing import Any

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from ecommerce.products.models import Attribute, Brand, Category, Product
from ecommerce.products.tests.factories import (
    BrandFactory,
    CategoryFactory,
    ProductFactory,
)
from ecommerce.users.models import User
from ecommerce.users.tests.factories import UserFactory

NUM_USERS = 25
NUM_CATEGORIES_NODE = 2
NUM_CATEGORIES_LEVEL = 5
NUM_BRANDS = 25
NUM_PRODUCTS = 30


class Command(BaseCommand):
    """Populate database with fake data."""

    help = "Populate database with fake data."

    def add_arguments(self, parser):
        parser.add_argument("users", nargs="?", default=NUM_USERS, type=int)
        parser.add_argument(
            "categories_node", nargs="?", default=NUM_CATEGORIES_NODE, type=int
        )
        parser.add_argument(
            "categories_level", nargs="?", default=NUM_CATEGORIES_LEVEL, type=int
        )
        parser.add_argument("brands", nargs="?", default=NUM_BRANDS, type=int)
        parser.add_argument("products", nargs="?", default=NUM_PRODUCTS, type=int)

    @transaction.atomic
    def handle(self, *args: tuple, **options: dict[str, Any]):
        """
        Handle the command to populate the database with fake data.
        """
        self.stdout.write("Deleting old data...")
        # Need to be ordered by dependencies to avoid FK errors.
        models = [Product, Attribute, Brand, Category, User]
        for m in models:
            try:
                m.objects.all().delete()
            except m.DoesNotExist:
                raise CommandError(f"{type(m).__name__} does not exist.")

        # Create admin
        self.stdout.write("Creating admin users...")
        admin = UserFactory(
            username="admin",
            password="pass1234",
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )

        common_user = UserFactory(
            username="user",
            password="pass1234",
            is_active=True,
            is_staff=False,
            is_superuser=False,
        )

        # Create all extra users
        self.stdout.write("Creating new users...")
        num_users = options["users"]
        extra_users = UserFactory.create_batch(password="pass1234", size=num_users)

        # Add common user to extra users
        users = [common_user] + extra_users

        # Create all the brands
        self.stdout.write("Creating new brands...")
        num_brands = options["brands"]
        brands = BrandFactory.create_batch(
            size=num_brands, created_by=admin, updated_by=admin
        )

        # Create all the categories
        self.stdout.write("Creating new categories...")
        categories_level = options["categories_level"]
        categories_node = options["categories_node"]

        # Create many levels of categories
        root_category = CategoryFactory.build(
            name="Category 1",
            slug="category_1",
            created_by=admin,
            updated_by=admin,
        )
        root_category = Category.add_root(instance=root_category)
        categories_ids = [root_category.id]
        categories = []
        for _ in range(categories_level):
            new_categories_ids = []
            for node_id in categories_ids:
                parent = Category.objects.get(pk=node_id)
                for index in range(categories_node):
                    category = CategoryFactory.build(
                        name=f"{parent.name}.{index+1}",
                        slug=f"{parent.slug}_{index+1}",
                        created_by=admin,
                        updated_by=admin,
                    )
                    if parent:
                        category = parent.add_child(instance=category)
                    new_categories_ids.append(category.id)
                    categories.append(category)
            categories_ids = new_categories_ids

        # Add some products
        self.stdout.write("Creating new products...")
        num_products = options["products"]
        products = []
        for _ in range(num_products):
            # Randomize Owner
            user = random.choice(users)
            category = random.choice(categories)
            brand = random.choice(brands)

            product = ProductFactory(
                category=category,
                brand=brand,
                created_by=user,
                updated_by=user,
                owner=user,
            )
            products.append(product)
