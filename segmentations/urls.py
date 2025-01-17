from rest_framework.routers import DefaultRouter

from segmentations.views import SegmentationClassViewSet, SegmentationLabelViewSet

router = DefaultRouter()
router.register(
    r"segmentation-labels", SegmentationLabelViewSet, basename="segmentation-label"
)

router.register(
    r"segmentation-classes", SegmentationClassViewSet, basename="segmentation-class"
)


urlpatterns = router.urls
