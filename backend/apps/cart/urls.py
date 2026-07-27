from rest_framework.routers import DefaultRouter

from .views import CartViewSet

router = DefaultRouter()
#"Everything inside CartViewSet belongs to the cart endpoint."
router.register("", CartViewSet, basename="cart")

urlpatterns = router.urls