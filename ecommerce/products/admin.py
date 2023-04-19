from typing import Any

from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from ecommerce.products.models import (
    Attribute,
    Brand,
    Category,
    Product,
    ProductAttribute,
    ProductImage,
    ProductLine,
)
from ecommerce.utils.admin import CustomAdminFileWidget

admin.site.site_header = "Ecommerce Admin"


@admin.register(Category)
class CategoryTreeAdmin(TreeAdmin):
    readonly_fields = (
        "created_by",
        "updated_by",
    )
    actions = ["make_active", "make_inactive"]
    form = movenodeform_factory(Category)
    list_filter = ["is_active"]
    search_fields = ["id", "name"]
    list_per_page = 15

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description="Mark selected as active")
    def make_active(self, request: Any, queryset: Any):
        queryset.update(is_active=True, updated_by=request.user)

    @admin.display(description="Mark selected as inactive")
    def make_inactive(self, request: Any, queryset: Any):
        queryset.update(is_active=False, updated_by=request.user)

    def save_form(self, request, form, change):
        if not change:
            form.instance.created_by = request.user
        form.instance.updated_by = request.user
        return super().save_form(request, form, change)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
    )
    actions = ["make_active", "make_inactive"]
    list_filter = ["is_active"]
    list_display = ["id", "name", "is_active"]
    search_fields = ["id", "name"]
    list_per_page = 15
    fieldsets = (
        (None, {"fields": ("name",)}),
        (_("Status info"), {"fields": ("is_active",)}),
        (
            _("Auditing info"),
            {"fields": ("created_by", "created_at", "updated_by", "updated_at")},
        ),
    )

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description="Mark selected as active")
    def make_active(self, request: Any, queryset: Any):
        queryset.update(is_active=True, updated_by=request.user)

    @admin.display(description="Mark selected as inactive")
    def make_inactive(self, request: Any, queryset: Any):
        queryset.update(is_active=False, updated_by=request.user)

    def save_form(self, request, form, change):
        if not change:
            form.instance.created_by = request.user
        form.instance.updated_by = request.user
        return super().save_form(request, form, change)


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
    )
    actions = ["make_active", "make_inactive"]
    list_filter = ["is_active"]
    list_display = ["id", "name", "slug", "is_active"]
    search_fields = ["id", "name", "slug"]
    list_per_page = 15
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "slug",
                    "description",
                )
            },
        ),
        (_("Status info"), {"fields": ("is_active",)}),
        (
            _("Auditing info"),
            {"fields": ("created_by", "created_at", "updated_by", "updated_at")},
        ),
    )

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description="Mark selected as active")
    def make_active(self, request: Any, queryset: Any):
        queryset.update(is_active=True, updated_by=request.user)

    @admin.display(description="Mark selected as inactive")
    def make_inactive(self, request: Any, queryset: Any):
        queryset.update(is_active=False, updated_by=request.user)

    def save_form(self, request, form, change):
        if not change:
            form.instance.created_by = request.user
        form.instance.updated_by = request.user
        return super().save_form(request, form, change)


class ProductImageInline(admin.TabularInline):
    verbose_name = "Image"
    verbose_name_plural = "Images"
    model = ProductImage
    readonly_fields = ("created_by", "updated_by")
    formfield_overrides = {models.ImageField: {"widget": CustomAdminFileWidget}}
    extra = 0


class ProductAttributeInline(admin.TabularInline):
    verbose_name = "Attribute"
    verbose_name_plural = "Attributes"
    model = ProductAttribute
    readonly_fields = ("created_by", "updated_by")
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ["make_active", "make_inactive"]
    readonly_fields = (
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
    )
    list_filter = ["is_active", "category"]
    list_display = ["id", "name", "slug", "category", "brand", "is_active"]
    search_fields = [
        "id",
        "name",
        "slug",
    ]
    list_per_page = 15
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "slug",
                )
            },
        ),
        (
            _("Details info"),
            {
                "fields": (
                    "category",
                    "brand",
                    "description",
                )
            },
        ),
        (
            _("Status info"),
            {
                "fields": (
                    "owner",
                    "is_active",
                )
            },
        ),
        (
            _("Auditing info"),
            {"fields": ("created_by", "created_at", "updated_by", "updated_at")},
        ),
    )
    inlines = [ProductImageInline]

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description="Mark selected as active")
    def make_active(self, request: Any, queryset: Any):
        queryset.update(is_active=True, updated_by=request.user)

    @admin.display(description="Mark selected as inactive")
    def make_inactive(self, request: Any, queryset: Any):
        queryset.update(is_active=False, updated_by=request.user)

    def save_form(self, request, form, change):
        if not change:
            form.instance.created_by = request.user
        form.instance.updated_by = request.user
        return super().save_form(request, form, change)


@admin.register(ProductLine)
class ProductLineAdmin(admin.ModelAdmin):
    actions = ["make_active", "make_inactive"]
    readonly_fields = (
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
        "get_product",
    )
    list_filter = ["is_active"]
    list_display = [
        "id",
        "get_product",
        "sku",
        "price",
        "stock_quantity",
        "is_active",
    ]
    search_fields = ["id", "get_product"]
    list_per_page = 15
    fieldsets = (
        (
            None,
            {"fields": ("sku", "get_product")},
        ),
        (
            _("Details info"),
            {
                "fields": (
                    "price",
                    "stock_quantity",
                )
            },
        ),
        (
            _("Status info"),
            {"fields": ("is_active",)},
        ),
        (
            _("Auditing info"),
            {"fields": ("created_by", "created_at", "updated_by", "updated_at")},
        ),
    )
    inlines = [ProductAttributeInline]

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description="Mark selected as active")
    def make_active(self, request, queryset):
        queryset.update(is_active=True, updated_by=request.user)

    @admin.display(description="Mark selected as inactive")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False, updated_by=request.user)

    def save_form(self, request, form, change):
        if not change:
            form.instance.created_by = request.user
        form.instance.updated_by = request.user
        return super().save_form(request, form, change)

    @admin.display(ordering="product", description="Product")
    def get_product(self, obj):
        return obj.product
