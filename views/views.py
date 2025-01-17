from rest_framework.permissions import IsAuthenticated

from labeler.rest_framework import viewsets
from views.models import ViewClass, ViewLabel
from views.serializers import ViewClassSerializer, ViewLabelSerializer


class ViewClassViewSet(viewsets.CamelCaseModelViewSet):
    http_method_names = ["get"]
    permission_classes = [IsAuthenticated]
    queryset = ViewClass.objects.all().order_by("-created_at")
    serializer_class = ViewClassSerializer


class ViewLabelViewSet(viewsets.CamelCaseModelViewSet):
    lookup_field = "uuid"
    permission_classes = [IsAuthenticated]
    serializer_class = ViewLabelSerializer
    filterset_fields = {
        "dicom__uuid": ["exact"],
    }
    queryset = (
        ViewLabel.objects.all()
        .order_by(
            "-created_at",
        )
        .select_related(
            "dicom",
            "view_class",
        )
    )

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                user=self.request.user,
            )
        )
