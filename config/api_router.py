from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from ecommerce.products.api.views import (
    AttributeViewSet,
    BrandViewSet,
    CategoryViewSet,
    ProductImageViewSet,
    ProductLineViewSet,
    ProductViewSet,
)
from ecommerce.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("brands", BrandViewSet)
router.register("categories", CategoryViewSet)
router.register("products", ProductViewSet)
router.register("product_lines", ProductLineViewSet)
router.register("product_image", ProductImageViewSet)
router.register("attributes", AttributeViewSet)

app_name = "api"
urlpatterns = router.urls
