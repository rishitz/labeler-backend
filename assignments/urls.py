from rest_framework.routers import DefaultRouter

from .views import (
    DicomLabelingJobViewSet,
    FullStudyAnnotationSetViewSet,
    StudyLabelingJobViewSet,
)

router = DefaultRouter()
router.register(
    r"full-study-annotation-sets",
    FullStudyAnnotationSetViewSet,
    basename="full-study-annotation-set",
)
router.register(
    r"study-labeling-jobs",
    StudyLabelingJobViewSet,
    basename="study-labeling-job",
)
router.register(
    r"dicom-labeling-jobs",
    DicomLabelingJobViewSet,
    basename="dicom-labeling-job",
)


urlpatterns = router.urls
