from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from labeler.rest_framework import viewsets
from quality.models import QualityLabel
from quality.serializers import QualityLabelSerializer


class QualityLabelViewSet(viewsets.CamelCaseModelViewSet):
    """
    ViewSet for managing QualityLabel objects.
    """

    queryset = QualityLabel.objects.all()
    serializer_class = QualityLabelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user", "dicom", "quality_class"]

    def perform_create(self, serializer):
        """
        Custom logic during creation to prevent duplicate quality labels for the same user and dicom.
        """
        serializer.save(user=self.request.user)
