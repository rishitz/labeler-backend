from rest_framework.routers import DefaultRouter

from .views import (
    KeypointClassViewSet,
    KeypointCollectionClassViewSet,
    KeypointCollectionLabelViewSet,
    KeypointLabelViewSet,
)

router = DefaultRouter()
router.register(
    r"key-point-collection-classes",
    KeypointCollectionClassViewSet,
    basename="key-point-collection-class",
)
router.register(
    r"key-point-collection-labels",
    KeypointCollectionLabelViewSet,
    basename="key-point-collection-label",
)
router.register(r"key-point-classes", KeypointClassViewSet, basename="key-point-class")
router.register(r"key-point-labels", KeypointLabelViewSet, basename="key-point-label")

urlpatterns = router.urls
