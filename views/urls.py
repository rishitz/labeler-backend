from rest_framework.routers import DefaultRouter

from views.views import ViewClassViewSet, ViewLabelViewSet

router = DefaultRouter()
router.register(r"view-classes", ViewClassViewSet, basename="view-class")
router.register(r"view-labels", ViewLabelViewSet, basename="view-label")

urlpatterns = router.urls
