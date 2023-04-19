import uuid

from django.contrib.auth import get_user_model
from django.db import models
from treebeard.ns_tree import NS_Node

User = get_user_model()


class Category(NS_Node):
    """
    Category model. It represents a product category.
    It uses the treebeard library to implement the nested set model.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    is_active = models.BooleanField(default=False)

    created_by = models.ForeignKey(User, related_name="+", on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, related_name="+", on_delete=models.PROTECT)
    updated_at = models.DateTimeField(auto_now=True)

    node_order_by = ["name"]

    def __str__(self):
        """
        Return the slug of the category.
        """
        return self.slug

    class Meta:
        verbose_name_plural = "categories"


class Brand(models.Model):
    """
    Brand model. It represents a product brand.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    is_active = models.BooleanField(default=False)

    created_by = models.ForeignKey(User, related_name="+", on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, related_name="+", on_delete=models.PROTECT)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return the name of the brand.
        """
        return self.slug


class Attribute(models.Model):
    """
    Attribute model. It represents a product attribute.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    is_active = models.BooleanField(default=False)

    created_by = models.ForeignKey(User, related_name="+", on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, related_name="+", on_delete=models.PROTECT)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return the slug of the attribute.
        """
        return self.slug


class Product(models.Model):
    """
    Product model. It represents a product in the store.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=False)

    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )

    owner = models.ForeignKey(User, related_name="+", on_delete=models.PROTECT)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, related_name="+", on_delete=models.PROTECT)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return the slug of the product.
        """
        return self.slug


class ProductLine(models.Model):
    """
    Product Line model. It keeps a track of the stock quantity of a product.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=100, unique=True)
    stock_quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=False)

    created_by = models.ForeignKey(User, related_name="+", on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, related_name="+", on_delete=models.PROTECT)
    updated_at = models.DateTimeField(auto_now=True)

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_lines"
    )

    product_attributes = models.ManyToManyField(
        "Attribute", through="ProductAttribute", related_name="product_line"
    )

    def __str__(self):
        """
        Return the name of the product line.
        """
        return f"{self.stock_quantity} of {self.product.slug}({self.sku})"

    def get_owner(self):
        """
        Return the owner of the product line.
        """
        return self.product.owner

    class Meta:
        verbose_name_plural = "Product Lines"


class ProductImage(models.Model):
    """
    Product Image model. It represents an image of a product.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to="products")
    alt_text = models.CharField(max_length=100)

    created_by = models.ForeignKey(User, related_name="+", on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, related_name="+", on_delete=models.PROTECT)
    updated_at = models.DateTimeField(auto_now=True)

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )

    def __str__(self):
        """
        Return the name of the product image.
        """
        return f"{self.product} image"

    def get_owner(self):
        """
        Return the owner of the product image.
        """
        return self.product.owner


class ProductAttribute(models.Model):
    """
    Product Attribute model. It represents a product attribute, like color, size, etc.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.CharField(max_length=100)

    created_by = models.ForeignKey(User, related_name="+", on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, related_name="+", on_delete=models.PROTECT)
    updated_at = models.DateTimeField(auto_now=True)

    product_line = models.ForeignKey(ProductLine, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.PROTECT)

    def __str__(self):
        """
        Return the name of the product attribute.
        """
        return f"{self.product_line.product}({self.attribute}) - {self.value}"
