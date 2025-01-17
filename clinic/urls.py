from rest_framework.routers import DefaultRouter

from .views import DicomViewSet, FrameViewSet, MediaViewSet, StudyViewSet

router = DefaultRouter()
router.register(r"dicoms", DicomViewSet, basename="dicom")
router.register(r"studies", StudyViewSet, basename="study")
router.register(r"frames", FrameViewSet, basename="frame")
router.register(r"media", MediaViewSet, basename="media")

urlpatterns = router.urls
