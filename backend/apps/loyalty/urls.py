from rest_framework.routers import DefaultRouter

from .views import LoyaltyViewSet

router = DefaultRouter()
router.register("", LoyaltyViewSet, basename="loyalty")

urlpatterns = router.urls