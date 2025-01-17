from rest_framework.routers import DefaultRouter

from quality.views import QualityLabelViewSet

router = DefaultRouter()
router.register(r"quality-labels", QualityLabelViewSet, basename="quality-label")

urlpatterns = router.urls
