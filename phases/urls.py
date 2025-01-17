from rest_framework.routers import DefaultRouter

from .views import PhaseClassViewSet, PhaseLabelViewSet, PhaseViewViewSet

router = DefaultRouter()
router.register(r"phase-classes", PhaseClassViewSet, basename="phase-class")
router.register(r"phase-labels", PhaseLabelViewSet, basename="phase-label")
router.register(r"phase-views", PhaseViewViewSet, basename="phase-view")

urlpatterns = router.urls
